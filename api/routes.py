from . import api_blueprint
import os
from flask import request, jsonify, Response, stream_with_context, json
import requests
import re

import time
import sys

from utils.parseChat import parse_chat_history
from utils.response import gemini_response
from utils.regularCall import regularCall



lastCalls = []

@api_blueprint.route('/get_query_response', methods=['POST', 'OPTIONS'])
def get_query_response():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Max-Age", "3600")  # Cache preflight for 1 hour
        return response
    elif request.method == "POST":
        data = request.get_json()
        query = data["query"]
    
        #raw_chat_history = data["chatHistory"]

    #chat_history = parse_chat_history(raw_chat_history)

   # app.logger.debug(f"Query: {query}")
    #app.logger.debug(f"Raw chat history: {raw_chat_history}")
    #app.logger.debug(f"Parsed chat history: {chat_history}")

    #making for 2 RPM

    currTime = time.time()

    if len(lastCalls) < 2:
     lastCalls.append(currTime)
     print("Less than 2")
    
    elif (currTime - lastCalls[0]) < 60:
         time.sleep(lastCalls[0] + 60 - currTime)
         print("slept")
         del lastCalls[0]
         lastCalls.append(currTime)
    else:
         del lastCalls[0]
         lastCalls.append(currTime)
         print("More than 2 but instant")
         
    


    resp = gemini_response(hobbies=query)

    resp = resp.replace('\n', '\n\n')

    def bold_line(match):
            return f"<b>{match.group(1)}:</b>{match.group(2)}"

    # This regular expression identifies lines containing ':'
    resp = re.sub(r'^(.+?):(.*)$', bold_line, resp, flags=re.MULTILINE)

    resp = re.sub(r'\*', '', resp)

    response = jsonify({"response": resp})

    return jsonify({"response": resp})
@api_blueprint.route('/get_reg', methods=['POST', 'OPTIONS'])
def get_reg():
    if request.method == "OPTIONS":
            response = jsonify({})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Max-Age", "3600")  # Cache preflight for 1 hour
            return response
    elif request.method == "POST":
         data = request.get_json()
         query = data["query"]
         raw_chat_history = data["chatHistory"]
    history = parse_chat_history(raw_chat_history)
    resp = regularCall(query, history)

    resp = resp.replace('\n', '\n\n')

    def bold_line(match):
            return f"<b>{match.group(1)}:</b>{match.group(2)}"

    # This regular expression identifies lines containing ':'
    resp = re.sub(r'^(.+?):(.*)$', bold_line, resp, flags=re.MULTILINE)

    resp = re.sub(r'\*', '', resp)

    

    return jsonify({"response": resp})


@api_blueprint.route('/test_cors', methods=['GET'])
def test_cors():
    return jsonify({"message": "CORS is working!"})

