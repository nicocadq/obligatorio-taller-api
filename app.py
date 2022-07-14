from flask import Flask, jsonify, request
from flask_cors import CORS
import serial, time

IRRIGATE = "1"
UPDATE_TEMPERATURE = "2"
UPDATE_HUMIDITY = "3"
GET_ACTUAL_DATA = "4"
UPDATE_INTERVAL = "5"
ON_OFF_TEMPERATURE = "6"
ON_OFF_HUMIDITY = "7"

app = Flask(__name__)
CORS(app)

# NOTE: this is the Mac Port: /dev/cu.usbmodem112301 should be changed for other devices
ArduinoSerial = serial.Serial(port='/dev/cu.usbmodem112401', baudrate=9600, timeout=.1)
time.sleep(2) 

@app.route('/', methods=['GET'])
def welcome():
  return "Hello world"


@app.route('/configure-temperature', methods=['POST'])
# Configurar humedad a la cual regar
def configure_temperature():
  import time

  data = request.get_json()

  temperature = data['temperature']

  temperature_message = UPDATE_TEMPERATURE + ":" + temperature

  ArduinoSerial.write(temperature_message.encode('utf-8'))
  time.sleep(5) 

  # message = ArduinoSerial.readline().decode()
  # time.sleep(5) 

  return jsonify(data)

@app.route('/configure-humidity', methods=['POST'])
# Configurar humedad a la cual regar
def configure_humidity():
  import time

  data = request.get_json()

  humidity = data['humidity']

  humidity_message = UPDATE_HUMIDITY + ":" + humidity

  ArduinoSerial.write(humidity_message.encode('utf-8'))
  time.sleep(5) 


  return jsonify(data)


@app.route('/configure-interval', methods=['POST'])
# Configurar humedad a la cual regar
def configure_interval():
  import time

  data = request.get_json()

  interval = data['interval']

  interval_message = UPDATE_INTERVAL + ":" + interval

  ArduinoSerial.write(interval_message.encode('utf-8'))
  time.sleep(5) 


  return jsonify(data)

@app.route('/irrigate', methods=['POST'])
# Regar
def irrigate():
  response = jsonify(message="Simple server is running")

  ArduinoSerial.write(IRRIGATE.encode('utf-8'))

  return response


@app.route('/current-data', methods=['GET'])
# Retorna temperatura y humedad actual, y minutos desde el ultimo regado
def current_data():
  import time

  ArduinoSerial.write(GET_ACTUAL_DATA.encode('utf-8'))
  time.sleep(5)

  data = ArduinoSerial.readline().decode().split(";")
  time.sleep(5)

  response = jsonify(data)

  return response

@app.route('/toggle-temperature', methods=['POST'])
# Apaga/Enciende el control de temperatura
def toggle_temperature():
  data = request.get_json()

  toggle = data['toggle']
  message = ON_OFF_TEMPERATURE + ":" + toggle

  ArduinoSerial.write(message.encode('utf-8'))

  response = jsonify(message="Turning temperature on/off")

  return response

@app.route('/toggle-humidity', methods=['POST'])
# Apaga/Enciende el control de humedad
def toggle_humidity():
  data = request.get_json()

  toggle = data['toggle']
  message = ON_OFF_HUMIDITY + ":" + toggle

  ArduinoSerial.write(message.encode('utf-8'))

  response = jsonify(message="Turning humidity on/off")

  return response

if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080, debug=True)