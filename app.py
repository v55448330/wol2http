from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def send_wol_packet(mac_address, broadcast_ip='255.255.255.255', port=9):
    mac_address = mac_address.replace(':', '')
    mac_address = mac_address.replace('-', '')
    mac_address = mac_address.replace('.', '')
    payload = bytes.fromhex('FF' * 6 + mac_address * 16)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(payload, (broadcast_ip, port))
    sock.close()

@app.route('/wakeup', methods=['POST'])
def wakeup():
    data = request.get_json()
    mac_address = data.get('mac_address')
    if not mac_address:
        return jsonify({'error': 'MAC address is missing'}), 400
    try:
        send_wol_packet(mac_address)
        return jsonify({'message': 'WOL packet sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
