from flask import Flask
from flask import request
from flask import jsonify
import db_worker as dbw
app = Flask(__name__)

Akey = 'TEST:TESTKEYID12:SUPERSECRETSTRING'

global db
db = dbw.database('database.db')

@app.route('/api/', methods=['POST','GET'])
def accept():
    a_type = request.args.get("type")
    channel = request.args.get("channel")
    if request.args.get("akey") == Akey:
        if a_type == 'get':
            try:
                sett = db.get_settings(request.args.get(str(channel)))
                coefs = db.get_coefs(request.args.get(str(channel)))
                return jsonify({'settings':sett,'coefs':coefs})
            except Exception:
                return '500'
        elif a_type == 'post':
            try:
                if db.get_settings(str(channel)):
                    if request.args.get("sc") == 's':
                        db.set_settings(channel,{'emoji':request.args.get("emoji"), 'copypasta':request.args.get("copypasta"), 'troll':request.args.get("troll"), 'insult':request.args.get("insult"),'alt':request.args.get("alt")})
                        return '200'
                    elif request.args.get("sc") == 'c':
                        db.set_coefs(channel,{'troll':request.args.get('troll'), 'insult':request.args.get("insult")})
                        return '200'
                    else:
                        return '500'
                else:
                    if request.args.get("sc") == 's':
                        db.create_settings(channel,{'emoji':request.args.get("emoji"), 'copypasta':request.args.get("copypasta"), 'troll':request.args.get("troll"), 'insult':request.args.get("insult"),'alt':request.args.get("alt")})
                        return '200'
                    elif request.args.get("sc") == 'c':
                        db.create_coefs(channel,{'troll':request.args.get('troll'), 'insult':request.args.get("insult")})
                        return '200'
                    else:
                        return '500'
            except Exception:
                return '500'
    return '500'        
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2048)
