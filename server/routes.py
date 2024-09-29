# from main import app
# from flask import Flask, request, jsonify, send_from_directory
# from scraping_file import InstagramBot
# from flask_cors import CORS
# import json
# import os

# @app.route('/api', methods=['POST'])
# def api_endpoint():
#     data = request.get_json() 
    
#     username = data.get('username')
#     password = data.get('password')
#     item_list = data.get('list')

#     if username is None or password is None or item_list is None:
#         return jsonify({'error': 'Missing data!'}), 400
#     else:
#         bot = InstagramBot(username, password, item_list)
#         bot.start_bot()
#         response = {
#             'message': 'Data received successfully!',
#             'username': username,
#             'list': item_list
#         }
#     return jsonify(response), 200