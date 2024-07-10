import constants
try:
    import RPi.GPIO as GPIO
except (Exception):
    from MockGPIO import GPIO

ILLUMINATION = 17
IRRIGATOR = 23
AIR_CONDITIONING = 27
MECHANICAL_VENTILATION = 22
READY_LIGHT = 24
LOW_WATER_LEVEL_WARN = 26
MANUAL_MODE = 19

def setup():
  print('GPIO configuration - Started')
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(ILLUMINATION, GPIO.OUT)
  GPIO.setup(IRRIGATOR, GPIO.OUT)
  GPIO.setup(AIR_CONDITIONING, GPIO.OUT)
  GPIO.setup(MECHANICAL_VENTILATION, GPIO.OUT)
  GPIO.setup(READY_LIGHT, GPIO.OUT)
  GPIO.setup(LOW_WATER_LEVEL_WARN, GPIO.OUT)
  GPIO.setup(MANUAL_MODE, GPIO.OUT)
  print('GPIO configuration - Done')

def turn_off_all():
   set_illumination(constants.ACTIVE_OFF)
   set_air_conditioning(constants.ACTIVE_OFF)
   set_irrigator(constants.ACTIVE_OFF)
   set_mechanical_ventilation(constants.ACTIVE_OFF, 0)
   set_ReadyLight(constants.ACTIVE_OFF)
   set_LowWaterLevelWarn(constants.ACTIVE_OFF)
   set_ManualMode(constants.ACTIVE_OFF)
def cleanUp():
  GPIO.cleanup()

def set_ReadyLight(active : str) :
   set_pin_output_high(READY_LIGHT, _is_on(active))

def set_LowWaterLevelWarn(active : str) :
   set_pin_output_high(LOW_WATER_LEVEL_WARN, _is_on(active))

def set_ManualMode(active : str) :
   set_pin_output_high(MANUAL_MODE, _is_on(active))

def set_illumination(active : str) :
   set_pin_output_high(ILLUMINATION, _is_on(active))

def set_air_conditioning(active : str) :
   set_pin_output_high(AIR_CONDITIONING, _is_on(active))

def set_irrigator(active : str) :
   set_pin_output_high(IRRIGATOR, _is_on(active))

def set_mechanical_ventilation(active : str, power: int) :
   set_pin_output_high(MECHANICAL_VENTILATION, _is_on(active))

def set_pin_output_high(pin : int, high: bool):
  GPIO.output(pin, GPIO.HIGH if high else GPIO.LOW)

def _is_on(active : str):
   return True if active == constants.ACTIVE_ON else False