import json
import apiai

import twilio.twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse

from flask import Flask, request, redirect

# Twilio account info
with open('/home/rgpeach10/Documents/Workspace/lightphone/secrets.json', 'r') as f:
    secrets = json.load(f)
account_sid = secrets['account_sid']
auth_token = secrets['auth_token']
account_num = secrets['account_num']
client = Client(account_sid, auth_token)

# api.ai account info
CLIENT_ACCESS_TOKEN = secrets['api.ai.AT']
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello api.ai (from Flask!)'

@app.route("/", methods=['GET', 'POST'])
def server():
    from flask import request
    # get SMS input via twilio
    resp = MessagingResponse()

    # get SMS metadata
    msg_from = request.values.get("From", None)
    msg = request.values.get("Body", None)

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
        client.messages.create(to=msg_from, from_= account_num, body=response)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
