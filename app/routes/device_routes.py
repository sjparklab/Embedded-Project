from flask import Blueprint, request, jsonify

device_bp = Blueprint('device', __name__, url_prefix='/api/device')

@device_bp.post('/temperature')
def receive_temp():
    data = request.json
    print('Raspberry Pi temperature:', data)
    return jsonify({'status': 'received'})
