# -*- coding: utf-8 -*-\
import os
import sys
import json
from datetime import datetime,  date
import time
import requests
import random
import threading
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import tweepy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#configurating  Discover
global timestart, routine
routine = []

activity_start=['09','10','11','12']
activity_end = ['00','01','02','03','04','05']

bad_signs = ['( ','((',':(',';(','хуй','бля','сук','ненавижу','хейт','йобаний','піздос','хуйово','мда','блеть','гавно','ужас','косячно',' плохо']
good_signs =[')','))',':)','<3','отличн','супер','хорош',' удал','неплох','ок','верю','надеюсь','будет','пройдёт','прокатит','прорвё','never give','вуху']
#Teaching to evaluate emotions
def mood_evaluate(msg):
    #basic mood value = 50 = content
    msg = msg.encode('utf-8')
    msg = msg.lower()
    mood = 50
    lenght = len(msg)
    #How one sign of bad mood affects the whole image
    symbol_koeff = 100/lenght
    #Counting bad signs
    for sign in bad_signs:
        count_signs = msg.find(sign)
        if count_signs >-1:
            mood= mood-symbol_koeff*count_signs
    #Counting good signs
    for sign in good_signs:
          count_signs = msg.find(sign)
          if count_signs >-1:
            mood= mood+symbol_koeff*count_signs
    if mood<10:
        return 'very bad'
    if mood<25:
        return 'bad'
    if mood>=25 and mood<=65:
        return 'ok'
    if mood>=85:
        return 'very good'
    if mood>65:
        return 'good'


class Character(db.Model):
   __tablename__ = "stats"
   date = db.Column(db.TIMESTAMP , primary_key=True)
   location = db.Column(db.Integer)
   mood = db.Column(db.Integer)
   money = db.Column(db.Integer)
   food = db.Column(db.Integer)
   def __init__(self,date,location,moood,money):
        self.date = date
        self.location = location
        self.mood = mood
        self.money = money
   def __repr__(self):
        return '<date>' % self.date


#Database of bot's contacts
class Friends(db.Model):
    __tablename__ = "friends"
    page_id = db.Column(db.Integer)
    date = db.Column(db.TIMESTAMP , primary_key=True)

    def __init__(self,date, page_id):
        self.date = date
        self.page_id=page_id


#Databse of bot's inventory
class Products(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self,type_id, price):
        self.type_id=type_id
        self.price = price


#Function executed before first request on the server.

def send_automatic():
    print('exec')
    def run_sender():
            send_message(u'1579846222104780', 'First')
    thread = threading.Thread(target=run_sender)
    thread.start()
@app.before_first_request(send_automatic())

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
x=1

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    if message_text == "Аніме".decode('UTF-8'):
                        send_message(sender_id, sender_id)
                    else:
                        send_message(sender_id, mood_evaluate(message_text))
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
    return 'ok',200


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

#checking out status of the server if it's already online.
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
    consumer_secret= os.environ["CONSUMER_SECRET_TWITTER"]
    access_key=os.environ["ACCESS_KEY_TWITTER"]
    access_secret=os.environ["ACCESS_SECRET_TWITTER"]
    print(consumer_key)
    print('succes')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    twitter=tweepy.API(auth)

def tweet(twit):
    if len(twit)<=140 and len(twit)>0:
        twitter.update_status(twit) #обновляем статус (постим твит)
        return True
    else:
        return False

init()
if __name__ == '__main__':
    #checking status of server before running first functions
    check_status()

    #initiliazing twitter
    #remembering the time we started
    timestart=datetime.now()
    print(str(timestart))
    #running the server
    app.run(debug=True)
