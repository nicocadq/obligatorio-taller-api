from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def welcome():
  return "Hello world"

@app.route('/configure', methods=['POST'])
  #  Configurar humedad y temperatura a la cual regar
def configure():
  data = request.get_json()
  
  temperature = data['temperature']
  humidity = data['humidity']

  return jsonify(data)

@app.route('/irrigate', methods=['POST'])
def irrigate():
  # Regar la planta basandose
  response = jsonify(message="Simple server is running")

  return response

@app.route('/time', methods=['GET'])
def time():
  # Retorna date del ultimo regado 
  response = jsonify(message="123")

  return response

if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080, debug=True)
