import os
import json
import subprocess

import apiai

import twilio.twiml
from twilio.rest import Client

from twilio.http.http_client import TwilioHttpClient

from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect

# Twilio account info
with open('/home/rgpeach10/Documents/Workspace/lightphone/secrets.json', 'r') as f:
    secrets = json.load(f)
account_sid = secrets['account_sid']
auth_token = secrets['auth_token']
account_num = secrets['account_num']
my_number = secrets['my_number']

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
client = Client(account_sid, auth_token, http_client=proxy_client)

# api.ai account info
CLIENT_ACCESS_TOKEN = secrets['api.ai.AT']
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello api.ai (from Flask!)'

@app.route("/", methods=['GET', 'POST'])
def server():
    # get SMS input via twilio
    resp = MessagingResponse()

    # get SMS metadata
    msg_from = request.values.get("From", my_number)
    msg = request.values.get("Body", "")
    
    # Security
    if msg_from != my_number:
        client.messages.create(to=msg_from, from_=account_num, body="Unauthorized Access")
        client.messages.create(to=my_number, from_=account_num, body=f"Unauthorized Access by {msg_from}. Msg reads: {msg}")
        return str(resp)
    
    # Bash Access
    if msg.startswith('!'):
        msg = msg[1:]
        if msg:
            out = subprocess.check_output(msg.split(' ')).decode('utf-8')[0:100]
            client.messages.create(to=msg_from, from_=account_num, body=out)
        return str(resp)

    # Python Access
    if msg.startswith('?'):
        msg = msg[1:]
        if msg:
            out = eval(msg)
            client.messages.create(to=msg_from, from_=account_num, body=out)
        return str(resp)

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = msg

    # get response from API.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
        # send SMS response back via twilio
        client.messages.create(to=msg_from, from_=account_num, body=response)
    else:
        client.messages.create(to=msg_from or my_number, from_=account_num, body="Internal Server Error 500")
        raise Exception(str(request))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
