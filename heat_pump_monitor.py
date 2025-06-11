from pymodbus.client import ModbusTcpClient
import time
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 1502
SLAVE_ID = 1
DB_NAME = "heat_pump_data.db"
POWER_REGISTER = 100
SCALE_TEMP = 10
SCALE_POWER = 100

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS heat_data
                     (timestamp TEXT, temperature_C REAL, power_kW REAL)''')
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"DB init error: {e}")
    finally:
        conn.close()

def poll_data():
    client = None
    try:
        client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
        if not client.connect():
            logger.error("Failed to connect to Modbus device")
            return None
        result = client.read_holding_registers(address=POWER_REGISTER, count=2, slave=SLAVE_ID)
        if not result.isError():
            temperature = result.registers[0] / SCALE_TEMP
            power = result.registers[1] / SCALE_POWER
            data = {
                "temperature_C": temperature,
                "power_kW": power,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            logger.info(f"Data polled: {data}")
            return data
        else:
            logger.error(f"Modbus read error: {result}")
            return None
    except Exception as e:
        logger.error(f"Modbus error: {e}")
        return None
    finally:
        if client is not None:
            client.close()

def log_data(data):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO heat_data VALUES (?, ?, ?)",
              (data['timestamp'], data['temperature_C'], data['power_kW']))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    while True:
        data = poll_data()
        if data:
            log_data(data)
        print(data)
        time.sleep(5)