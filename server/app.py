from flask import Flask
from subprocess import call
from flask_cors import CORS
from scraping_file import InstagramBot

app = Flask(__name__)
CORS(app)

@app.route('/')
def Home():
    return "Hello from flask, api call recieved successfully from "

@app.route('/login/<username>&&<password>')
def Home2(username,password):
    bot = InstagramBot(username=username,password=password)
    result = bot.start_bot()
    return result

@app.route('/process', methods=['POST'])
def process_form():
    data = request.form.get('data')
    my_object = InstagramBot(data)
    result = my_object.my_method()
    return f"Result: {result}"

@app.route('/login',methods=['POST'])
def login():
    return "Hello world"

if __name__ == '__main__':
    app.run()