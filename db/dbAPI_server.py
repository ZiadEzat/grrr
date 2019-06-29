import config_load as cl
from DB import getSettings, updateCogSettings
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

API_KEY = cl.config_load()['key']


@app.route('/api/<int:server_id>', methods=['POST', 'GET'])
def accept(server_id):
    if request.args.get("key") == API_KEY:
        if request.method == 'GET':
            try:
                settings = (getSettings(server_id))
                if settings is None:
                    return jsonify({"error": "No server with that ID was found"}), 404
                del settings['_id']
                return jsonify(settings), 200
            except Exception as e:
                return jsonify({'error': e}), 500
        elif request.method == 'POST':
            try:
                body = request.get_json()
                updateCogSettings(server_id, body['cog'], body['setting'])
                return jsonify({'response': 'success', 'data': body}), 200
            except Exception as e:
                return jsonify({'error': e}), 500
        else:
            return '500'
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2048)
