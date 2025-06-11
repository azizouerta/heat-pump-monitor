import sqlite3
import paho.mqtt.client as mqtt
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DB_NAME = "heat_pump_data.db"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "heatpump/status"

mqtt_client = mqtt.Client()
def on_connect(client, userdata, flags, rc):
    logger.info("MQTT connected" if rc == 0 else f"MQTT failed: {rc}")
mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()

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

def log_data(data):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO heat_data VALUES (?, ?, ?)",
                    (data['timestamp'], data['temperature_C'], data['power_kW']))
        conn.commit()
        logger.info(f"Logged to SQLite: {data}")
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
    finally:
        conn.close()

def publish_mqtt(data):
    try:
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data), qos=1)
        logger.info(f"Published to {MQTT_TOPIC}: {data}")
    except Exception as e:
        logger.error(f"MQTT error: {e}")

if __name__ == "__main__":
    init_db()
    while True:
        try:
            temp = float(input("Enter temperature (°C): "))
            power = float(input("Enter power (kW): "))
            data = {
                "temperature_C": temp,
                "power_kW": power,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            log_data(data)
            publish_mqtt(data)
        except ValueError:
            logger.error("Invalid input: Please enter numeric values")
        except KeyboardInterrupt:
            logger.info("Exiting...")
            mqtt_client.loop_stop()
            break