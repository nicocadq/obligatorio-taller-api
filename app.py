from flask import Flask, jsonify, request
from flask_cors import CORS
import serial, time

IRRIGATE = "1"
UPDATE_TEMPERATURE = "2"
UPDATE_HUMIDITY = "3"
LAST_IRRIGATE = "4"
UPDATE_INTERVAL = "5"
GET_TEMP_HUM = "6"
ON_OFF_TEMPERATURE = "7"
ON_OFF_HUMIDITY = "8"

app = Flask(__name__)
CORS(app)

ArduinoSerial = serial.Serial(port='/dev/cu.usbmodem112301', baudrate=9600, timeout=.1)
time.sleep(2) 

@app.route('/', methods=['GET'])
def welcome():
  return "Hello world"

  # /dev/cu.usbmodem112301

@app.route('/configure-temperature', methods=['POST'])
  #  Configurar humedad a la cual regar
def configure_temperature():
  import time

  data = request.get_json()

  temperature = data['temperature']

  temperature_message = UPDATE_TEMPERATURE + ":" + temperature

  ArduinoSerial.write(temperature_message.encode('utf-8'))
  time.sleep(5) 

  # message = ArduinoSerial.readline().decode()
  # time.sleep(5) 

  # print(message)

  return jsonify(data)

@app.route('/configure-humidity', methods=['POST'])
  #  Configurar humedad a la cual regar
def configure_humidity():
  import time

  data = request.get_json()

  humidity = data['humidity']

  humidity_message = UPDATE_HUMIDITY + ":" + humidity

  ArduinoSerial.write(humidity_message.encode('utf-8'))
  time.sleep(5) 


  return jsonify(data)


@app.route('/configure-interval', methods=['POST'])
  #  Configurar humedad a la cual regar
def configure_interval():
  import time

  data = request.get_json()

  interval = data['interval']

  interval_message = UPDATE_INTERVAL + ":" + interval

  ArduinoSerial.write(interval_message.encode('utf-8'))
  time.sleep(5) 


  return jsonify(data)

@app.route('/irrigate', methods=['POST'])
def irrigate():
  # Regar la planta basandose
  response = jsonify(message="Simple server is running")

  ArduinoSerial.write(IRRIGATE.encode('utf-8'))

  return response

@app.route('/time', methods=['GET'])
def time():
  import time
  # Retorna minutos desde ultimo regado 

  ArduinoSerial.write(LAST_IRRIGATE.encode('utf-8'))
  time.sleep(5)

  minutes = ArduinoSerial.readline().decode()
  time.sleep(5)

  print(minutes)

  response = jsonify(minutes)

  return response


# Merge this endpoint with the time one
@app.route('/actualData', methods=['GET'])
def actualData():
  import time

  ArduinoSerial.write(GET_TEMP_HUM.encode('utf-8'))
  time.sleep(3)

  data = ArduinoSerial.readline().decode().split(";");

  return jsonify(data)

if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080, debug=True)