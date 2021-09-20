from pprint import pprint
from requests_toolbelt import MultipartEncoder
import requests
import json
import sys
import os
import DNAC
from config import WEBEX_BOT_ACCESS_TOKEN, TEAMS_BOT_URL
try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()

#Global Variables
webexUrl = "https://api.ciscospark.com/v1/"
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + WEBEX_BOT_ACCESS_TOKEN
}

def webex_webhook ():
    print ("Gnork is starting. publicUrl: " + TEAMS_BOT_URL + "\n")

    #Post Webex Webehook
    url = webexUrl + "webhooks/"
    payloadMembership = {
        "name": "Brandon Test Bot",
        "targetUrl": TEAMS_BOT_URL,
        "resource": "memberships",
        "event": "created"
        }
    payloadMessages = {
        "name": "Brandon Test Bot",
        "targetUrl": TEAMS_BOT_URL,
        "resource": "messages",
        "event": "created"
        }
    payloadAttachment = {
            "name": "Brandon Test Bot",
            "targetUrl": TEAMS_BOT_URL,
            "resource": "attachmentActions",
            "event": "created"
            }
    responseMemberships = requests.post(url, headers=headers, json=payloadMembership)
    responseMessages = requests.post(url, headers=headers, json=payloadMessages)
    responseAttachment = requests.post(url, headers=headers, json=payloadAttachment)
    if responseMemberships.status_code != 200:
        print ("Webhook registration error")
        print(responseMemberships.text.encode('utf8'))
        exit(0)
    elif responseMessages.status_code != 200:
        print ("Webhook registration error")
        print(response.text.encode('utf8'))
        exit(0)
    elif responseAttachment.status_code != 200:
        print ("Webhook registration error")
        print(response.text.encode('utf8'))
        exit(0)


def send_get(url, payload=None,js=True):

    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request


def send_post(url, data):

    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request


def help_me():

    return "Sure! I can help. Below are the commands that I understand:<br/>" \
           "`Help me` - I will display what I can do.<br/>" \
           "`Hello` - I will display my greeting message<br/>" \
           "`Repeat after me` - I will repeat after you <br/>" \
           "`List devices` - I will list devices in DNA Center <br/>" \
           "`Show Device Config` - I will attach the device configuraiton for your device <br/>" \
           "`Image Compliance` - I will show the image software compliance"


def greetings():

    return "Hi my name is %s.<br/>" \
           "Type `Help me` to see what I can do.<br/>" % bot_name



app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def teams_webhook():
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        if webhook['data']['personEmail']!= bot_email:
            pprint(webhook)
        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            send_post( webexUrl + "messages",
                            {
                                "roomId": webhook['data']['roomId'],
                                "markdown": (greetings() +
                                             "**Note This is a group room and you have to call "
                                             "me specifically with `@%s` for me to respond**" % bot_name)
                            }
                            )
        msg = None
        msgPoint = None
        if "@webex.bot" not in webhook['data']['personEmail']:
            result = send_get(webexUrl + 'messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower() + " ", '')
            if in_message.startswith('help me'): #Help Me Post
                msg = help_me()
            elif in_message.startswith('hello'): #Hello Post
                msg = greetings()
            elif in_message.startswith("list devices"): #List DNAC Devices Post
                msg = DNAC.get_device_list()
            elif in_message.startswith("image compliance"):
                msg = DNAC.get_compliance_list()
            elif in_message.startswith("show device config"): #Attach DNAC Device Config Post
                msg = DNAC.get_device_config()
                m = MultipartEncoder({'roomId': webhook['data']['roomId'],
                                    'text': msg,
                                    'files': ('Switch_Config.txt', open('/tmp/Switch_Config.txt', 'rb'),'image/txt')})
                msgPoint = 1
            else:
                msg = "Sorry, but I did not understand your request. Type `Help me` to see what I can do"
        if msgPoint == 1: #AttachFile Messages Post
            r = requests.post(webexUrl  + "messages", data=m, headers={'Authorization': 'Bearer ' + WEBEX_BOT_ACCESS_TOKEN ,'Content-Type': m.content_type})
        elif msg != None: #Formated Text Messages Post
            send_post(webexUrl  + "messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
        return "true"
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\" alt=\"Webex Teams Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Webex Teams!</i></b></center>" % bot_name
        return message

def main():
    global bot_email, bot_name
    if len(WEBEX_BOT_ACCESS_TOKEN) != 0:
        test_auth = send_get(webexUrl + "people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.webex.com/my-apps "
                  "and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/my-apps "
              "and generate a new access token.")
        sys.exit()

    if "@webex.bot" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access token, view it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/my-apps "
              "and generate a new access token for your Bot.")
        sys.exit()
    else:
        webex_webhook()
        app.run(host='localhost', port=8080)

if __name__ == "__main__":
    main()
