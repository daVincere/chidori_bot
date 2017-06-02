"""
First messenger bot
"""

import sys, json, traceback, requests

# always instantiate the flask application like this
from flask import Flask, request, render_template

import thekey

application = Flask(__name__)
app = application

@app.route('/builder')
def builder():
	return render_template("builder.html")


@app.route('/', methods=['GET'])
# why?
def handle_verification():
	print "Handle Verification"

	if request.args.get('hub.verify_token', '') == thekey.VERIFICATION_TOKEN:
		print "Voila! Webhook Verified"

		return request.args.get('hub.challenge', '')
	else:
		return "Wrong verification code"

# ====== Bot Processing =========
@app.route('/', methods=['POST'])
def handle_message():
	payload = request.get_data()

	# Handle messages
	for sender_id, message in messaging_events(payload):
		# starts processing valid data
		try:
			response = processIncoming(sender_id, message)
			if response is not None:
				send_message(thekey.ACCESS_TOKEN, sender_id, response)
				print response
			else:
				send_message(thekey.ACCESS_TOKEN, sender_id, "Sorry I didn't get your message")
				print "Invalid message"

		except Exception, e:
			# getting realtime exceptions
			print e
			# why this?
			traceback.print_exc()
	return "ok"

def processIncoming(user_id, message):
	# The data is recieved in the json format
	if message['type'] == 'text':
		message_text = message['data']
		return message_text

	elif message['type'] == 'location':
		response = "I recieved this location (%s, %s) (y)" %(message['data'][0], message['data'][1])
		return response

	elif message['type'] == 'audio':
		audio_url = message['data']
		response = "I recieved audio at %s" %(audio_url)
		return response

	# for stuff that can't be recognized by the messenger
	else:
		print "*scratching my head*"
		return "Something different"


def send_message(token, user_id, text):
	"""
	Send the message text to recipient with id recipient
	"""

	r = requests.post(
					"https://graph.facebook.com/v2.6/me/messages",
					params={"access_token": token},
					data = json.dumps({
								"recipient" : {"id":user_id},
								"message" : {"text": text.decode('unicode_escape')}
							}),
					headers = {"Content-type": 'application/json'}
					)

	if r.status_code != requests.codes.ok:
		print r.text


# Generate tuples of (sender_id, message_text) from the provided payload
# This part technically cleans up received data to pass only meaningful data to processIncoming() function

def messaging_events(payload):
	data = json.loads(payload)

	messaging_events = data["entry"][0]["messaging"]

	for event in messaging_events:
		sender_id = event["sender"]["id"]

		# Ifnot a message
		if "message" not in event:
			yield sender_id, None

		# In case of a pure text message
		if "message" in event and "text" in event["message"] and "quick_reply" not in event["message"]:
			data = event["message"]["text"].encode('unicode_escape')
			yield sender_id, {'type': 'text', 'data': data, 'message_id': event['message']['mid']}

		# Message with attachment (location, audio, photo, file etc)
		elif "attachments" in event['message']:
			# In case the message is a location
			if "location" == event['message']['attachments'][0]['type']:
				coordinates = event['message']['attachments'][0]['payload']['coordinates']

				latitude = coordinates['lat']
				longitude = coordinates['long']

				yield sender_id, {'type':'location', 'data':[latitude, longitude], 'message_id': event['message']['mid']}

			# In case of an audio in the message
			elif "audio" == event['message']['attachments'][0]["type"]:
				audio_url = event['message']['attachments'][0]['payload']['url']

				yield sender_id, {'type':'audio', 'data': audio_url, "message_id": event['message']['mid']}

			else:
				yield sender_id, {'type': 'text', 'data':"Opps. Didn't sign-up for this", "message_id": event['message']['mid']}

		elif "quick_reply" in event['message']:
			data = event['message']['quick_reply']['payload']

			yield sender_id, {'type':'text', 'data':data, 'message_id': event['message']['mid']}

		else:
			yield sender_id, {'type':'text', 'data':"I don't understand this. Seriously!", 'message_id': event['message']['mid']}


# simple running protocol
if __name__ == '__main__':
	# if port no different
	app.run()

