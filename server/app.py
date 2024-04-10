from flask import Flask, jsonify, request
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app, origins='http://localhost:5173')

redis_host = '147.45.148.191'
redis_port = 6379
redis_username = 'default'
redis_password = 'Skn\\Zax/$Hx90:'

# Подключение к Redis
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

# GET-запрос для получения значения из Redis
@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    value = r.get(key)
    if value is None:
        return jsonify({'message': 'Key not found'}), 404
    return jsonify({key: value.decode('utf-8')}), 200

# SET-запрос для установки значения в Redis
@app.route('/set', methods=['POST'])
def set_value():
    data = request.get_json()
    if 'key' not in data or 'value' not in data:
        return jsonify({'message': 'Key and value required'}), 400
    key = data['key']
    value = data['value']
    r.set(key, value)
    return jsonify({'message': 'Value set successfully'}), 200

@app.route('/lrange_data_from_redis', methods=['GET'])
def get_data_from_redis():
    keys = r.keys('*') 
    data = {}
    for key in keys:
        value = r.get(key)
        data[key.decode('utf-8')] = value.decode('utf-8')
    return jsonify(data), 200



if __name__ == '__main__':
    app.run(debug=True)
