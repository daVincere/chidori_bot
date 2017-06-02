"""
Second Messenger Bot
"""

import requests
import json
from flask import Flask, request
import apiai

# Messenger Credentials
ACCESS_TOKEN = "EAAYHOejOPgYBAIdvrIbABXZBkyZBlUOtfkuFsWK6aX0ZBDT9EA3eBqplX3YkzIjBTmX7n5FnEIQkJyBOy2UQDCBcgPBAKwuuW8JxJhMTEDKo4Dg0YCwCgPLytfQlu8VX2myaA9SZByIZAdQsGZBqficnx0eiuCeV9hjPzn55kDKAZDZD"

# apiai Credentials
CLIENT_ACCESS_TOKEN = "83ca492d5bb04b3d81aa0408d92c90d4"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/dholu', methods=['GET'])
def verify():
	# our endpoint echos back the 'hub.challenge' value
	# specified when we setup the webhook
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		# if the webhook has been subscribed and there's an argument as "hub.challenge"
		if not request.args.get("hub.verify_token") == "1234567890":
			return "Verification token mismatch", 443
		return request.args['hub.challenge'], 200

	return 'Hello World(from flask!)', 200


def reply(user_id, msg):
	data = {
	'recipient' : {'id': user_id},
	'message': {'text':msg},
	} 

	resp = requests.post("https://graph.facebook.com/v2.9/me/messages?access_token="+ACCESS_TOKEN , json=data) 
	print resp.content


@app.route('/dholu', methods=['POST'])
def handle_incoming_message():
	data = request.json
	sender = data['entry'][0]['messaging'][0]['sender']['id']
	message = data['entry'][0]['messaging'][0]['message']['text']

	# prepare apiai request

	req = ai.text_request()
	req.lang = 'en' # optional, default value 'en'
	req.query = message

	# get response from api.ai
	api_response = req.getresponse()
	responsestr = api_response.read().decode('utf-8')
	response_obj = json.loads(responsestr)

	if 'result' in response_obj:
		response = response_obj['result']['fulfillment']['speech']

	reply(sender, response)

	return "ok"

if __name__ == '__main__':
	app.run(debug=True)