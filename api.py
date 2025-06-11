from fastapi import FastAPI, HTTPException
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
DB_NAME = "heat_pump_data.db"

@app.get("/heatpump/status")
async def get_status():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM heat_data ORDER BY timestamp DESC LIMIT 1")
        row = c.fetchone()
        if row:
            return {
                "temperature_C": row[1],
                "power_kW": row[2],
                "timestamp": row[0]
            }
        raise HTTPException(status_code=404, detail="No data available")
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/heatpump/history")
async def get_history(limit: int = 5):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM heat_data ORDER BY timestamp DESC LIMIT ?", (limit,))
        data = c.fetchall()
        if not data:
            raise HTTPException(status_code=404, detail="No data available")
        return [
            {
                "timestamp": row[0],
                "temperature_C": row[1],
                "power_kW": row[2]
            }
            for row in data
        ]
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/heatpump/average")
async def get_average(start: str, end: str):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT AVG(temperature_C), AVG(power_kW)
            FROM heat_data
            WHERE timestamp BETWEEN ? AND ?
        """, (start, end))
        row = c.fetchone()
        if row[0] is None or row[1] is None:
            raise HTTPException(status_code=404, detail="No data available in range")
        return {
        
            "average_temperature_C": round(row[0], 3),
            "average_power_kW": round(row[1], 3),
            "start_date": start,
            "end_date": end 
        }
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
