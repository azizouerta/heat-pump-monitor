from modbus_tk import modbus_tcp, defines
import random
import logging
import time 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_server():
    server = modbus_tcp.TcpServer(address="0.0.0.0", port=1502)
    server.start()
    logger.info("Modbus TCP server started on 0.0.0.0:1502")
    slave = server.add_slave(1)
    slave.add_block("holding", defines.HOLDING_REGISTERS, 100, 10)
    while True:
        temp = int(random.uniform(20.0, 30.0) * 10)  # Temp in °C (scaled)
        power = int(random.uniform(1.0, 5.0) * 100)  # Power in kW (scaled)
        slave.set_values("holding", 100, [temp, power])
        logger.info(f"Set: temp={temp/10}°C, power={power/100}kW")
        time.sleep(5)

if __name__ == "__main__":
    run_server()
    