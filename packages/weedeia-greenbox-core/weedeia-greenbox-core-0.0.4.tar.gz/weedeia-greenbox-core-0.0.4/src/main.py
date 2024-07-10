from fastapi import FastAPI
import signal
import sys
import random
import uvicorn

import src.gpio

def handle_exit(_signal, _frame):
    gpio.turn_off_all()
    gpio.cleanUp()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
gpio.setup()
gpio.turn_off_all()

app = FastAPI()

@app.get("/management/status")
def health_check():
  return "UP"

@app.put("/illumination/{active}")
def setIllumination(active : str):
  gpio.set_illumination(active)

@app.put("/air-conditioning/{active}")
def setAirConditioning(active : str):
  gpio.set_air_conditioning(active)

@app.put("/irrigator/{active}")
def setIrrigator(active : str):
  gpio.set_irrigator(active)

@app.put("/mechanical-ventilation/{active}/{power}")
def setMechanicalVentilation(active : str, power : int):
  gpio.set_mechanical_ventilation(active, power)

@app.put("/ready-light/{active}")
def setReadyLight(active : str):
  gpio.set_ReadyLight(active)

@app.put("/low-water-level-warn/{active}")
def setReadyLight(active : str):
  gpio.set_LowWaterLevelWarn(active)

@app.put("/manual-mode/{active}")
def setReadyLight(active : str):
  gpio.set_ManualMode(active)

@app.get("/temperature-humidity")
def getTemperatureAndHumidity():
  # mock
  return {
    "temperature": random.randint(16, 38),
    "humidity": random.randint(40, 80)
  }

@app.get("/water-level")
def getWaterLevel():
  # mock
  return {
    "level": random.randint(0, 50)
  }

def main():
  uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()