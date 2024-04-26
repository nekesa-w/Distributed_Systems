from flask import flask

app=Flask(_name_)

@app.route('/home', methods=['GET'])

def home():
      server_id=os.environ.get('SERVER_ID', 'Unknown')
      return f "Hello from Server: {server_id}",200

@app.route('/heartbeat', methods=['GET'])
def  heartbeat():
      return "", 200 

if _name_=='_main_':
app.run(host='0.0.0.0', port=5000)
