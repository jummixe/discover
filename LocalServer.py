# -*- coding: utf-8 -*-\
import time

import worldProcessing
import datetime
from datetime import timedelta
from datetime import datetime

import json


class LocalResponser:

    def __init__(self,time_run,interval=5):
        self.discover = worldProcessing.init_discover()
        self.routine = worldProcessing.init_routine()
        self.time_run = time_run
        self.start_time = datetime.now().hour
        self.end_time = datetime.now() + timedelta(hours=self.time_run)
        self.interval = interval

    def check_time(self):
        print(str(datetime.now().hour)+" <?> " + str(self.end_time))
        if datetime.now() >= self.end_time:
            return True
        else:
            return False

    def request(self,message):
        print("Local request: "+message)
        self.response(worldProcessing.process_string("пидор",message))

    def response(self,msg):
        print("Discover response:"+msg)

    def process(self):
        print("Processing time in Discover world")
        self.routine.time_process()
        self.discover.calculateStats()
        print("LOG STATE after processing")
        self.log_state()

    def log_state(self):
        print("Discover goal: "+ str(self.discover.goal.suggest_actions()))
        print("############ PHYSICAL STATS ##############")
        print("Discover hunger:" + str(self.discover.hunger))
        print("Discover mood"+ str(self.discover.mood))
        print("Discover thirst"+str(self.discover.thirst))
        print("############ BELONGINGS ##################")
        print("Discover money"+ str(self.discover.money))
        print("Discover inventory"+str(self.discover.inventory))
        print("Discover location"+self.discover.location.names["where"])
        print("############# STORY ######################")
        if len(self.discover.story) > 0:
            print(self.discover.story)
            for event in self.discover.story:
                print(str(self.discover.story.index(event))+" event is of following type"+event.event_type)
                print(event.loc.names["what"]+" is where this event happened")
                print(str(event.adjectives[0])+" is what she thinks about it")
        else:
            print("Discover have no story to show you.")

def main_loop():

    responder = LocalResponser(24,5)

    while not responder.check_time():
        responder.routine.state -=1
        responder.process()
        responder.request("ПОШЕЛ")
        responder.routine.resolve_story()
        time.sleep(responder.interval)


if __name__ == '__main__':
    main_loop()
