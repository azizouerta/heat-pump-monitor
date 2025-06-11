# Heat Pump Monitoring System

   A Python application to monitor heat pump data via Modbus TCP, store it in SQLite, and expose it through FastAPI endpoints.

   ## Features
   - Polls temperature (°C) and power (kW) from a Modbus TCP server at `127.0.0.1:1502`.
   - Stores data in SQLite (`heat_pump_data.db`).
   - FastAPI endpoints:
     - `GET /heatpump/status`: Latest data.
     - `GET /heatpump/history?limit=N`: Last N records.
     - `GET /heatpump/average?start=YYYY-MM-DDTHH:MM:SS&end=YYYY-MM-DDTHH:MM:SS`: Average temperature and power.

   ## Requirements
   - Python 3.9+
   - Dependencies: See `requirements.txt`

   ## Setup
   1. Clone repository:
      ```bash
      git clone <repository-url>
      cd heat-pump-monitor
      ```
   2. Create virtual environment:
      ```bash
      python3 -m venv heat_pump_env
      source heat_pump_env/bin/activate
      pip install -r requirements.txt
      ```
   3. Run Modbus simulator:
      ```bash
      python3 heat_pump_simulator.py
      ```
   4. Run monitor:
      ```bash
      python3 heat_pump_monitor.py
      ```
   5. Run FastAPI:
      ```bash
      uvicorn api:app --reload --port 8000
      ```

   ## Files
   - `heat_pump_simulator.py`: Modbus TCP server simulating heat pump.
   - `heat_pump_monitor.py`: Polls data and stores in SQLite.
   - `api.py`: FastAPI app with REST endpoints.
   - `requirements.txt`: Python dependencies.
   - `.gitignore`: Excludes virtual env and SQLite DB.

   ## Endpoints
   - `GET /heatpump/status`: Returns latest temperature, power, timestamp.
   - `GET /heatpump/history?limit=N`: Returns last N records.
   - `GET /heatpump/average?start=YYYY-MM-DDTHH:MM:SS&end=YYYY-MM-DDTHH:MM:SS`: Returns average temperature and power.

   ## Future Enhancements
   - MQTT publishing.
   - Unit tests with `pytest`.
   - Additional endpoints (e.g., reset data).

   ## License
   MIT

   ## Author
   Aziz
