﻿#-------------------------------------------------------------------------------
# Name:        DiscoverMemory
# Purpose:     to manage DisoverChan's memory
#
# Author:      Jummixe
#
# Created:     30.09.2018
# Copyright:   (c) Jummixe 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy
import discoverServer as Server
db = SQLAlchemy()

class Character(db.Model):
   __tablename__ = "stats"
   date = db.Column(db.TIMESTAMP , primary_key=True)
   location = db.Column(db.Integer)
   mood = db.Column(db.Integer)
   money = db.Column(db.Integer)
   food = db.Column(db.Integer)

   def __init__(self,date,location,mood,money):
        self.date = date
        self.location = location
        self.mood = mood
        self.money = money

   def __repr__(self):
        return '<date>' % self.date


#db of bot's contacts
class Friends(db.Model):
    __tablename__ = "friends"
    page_id = db.Column(db.Integer)
    date = db.Column(db.TIMESTAMP , primary_key=True)

    def __init__(self,date, page_id):
        self.date = date
        self.page_id=page_id
    def __repr__(self):
        return '<date>' % self.date

#Databse of bot's inventory
class Products(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    name = db.Column(db.String)

    def __init__(self,item_id, type_id, price):
        self.id=item_id
        self.type_id=type_id
        self.price = price

    def __repr__(self):
        return '<date>' % self.date

class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String)
    location = db.Column(db.Integer)
    date = db.Column(db.TIMESTAMP , primary_key=True)

    def __init__(self,event_type, location, date):
        self.event_type = event_type
        self.location = location
        self.date = date
    def __repr__(self):
        return '<date>' % self.date

def init(app):
    global db
    db = SQLAlchemy(app)


def main(db):
    pass


if __name__ == '__main__':
    main(db)
