from flask import Flask, app
from flask.globals import request
from flask_socketio import SocketIO
import socketio
from flask_cors import CORS
from utils.rest_utils import Mockerpi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)

@app.route('/product/update', methods=['PUT'])
def update_product():
    data = request.get_json()
    updated_product = Mockerpi().update_product(data)
    socketio.emit('product_updated')
    return updated_product, 200


if __name__== '__main__':
    socketio.run(app, port="5001", host="0.0.0.0")