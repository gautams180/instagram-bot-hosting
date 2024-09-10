from flask import Flask, request, jsonify, send_from_directory
from scraping_file import InstagramBot
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

frontend_folder = os.path.join(os.getcwd(),"..")
print(frontend_folder)
build_folder = os.path.join(frontend_folder,"build")

#Serve static files from the "build" folder under the "frontend" directory

@app.route("/", defaults={"filename":""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(build_folder,filename)

#To fetch followers
@app.route('/login/<username>&&<password>')
def Home2(username,password):
    bot = InstagramBot(username=username,password=password)
    result = bot.start_bot()
    return result

@app.route('/api', methods=['POST'])
def api_endpoint():
    data = request.get_json() 
    
    username = data.get('username')
    password = data.get('password')
    item_list = data.get('list')

    if username is None or password is None or item_list is None:
        return jsonify({'error': 'Missing data!'}), 400
    else:
        bot = InstagramBot(username, password, item_list)
        bot.start_bot()
        response = {
            'message': 'Data received successfully!',
            'username': username,
            'list': item_list
        }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)