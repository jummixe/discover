# -*- coding: utf-8 -*-\
import os
import sys
import json
import codecs
from datetime import datetime, date
import time
import requests
import random
import threading
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import tweepy
import discover
import worldProcessing
import discoverMemory
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MYDIR = os.path.dirname(__file__)

def get_self():
    return app


def set_database():
    global db
    db = discoverMemory(SQLAlchemy(app))


def get_database():
    global db
    if db is not None:
        return db
    else:
        db = SQLAlchemy(app)
        return db


# configurating  Discover
global timestart, routine
routine = []

activity_start = ['09', '10', '11', '12']
activity_end = ['00', '01', '02', '03', '04', '05']


@app.before_first_request
def automatic():
    global routinedisc
    worldProcessing.init_discover()
    print("Discover Chan setted-up!")
    worldProcessing.init_discover()
    routinedisc = worldProcessing.init_routine()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=discover_iterate, trigger="interval",minutes=15)
    scheduler.start()
    send_message(u'1579846222104780', "Automatic")
   # send_message(u'1579846222104780', worldProcessing.return_thoughts())
    time.sleep(10)
    return "Huh", 200


def discover_iterate():
    routinedisc.time_process()
    story = routinedisc.resolve_story()
    send_message(u'1579846222104780', "Automatic")
   # send_message(u'1579846222104780', "pew-pew")

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    if routinedisc and routinedisc.char:
        return render_template("home.html", location=routinedisc.char.location.names["where"],hunger=str(routinedisc.char.hunger), mood = str(routinedisc.char.mood))
    else:
        return "404",200

x = 1

@app.route('/Status', methods=['GET'])
def report_status():
    return worldProcessing.return_thoughts(), 200

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    my_id = "0"
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][
                        "id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    worldProcessing.process(messaging_event)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
    return 'ok', 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = msg.decode('utf-8')
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


# checking out status of the server if it's already online.
def check_status():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('https://discoverchan.herokuapp.com')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


def init():
    global twitter
    consumer_key = os.environ["CONSUMER_KEY_TWITTER"]
    consumer_secret = os.environ["CONSUMER_SECRET_TWITTER"]
    access_key = os.environ["ACCESS_KEY_TWITTER"]
    access_secret = os.environ["ACCESS_SECRET_TWITTER"]
    print(consumer_key)
    print('succes')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    twitter = tweepy.API(auth)


def tweet(twit):
    if len(twit) <= 140 and len(twit) > 0:
        twitter.update_status(twit)  # обновляем статус (постим твит)
        return True
    else:
        return False


init()

if __name__ == '__main__':
    print("Server response")
    # checking status of server before running first functions
    check_status()
    worldProcessing.init_discover()
    # initiliazing twitter
    # remembering the time we started
    timestart = datetime.now()
    print(str(timestart))
    # running the server
    app.run(debug=True, use_reloader=False)
    discoverMemory.init(app)
