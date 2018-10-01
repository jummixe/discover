#-------------------------------------------------------------------------------
# Name:        Discover Chan interface
# Purpose:     To manage Discover chan
#
# Author:      Jummixe
#
# Created:     30.09.2018
# Copyright:   (c) Jummixe 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import discover as discoverWorld

def return_thoughts():
    return  discoverChar.rethink_events()

def init_discover():
    global discoverChar
    discoverWorld.get_time()
    discoverChar = discoverWorld.Character(100,2500,discoverWorld.HomeLoc,discoverWorld.Disinventory,100,50)
    discoverChar.routine_start()

class routine():
    def __init__ (self,speed,active=False):
        self.speed = speed
        self.active = active

    def time_process():
        discoverWorld.get_time()
        discoverWorld.discover_time(discoverWorld.Hour)


def process_goals():
    discoverChar.goal_processing()

def start_routine():
    discoverChar.routine_start()

def remind_inventory(inventory):
    pass

