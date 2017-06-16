# chidori_bot
Facebook messenger chat-bots.

Work under progress. 

The aim is to create three more bots:

1. A music player, playing youtube videos of the particular song.
2. A chatbot based on one of a close friend. 
3. //getting ahead of myself.

Cheers!

To use this script though, 
1. Go to https://developers.facebook.com and create a new messenger app. 
2. If you haven't made a facebook page, make one. 
3. Get a public access token against your page from the app dashboard.
4. Copy the Public Access Token in key.py as:
   </br>ACCESS_TOKEN = "Your Public Access Token"
   </br>VERIFICATION_TOKEN = "Any string that you may like. For eg here: your_phone_number"
5. Install requirements as:
   pip install -r requirements.txt
5. Run the script as:
   </br> python <script_name> 3000 
6. Download ngrok, unzip it, from commandline go to the directory and run it as:
   ngrok http 3000
7. On your app, set up the webhook as:
   </br> Callback URL: https://something.ngrok.io
   </br> Verification Token: "The string that you'd set earlier at step 4"
   Save and verify.
8. Check it out.
