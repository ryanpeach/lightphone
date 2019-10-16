import json
import apiai
from flask import Flask
import twilio.twiml
from twilio.rest import TwilioRestClient

# Twilio account info
account_sid = "AC11ba____________________96e87003"
auth_token = "6789333____________________849d2"
account_num = "+1617_____42"
client = TwilioRestClient(account_sid, auth_token)

# api.ai account info
CLIENT_ACCESS_TOKEN = "78c0e0________________fbcd9404a2"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello api.ai (from Flask!)'

@app.route("/", methods=['GET', 'POST'])
def server():
    from flask import request
    # get SMS input via twilio
    resp = twilio.twiml.Response()

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