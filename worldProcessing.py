# -------------------------------------------------------------------------------
# Name:        Discover Chan interface
# Purpose:     To manage Discover chan
#
# Author:      Jummixe
#
# Created:     30.09.2018
# Copyright:   (c) Jummixe 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import discover as discoverWorld
import json


def return_thoughts():
    return discoverChar.rethink_events()


def init_discover():
    global discoverChar
    discoverWorld.get_time()
    discoverChar = discoverWorld.Character(100, 2500, discoverWorld.HomeLoc, discoverWorld.Disinventory, 100, 50)
    return discoverChar


def init_routine():
    global discoverChar
    basicRoutine = Routine(speed=1, char = discoverChar, active=True)
    basicRoutine.start_routine()
    basicRoutine.time_process()
    basicRoutine.process_goals()
    return basicRoutine


def process(messagejson):
    sender = messagejson["sender"]["id"]
    message = messagejson["message"]["text"]

    if sender == "1579846222104780":
        print("Max messaging" + message)

    else:
        print("someone_else messaging")


def process_string(id,msg):

    if id == "1579846222104780":
        print("Max messaging" + msg)

    else:
        print("someone_else messaging")
    return "Pip"

class Routine():

    def __init__(self, speed, char, active=False):
        self.speed = speed
        self.active = active
        self.state = discoverWorld.Hour
        self.char =  char

    def time_process(self):
        discoverWorld.get_time()
        discoverWorld.discover_time(discoverWorld.Hour)
        if discoverWorld.Hour > self.state:
            self.create_goals()
            self.process_goals()
            self.state = discoverWorld.Hour
            self.char.calculateStats()

    def create_goals(selfs):
        if discoverChar.goal.achieved:
            discoverWorld.day_goal(discoverChar)

    def process_goals(self):
        discoverChar.goal_processing()

    def start_routine(self):
        discoverChar.routine_start()

    def resolve_story (self):
        discoverChar.rethink_events()

    def remind_inventory(inventory):
        pass
