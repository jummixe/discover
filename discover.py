# -*- coding: utf-8 -*-\
import os
import sys
import json
import codecs
from collections import defaultdict
import random
from datetime import datetime, date

all_flags = []

Global_items = []
global Hour, Minute, Day


# appends an object to the list, returning index
def get_id(id_list, what):
    id_list.append(what)
    return len(id_list) - 1


class Character():
    goal = None
    routine = None
    memory = []

    def __init__(self, mood, money, location, inventory, hunger, thirst):
        self.mood = mood
        self.money = money
        self.location = location
        self.inventory = inventory
        self.hunger = hunger
        self.thirst = thirst
        self.path = None
        self.story = []

    @property
    def region(self):
        global regions
        for region in regions:
            if self.location.loc_id in region.locations:
                self.region = region

    @property
    def weight(self):
        self.weight = 0
        for i in self.inventory:
            self.weight += i.weight

    # taking actions to process the goal
    def goal_processing(self):
        actions = self.goal.suggest_actions()
        if not self.goal.achieved:
            print(actions)
            print('actions')
            for action in actions:
                if action == 'move':
                    if not self.path:
                        self.create_path(self.goal.location)
                        print(self.path)
                    if self.move():
                        self.create_event('move')
                elif action == 'earn':
                    if work_Flag in self.location.flags:
                        self.create_event('earn')
                else:
                    self.create_event(action)
        else:
            self.goal = None
            # raw_input('routine completed.')

    # create_event in characters memory, to process it  then as a story
    def create_event(self, event_type):

        flags = self.location.flags
        verbs_f = []
        adjectives_f = []

        if event_type == 'enjoy':
            for flag in flags:
                for comp in flag.flag_components:
                    for verb in range(0, len(comp.verbs)):
                        print(flag.flag_components)
                        verbs_f.append(verb)
                    for adj in range(0, len(comp.adjectives)):
                        adjectives_f.append(adj)
            event_new = Event(datetime.now(), event_type='observation', flags=flags, verbs=verbs_f,
                              adjectives=adjectives_f, loc=self.location)

        if event_type == 'move':
            for comp in moveflag.flag_components:
                for verb in range(0, len(comp.verbs)):
                    verbs_f.append(verb)
                    ##raw_input(verbs_f)
                for adj in range(0, len(comp.adjectives)):
                    adjectives_f.append(adj)
            event_new = Event(datetime.now(), event_type='moving', flags=[moveflag], verbs=verbs_f,
                              adjectives=adjectives_f, loc=self.location)

        if event_type == 'collect':
            shop = self.location.shop
            print('shop')
            item_flags = []
            ##raw_input(shop)
            if shop is not False:
                for flag in Global_items[self.goal.inventory].flags:
                    item_flagsl = []
                    for comp in flag.flag_components:
                        for verb in range(0, len(comp.verbs)):
                            verbs_f.append(verb)
                            ####raw_input(verbs_f)
                        for adj in range(0, len(comp.adjectives)):
                            adjectives_f.append(adj)
                item_flags.append(productFlag)
                event_new = Event(datetime.now(), event_type='collect', flags=item_flags, verbs=verbs_f,
                                  adjectives=adjectives_f, loc=self.location)

        if event_type == 'eat':
            print('eat')
            item_flags = []
            ##raw_input(shop)
            if shop is not False:
                for flag in flag.flag_components:
                    for comp in flag.flag_components:
                        for verb in range(0, len(comp.verbs)):
                            verbs_f.append(verb)
                            ####raw_input(verbs_f)
                        for adj in range(0, len(comp.adjectives)):
                            adjectives_f.append(adj)
                event_new = Event(datetime.now(), event_type='eat', flags=[tasty_food, nasty_food], verbs=verbs_f,
                                  adjectives=adjectives_f, loc=self.location)

        self.story.append(event_new)

    # creates story summarizing all the events happened
    def rethink_events(self):

        story = ''
        story_new = Story(self, self.story, "present simple")
        story_new.time = story_new.decide_time()
        ###raw_input(self.story)
        index = 0
        if len(story_new.events) == 0:
            return normalize("i have nothing to tell yet")

        for event in story_new.events:
            if index > 0:
                story += '. ' + story_new.construct(event)
            else:
                story += story_new.construct(event)
            index += 1
        ##raw_input(story)
        story = normalize(story)
        print(story)
        return story

    def create_path(self, destination):
        print('>>>>>>>>>>>>>>>>>')
        print(destination)
        print(self.location.loc_id)
        print('>>>>>>>>>>>>>>>>>')
        self.path = path_find(self.location.loc_id, destination)
        print(self.path)

    def create_regions_path(self, destination):
        self.region_path = path_find(self.region, destination)

    def move(self):
        # Regular path inside the region (between locations)
        if self.path != None:
            next_lane = self.path.pop(0)
            print(self.path)
            self.location = locations[next_lane]
            print('i moved!, my loc now is' + ' ' + self.location.names['what'])
            return True

        # Discover-chan will never teleport from region to region unsless reaching hub-locations
        elif self.region_path > 0:
            next_lane = self.region_path[0]
            self.region_path.remove(0)
            self.region = next_lane
            print('i moved!, my region now is' + ' ' + self.region.names['what'])
            return True
        return False

    def routine_start(self):
        if self.goal == None:
            self.goal = goal_constructor(self)
        else:
            print('Routine wants to start, but previous routine is not finished! What the heck')
            pass


# Here Char can buy things.
class Shop():

    def __init__(self, locs=[], items=[]):
        self.locs = locs
        self.items = items

    def buy(self, who, item):
        if item in self.items:
            if who.money >= item.price:
                who.inventory.append(item)
            else:
                return False
        else:
            return False


night = ['night', [24, 7]]
morning = ['morning', [7, 12]]
noon = ['noon', [12, 14]]
afternoon = ['afternoon', [14, 19]]
evening = ['evening', [19, 24]]
worktime = ['work-time', [10, 16]]
breakfast = ['breakfast', [8, 9]]
lunch = ['lunch', [14, 15]]
dinner = ['dinner', [19, 20]]

work_day = [night, breakfast, morning, worktime, noon, lunch, afternoon, dinner, evening]
free_day = [night, breakfast, morning, noon, lunch, afternoon, dinner, evening]

work_days = [1, 2, 3]


# What time in terms of periods: night, day, etc
def discover_time(hour):
    print(Hour)
    if Day not in work_days:
        for time in free_day:
            num_time = time[1]
            if hour >= num_time[0] and hour < num_time[1]:
                nows = time
    else:
        for time in work_day:
            num_time = time[1]
            if hour >= num_time[0] and hour < num_time[1]:
                nows = time
    print('time V')
    print(nows)
    return nows


# def disover_time_int(time)


def normalize(text):
    # raw_input(text)
    text = text.split('. ')
    fintext = ''
    for part in text:
        # raw_input(part)
        parti = part[1].capitalize()
        fintext += parti
        fintext += part[2:len(part)]
        fintext.encode('utf-8')
        fintext += '. '
        # raw_input(fintext)
    # Because fuck you python+unicode and strings, that's why
    return fintext


# decide when the event Discover Chan talking about happened.


# construct new goal and return the goal
def goal_constructor(char):
    discvoer_timeObj = discover_time(datetime.now().hour)
    discover_hours = discvoer_timeObj[1]
    randomint = 20
    # randomint = random.randint(0,100)
    ##raw_input(randomint)
    # travel
    if randomint < 25:
        for loc in locations:
            if sceneryFlag in loc.flags:
                locgo = loc
        print('move' + str(locgo.loc_id))
        NewGoal = Goal(owner=char, inventory=None, money=None, location=locgo.loc_id)
    # collect
    elif randomint >= 25 and randomint <= 50:
        print('collect')
        NewGoal = Goal(owner=char, inventory=3, money=None, location=1)
    # earn
    elif randomint >= 50 and randomint <= 75:
        print('earn')
        NewGoal = Goal(owner=char, inventory=None, money=1000, location=1)
    # enjoy
    else:
        print('enjoy')
        NewGoal = Goal(owner=char, inventory=None, money=None, location=1, mood=100)
    # DummyGoal, just to start with smthing
    return NewGoal


# format: hours

# goal-creation based on the day timetable
def day_goal(char):
    time_now = discover_time(Hour)[0]
    for period in time_now:
        if period[0] == 'night':
            NewGoal = Goal(owner=char, inventory=None, money=None, location=1)
        if period[0] == 'worktime':
            NewGoal = Goal(owner=char, inventory=None, money=1000, location=1)
        if period[0] == 'evening':
            NewGoal = Goal(owner=char, inventory=None, money=None, location=1, mood=100)
        if period[0] == 'breakfast' or period[0] == 'lunch' or period[0] == 'dinner':
            NewGoal = Goal(owner=char, inventory=None, money=None, location=1, hunger=100)


class Goal():

    def __init__(self, owner=None, inventory=None, money=None, mood=None, location=None, specify=None, hunger=None):
        self.inventory = inventory
        self.money = money
        self.location = location
        self.mood = mood
        self.owner = owner
        self.specify = specify
        self.hunger = hunger
        self.achieved = False

    # evaluates approximate term to accomplish goal
    @property
    def Term(self):
        pass

    # Suggest character actions to accomplish goal
    def suggest_actions(self):
        suggestions = []

        if self.location:
            if self.owner.location.loc_id != self.location:
                suggestions.append('move')
                return suggestions

        if self.money:
            if self.money > self.owner.money:
                suggestions.append('earn')
                return suggestions

        if self.inventory:
            if Global_items[self.inventory] not in self.owner.inventory.items:
                suggestions.append('collect')
                return suggestions

        if self.mood:
            if self.owner.mood < self.mood:
                suggestions.append('enjoy')
                return suggestions

        if self.hunger:
            if self.owner.hunger < self.hunger:
                suggestions.append("eat")
                return suggestions

        if self.specify:
            suggestions.append(self.specify)
            return suggestions

        if suggestions == []:
            self.achieved = True


class Event():
    # But remember! Don't put string, but put numbers in these lists, so other
    # func would be able to create words\strings of proper forms\variations
    def __init__(self, date, flags, event_type, loc, verbs=[], adjectives=[], nouns=None):
        self.adjectives = adjectives
        self.date = date
        self.nouns = nouns
        self.loc = loc
        self.verbs = verbs
        self.flags = flags
        self.event_type = event_type
        self.time = discover_time(datetime.now().hour)


class Region():

    def __init__(self, reg_id, names={}, hubs=[], locations=[], connections=[], flags=[]):
        self.reg_id = reg_id
        self.names = names
        self.hubs = hubs
        self.locations = locations
        self.connections = connections


class Location():

    def __init__(self, loc_id, names={}, connections=[], flags=[]):
        self.loc_id = loc_id
        self.names = names
        self.connections = connections
        self.flags = flags

    @property
    def shop(self):
        for shop in shops:
            if self.loc_id in shop.locs:
                return shop
        return False


class Connection():

    def __init__(self, origin, dest):
        self.origin = origin
        self.dest = dest


class Item():

    def __init__(self, name, price, flags):
        self.name = name
        self.price = price
        self.flags = flags
        self.id = get_id(Global_items, self)


class Flag_Component():

    def __init__(self, adjectives=[], verbs=[[], [], []], verbs_self=None, pronoun=['mine', 'my own']):
        self.adjectives = adjectives
        self.verbs = verbs
        self.verb = None
        self.pronoun = pronoun


compGeneralBuy = Flag_Component(
    adjectives=['affordable', 'pricy', 'cheap', 'common', 'democratic-priced', 'unexpensive', 'low-cost'],

    verbs=[
        ['buy', 'get', 'collect', 'purchase', 'obtain', 'acquire'],
        ['bought', 'got', 'collected', 'purchased', 'obtained', 'acquired'],
        ['buying', 'geting', 'collecting', 'purchasing', 'obtaining', 'acquiring']])

compGeneralVisGood = Flag_Component(
    adjectives=['pretty', 'beautiful', 'breathtaking', 'enourmous', 'wonderful', 'pleasant', 'lovely', 'fetching'],

    verbs=[
        ['see', 'observe', 'watch', 'examine'],
        ['saw', 'observed', 'watched', 'examined'],
        ['seeing', 'observing', 'watching', 'examinating']],

    verbs_self=[
        ['stand', 'stay', 'sit'],
        ['standing', 'staying', 'sitting'],
        ['stood', 'stayed', 'sat']
    ])

compGeneralInt = Flag_Component(
    adjectives=['interesting', 'outstanding', 'original', 'originative'],
    verbs=[
        ['interact with', 'use', 'caress', 'operate', 'manipulate'],
        ['interacted with', 'used', 'caressed', 'operated', 'manipulated'],
        ['interacting with', 'using', 'caressing', 'operating', 'manipulating']
    ]
)

compGeneralVisBad = Flag_Component(
    adjectives=['negative', 'bad-looking', 'horrible', 'disgusting', 'terrible', 'horrific'],

    verbs=[
        ['see', 'observe', 'watch', 'examine', 'mark'],
        ['saw', 'observed', 'watched', 'examined', 'marked'],
        ['seeing', 'observing', 'watching', 'examinating', 'marking']
    ]
)

compDangerous = Flag_Component(
    adjectives=['dangerous', 'menacing', 'hazardous', 'unsafe', 'precarious'],
    verbs=[
        ['avoid', 'ignore', 'stay away from', 'refrain from'],
        ['avoided', 'ignored', 'stayed away from', 'refrain from'],
        ['avoiding', 'ignoring', 'staying away from', 'refraining from']
    ]
)

compClothesGood = Flag_Component(
    adjectives=['fit', 'comfortable', 'long-enough', 'durable', 'casual', 'fine', 'fitting', 'nice-looking'],
    verbs=[
        ['wear', 'examine', 'check'],
        ['wore', 'examined', 'checked'],
        ['wearing', 'examining', 'checking']
    ]
)

compClothesDirty = Flag_Component(
    adjectives=['dirty', 'muddy', 'messy', 'smelly', 'filthy', 'nasty', 'scruffy', 'mucky'],
    verbs=[
        ['wear', 'examine', 'fix'],
        ['wore', 'examined', 'fixed'],
        ['wearing', 'examining', 'fixing']
    ]
)

compShoes = Flag_Component(
    adjectives=['fit', 'membran', 'touristic', 'hiking', 'travel', 'waterproof', 'polyester'],
    verbs=[
        ['wear', 'examine', 'check'],
        ['wore', 'examined', 'checked'],
        ['wearing', 'examining', 'checking out']
    ]
)

compSelf = Flag_Component(
    adjectives=['good', 'loveable'],
    verbs=[
        ['cherish', 'love', 'enjoy', 'keep', 'preserve', 'retain'],
        ['cherished', 'loved', 'enjoyed', 'kept', 'preserved', 'retained'],
        ['cherishing', 'loving', 'enjoying', 'keeping', 'preserving', 'retaining']
    ]
)

compOutside = Flag_Component(
    adjectives=['gorgeous', 'hustly', 'busy', 'silent', 'peaceful', 'happy'],
    verbs=[
        ['spectate', 'pass through', 'walk through'],
        ['spectated', 'passed through', 'walked through'],
        ['spectating', 'passing through', 'walking through']
    ]
)

compSitting = Flag_Component(
    adjectives=['comfortable', 'cosy', 'plushy', 'soft', 'comfy'],
    verbs=[
        ['sit on', 'relax on', 'lay down on'],
        ['sat on', 'relaxed on', 'straddled on'],
        ['sitting on', 'relaxing on', 'straddling on']
    ]
)

compMoving = Flag_Component(
    adjectives=['quick', 'slow', 'fast', 'rapid'],
    verbs=[
        ['move to', 'walk to', 'go to'],
        ['moved to', 'walked  to', 'gone to'],
        ['moving on', 'walking to', 'going to']
    ]
)

compGoodTaste = Flag_Component(
    adjectives=['tasty', 'delicious', 'flavourous', 'yummy', 'lush', 'luscious'],
    verbs=[
        ['eat', 'yum', 'consume', 'devour', 'ingest'],
        ['ate', 'yumed', 'consumed', 'devoured', 'ingested'],
        ['eating', 'yumming', 'consuming', 'devouring', 'ingesting']
    ]
)

compOkTaste = Flag_Component(
    adjectives=['ok', 'edible', 'consumable', ],
    verbs=[
        ['eat', 'yum', 'consume', 'devour', 'ingest'],
        ['ate', 'yumed', 'consumed', 'devoured', 'ingested'],
        ['eating', 'yumming', 'consuming', 'devouring', 'ingesting']
    ]
)

compBadTaste = Flag_Component(
    adjectives=['horrible', 'unsavory', 'distasteful', 'unpatable', 'unconsumable', ],
    verbs=[
        ['shovel', 'jam', 'consume', 'devour', 'ingest'],
        ['shoveled', 'jammed', 'consumed', 'devoured', 'ingested'],
        ['shoveling', 'jaming', 'consuming', 'devouring', 'ingesting']
    ]
)


##def associate(string):
##    list = string.split(' ')
##    for string in list:
##        if len(string)>2:
##            for flag in all_flags:
##                for component in flag.flag_components:
##                    for adjective in component.adjectives:
##                        if adjective.find(string) is not -1 :
##                            #raw_input(adjective+' is something with '+ string)
##
##                    for verb_list in  component.verbs:
##                        for verb in verb_list:
##                             if verb.find(string) is not -1 :
##                                 if not flag.nouns:
##                                    #raw_input('things you can:'+ string+', you can describe with the word:'+random.choice(component.adjectives))
##                                 else:
##                                    #raw_input(random.choice(flag.nouns)+' you can:'+ string+', you can describe with the word:'+random.choice(component.adjectives))
##                if flag.nouns:
##                    for noun in flag.nouns:
##                        if noun.find(string) is not -1:
##                            #raw_input('noun')

class Flag():

    def __init__(self, flag_components=[], nouns=None, plural=False):
        self.flag_components = flag_components
        self.nouns = nouns
        self.flag_adjectives
        # infinitive
        self.flag_verb_inf
        # verbs 1-Present 2-Past 3-Future 4-Infinitive
        self.flag_verbs
        self.plural = plural
        all_flags.append(self)

    @property
    def flag_adjectives(self):
        self.flag_adjectives = []

        for comp in self.flag_components:
            for word in comp.adjectives:
                self.flag_adjectives.append(word)
        return self.flag_adjectives

    @property
    def flag_verbs(self, ):
        self.flag_verbs = []
        x = 0
        for comp in self.flag_components:
            while x < len(comp.verbs) - 1:
                self.flag_verbs.append(comp.verbs[x])
                x += 1
        present = self.flag_verbs[1]
        # print(present[1].decode('utf-8'))
        return self.flag_verbs

    @property
    def flag_verb_inf(self):
        self.flag_verb_inf = []
        for comp in self.flag_components:
            for word in comp.verbs[2]:
                self.flag_verb_inf.append(word)
        return self.flag_verb_inf

    # Remember! This is your world.
    # It's up to you to decide these little things. Just let all these little things happen.
    @property
    def flag_verbs_self(self):
        self.flag_verbs_self = []

        for comp in self.flag_components:
            for group in comp.self_verbs():
                for verb in group:
                    self.flag_verbs_self.append(verb)
        if self.flag_verbs_self != []:
            return self.flag_verbs_self
        else:
            return False


class Inventory():

    def __init__(self, items=[]):
        self.items = []

    def add(self, item):
        self.items.append(item)
        return len(self.items)

    def search_flags(self, flags=[]):
        list_return = list_return()
        for item in self.items:
            for flag in flags:
                if flag in item.flags:
                    if item not in list_return():
                        list_return.append(item)
                elif item in list_return:
                    list_return.remove(item)
        return list_return


homefurniture_Flag = Flag(flag_components=[compGeneralVisGood, compGeneralInt, compSelf],
                          nouns=['sofa', 'chair', 'computer', 'tv', 'window', 'armchair', 'wardrobe', 'bed', 'table'])
sittingfurniture_Flag = Flag(flag_components=[compGeneralVisGood, compGeneralInt, compSitting],
                             nouns=['sofa', 'chair', 'armchair', 'bed'])

##Name = None because item's name itself can count as a noun!!!!!
owneditems_Flag = Flag(flag_components=[compSelf, compClothesGood], nouns=None, plural=False)
gooditems_Flag = Flag(flag_components=[compClothesGood], nouns=None, plural=True)
pluralowneditems_Flag = Flag(flag_components=[compSelf, compClothesGood], nouns=None, plural=True)
shoes_Flag = Flag(flag_components=[compSelf, compShoes], nouns=None, plural=False)
productFlag = Flag(flag_components=[compGeneralBuy], nouns=['item', 'thing', 'merchandise', 'ware'], plural=False)
tasty_food = Flag(flag_components=[compGeneralVisGood, compGoodTaste], nouns=['food', 'nutrition'], plural=False)
nasty_food = Flag(flag_components=[compBadTaste, compOkTaste, compGeneralVisBad],
                  nouns=['food', 'edible', 'ration', 'dish'], plural=False);

yardnatureflag = Flag(flag_components=[compGeneralVisGood, compGeneralInt],
                      nouns=['trees', 'cats', 'flowers', 'birds', 'leaves', 'rats', 'bugs', 'dogs', 'bushes',
                             'grassies'], plural=True)
sceneryFlag = Flag(flag_components=[compGeneralVisGood],
                   nouns=['mountain ranges', 'mountains', 'crests', 'woods', 'valleys', 'creeks', 'views', 'sceneries',
                          'pictures', 'landscapes', 'mountain villages', 'summits', 'tops', 'cliffs'], plural=True)
moveflag = Flag(flag_components=[compMoving], nouns=None, plural=False);

DiscoverJacket = Item(name='soft-shell jacket', price=0, flags=[owneditems_Flag]);
DiscoverPants = Item(name='sport legwear', price=0, flags=[owneditems_Flag]);
DiscoverShoes = Item(name='chinese sneakers', price=0, flags=[pluralowneditems_Flag, shoes_Flag]);

StringsPanties = Item(name='panties', price=100, flags=[gooditems_Flag]);
Disinventory = Inventory()
Disinventory.add(DiscoverJacket)
Disinventory.add(DiscoverPants)
Disinventory.add(DiscoverShoes)

HomeReg = Region(0, names={'what': 'Uzhhorod', 'where': 'in Uzhhorod'}, hubs=[], locations=[0, 1, 2], connections=[],
                 flags=[]);
HomeLoc = Location(0, names={'what': 'my flat', 'where': 'in my flat'}, connections=[1],
                   flags=[homefurniture_Flag, sittingfurniture_Flag])
NeighbourHood = Location(1, names={'what': 'my yard', 'where': 'in my yard'}, connections=[0, 2],
                         flags=[yardnatureflag]);
PlishkaLoc = Location(2, names={'what': 'Plishka', 'where': 'at the Plishka'}, connections=[1],
                      flags=[yardnatureflag, sceneryFlag]);

Regular_Shop = Shop([1], [3, 4]);

shops = [Regular_Shop]
locations = [HomeLoc, NeighbourHood, PlishkaLoc];

adverbs_before = ['yesterday', 'before', 'recently', 'once', 'then'];
adverb_future = ['tommorow', 'next', 'somwhen', 'in the future'];
adverb_here = ['here'];
adverb_there = ['there'];
adverb_nowhere = ['nowhere', 'elsewhere', 'somewhere'];

linking_words = ['however', 'also', 'moreover', 'in addition'];

opinions = ['right as i think', 'as i think', 'imho', ' in my opinion', 'as i see'];

sequenceobs1 = ['$verb', '$noun', ', and ', '%opinion', '%pronoun', '%tobe', '%adjective'];
sequenceobs2 = ['%link', '$verb', '$noun', '%timeword', 'and', '%link', '%pronoun', '%tobe', '%adjective'];
sequenceobs3 = ['%link', '$verb', '$noun', '%timeword', '%location_w', '%link', '%pronoun', '%tobe', '%adjective'];
sequenceobs4 = ['$verb', '%adjective', '$noun', 'because', '%pronoun', '%tobe', '%adjective'];

observation_sequences = [sequenceobs1, sequenceobs2, sequenceobs3, sequenceobs4];

sequencemove1 = ['$verb', '%location'];
move_sequences = [sequencemove1];
times = ['present simple', 'present continious', 'present perfect', 'past simple', 'past perfect', 'past continious'];


class Story():

    def __init__(self, owner, events, time):
        self.owner = owner
        self.events = events
        self.time = time

    def decide_time(self):
        time_now = discover_time(Hour)
        earliest = 0
        latest = 0
        for event in self.events:
            event_num = self.events.index(event)
            print(event.flags)
            event_hours = event.time[1]
            if event_hours[1] < earliest:
                earliest = event_hours[1]
            elif event_hours[0] > latest:
                latest = event_hours[0]

        get_time()

        if Hour - latest < 2:
            return "present perfect"
        else:
            return "past simple"

    def construct(self, construct_event):
        linked = 0
        message = ''
        flag = random.choice(construct_event.flags)
        # print(flag)
        comp = random.choice(flag.flag_components)
        verb = random.choice(construct_event.verbs)
        # print(construct_event.verbs)
        # print(verb)
        nouns = construct_event.nouns
        Iam = False
        print(self.time)
        if construct_event.event_type == 'observation':
            sequence = random.choice(observation_sequences)
            index = 0
        elif construct_event.event_type == 'observation_item':
            sequence = random.choice(observation_sequences)
            index = 0
        elif construct_event.event_type == 'moving':
            sequence = random.choice(move_sequences)
            index = 0
        else:
            sequence = random.choice(observation_sequences)
            index = 0
        for part in sequence:
            index += 1
            # So we can link   sequences
            if index == 1 and part != 'I':
                message += ' i '
                Iam = True
            if part.lower() == 'i':
                Iam = True
            if part == '$verb':
                print('debug: verb construction')
                ##raw_input(verb)
                if self.time == 'present simple':
                    print('debug: present')
                    verb = construct_present_simple(flag, comp, verb)
                elif self.time == 'present continious':
                    verb = construct_present_continious(flag, comp, verb, Iam)
                elif self.time == 'present perfect':
                    verb = construct_present_perfect(flag, comp, verb)
                elif self.time == 'past simple':
                    verb = construct_past_simple(flag, comp, verb)
                elif self.time == 'past continious':
                    verb = construct_past_continious(flag, comp, verb)
                elif self.time == 'past perfect':
                    verb = construct_past_perfect(flag, comp, verb)
                print(verb + 'verb')
                message += ' ' + verb
            elif part == '$noun':
                if nouns == None:
                    if flag.nouns != None:
                        message += ' ' + random.choice(flag.nouns)
                    else:
                        message += 'I '
                else:
                    ##raw_input(nouns)
                    message += ' ' + random.choice(nouns)
            elif part == '%tobe':
                tobe = ''
                if not flag.plural:
                    if self.time == 'present simple':
                        tobe = 'is'
                    elif self.time == 'present continious':
                        tobe = 'is'
                    elif self.time == 'present perfect':
                        tobe = 'was'
                    elif self.time == 'past simple':
                        tobe = 'was'
                    elif self.time == 'past continious':
                        tobe = 'was'
                    elif self.time == 'past perfect':
                        tobe = 'was'
                    message += ' ' + tobe
                else:
                    if self.time == 'present simple':
                        tobe = 'are'
                    elif self.time == 'present continious':
                        tobe = 'are'
                    elif self.time == 'present perfect':
                        tobe = 'were'
                    elif self.time == 'past simple':
                        tobe = 'were'
                    elif self.time == 'past continious':
                        tobe = 'were'
                    elif self.time == 'past perfect':
                        tobe = 'were'
                    message += ' ' + tobe

            elif part == '%adjective':
                adj = random.choice(comp.adjectives)
                message += ' ' + adj

            elif part == '%pronoun':
                Iam = False

                if flag.plural == True:
                    pron = ' they'
                else:
                    pron = 'it'
                message += ' ' + pron

            elif part == '%opinion':
                pron = random.choice(opinions)
                message += ' ' + pron
            elif part == '%location_w':
                loc = construct_event.loc.names['where']
                message += ' ' + loc
            elif part == '%location':
                loc = construct_event.loc.names['what']
                message += ' ' + loc
            elif part == '%link' and linked == 0:
                if random.randint(0, 4) == 1:
                    link = random.choice(linking_words)
                    if not index == 0:
                        message += ', ' + link + ', '
                    else:
                        message += link + ','
                    linked = 1

            elif '%' not in part:
                message += ' ' + part
        print(message)
        return message


def tell_location(location):
    loc = location
    flag = random.choice(loc.flags)
    if flag.nouns is not None:
        noun = random.choice(flag.nouns)
    else:
        noun = loc.names['what']
    verb = random.choice(flag.flag_verbs)
    verb = random.choice(verb)
    text = 'I ' + verb
    text = text + ' ' + random.choice(flag.flag_adjectives)
    text = text + ' ' + noun + '.'

    text = text.split('. ')

    fintext = ''
    for i in text:
        i = unicode(i, 'utf-8').lower().capitalize() + '. '
        fintext += i

    # Because fuck you python+unicode and strings, that's why
    fintext = fintext[0:len(fintext) - 2]
    fintext.encode('utf-8')
    return fintext


def construct_present_simple(flag, flag_component, verb):
    construction = ''
    verb_list = flag_component.verbs[0]
    # print(verb_list)
    verb = verb_list[verb]
    construction = construction + '' + verb
    # print(construction)
    return construction


def construct_present_continious(flag, flag_component, verb, iam=False):
    construction = ''
    if flag.plural == False:
        if not iam:
            construction = ' is'
        else:
            construction = 'am'
    else:
        if not iam:
            construction = ' are'
        else:
            construction = 'am'
    verb_list = flag_component.verbs[2]

    # print(verb_list)
    # print(verb)
    verb = verb_list[verb]
    construction = construction + ' ' + verb
    # print(construction)
    return construction


# for something that started in the past and continues in the present:
# for something we have done several times in the past and continue to do:
# when we are talking about our experience up to the present:


def construct_present_perfect(flag, flag_component, verb, what='I', repeat=False):
    construction = ''
    verbs_list = flag_component.verbs
    verb = verb

    if what == 'I' or what == 'They':
        if repeat == False:
            verbs_list = flag_component.verbs[1]
            verb = verb
            # print(verbs_list)
            construction += "have " + verbs_list[verb]
            return construction
        else:
            verbs_list = flag_component.verbs[2]
            verb = verb
            construction += "have been " + verbs_list[verb]
        # print(construction)
        return construction

    if what == 'third':

        if repeat == False:
            verbs_list = flag_component.verbs[1]
            verb = verb
            construction += "has " + verbs_list[verb]
            return construction
        else:
            verbs_list = flag_component.verbs[2]
            verb = verb
            construction += "has been " + verbs_list[verb]
        # print(construction)
        return construction


def construct_past_simple(flag, flag_component, verb):
    verbs_list = flag_component.verbs[1]
    verb = verb
    construction = ''
    print(verbs_list)
    construction += verbs_list[verb]
    # print(construction)
    return construction


def construct_past_continious(flag, flag_component, verb):
    verbs_list = flag_component.verbs[2]
    verb = verb
    construction = ''
    if flag.plural == False:
        construction = 'was'
    else:
        construction = 'were'
    construction += ' ' + verbs_list[verb]
    # print(construction)
    return construction


def construct_past_continious(flag, flag_component, verb):
    verbs_list = flag_component.verbs[2]
    verb = verb
    construction = ''
    if flag.plural == False:
        construction = 'was'
    else:
        construction = 'were'
    construction += ' ' + verbs_list[verb]
    ##print(construction)
    return construction


def construct_past_perfect(flag, flag_component, verb):
    verbs_list = flag_component.verbs[2]
    verb = verb
    construction = 'had been '
    # print(verbs_list)
    construction += ' ' + verbs_list[verb]
    # print(construction+'aaaa')
    return construction


def path_find(origin, dest, global_list=locations):
    # Global list is the pool of structures
    # print(global_list)
    if origin == dest:
        return None
    origin = global_list[origin]
    dest = global_list[dest]
    print('>>>>>>>>>>')
    print(origin.loc_id)
    print(dest.loc_id)
    print('>>>>>>>>>>')

    open_locs = [origin]
    closed_locs = []
    path = []
    cur = origin

    for j in open_locs:
        print(j.loc_id)
        if j not in closed_locs:
            closed_locs.append(j)
            for i in j.connections:
                if i not in closed_locs:
                    if j == dest:
                        closed_locs.append(j)
                        break
                    open_locs.append(global_list[i])

    print(dest)
    cur = dest
    path.append(cur.loc_id)
    while cur != origin:

        for j in cur.connections:

            print('<><><>')
            for loc in open_locs:
                print(loc.loc_id)
            print('<><><>')
            if global_list[j] in closed_locs:
                print(dest.loc_id)
                print(origin.loc_id)

                cur = global_list[j]
                path.append(global_list[j].loc_id)
                if j == origin.loc_id:
                    print('PAAAATH')
                    path.reverse()
                    for loc in path:
                        print(loc)
                    print('^-path')
                    break
    return path


def test_event_constructor(locations):
    location_event = random.choice(locations)
    flags = []
    verbs_f = []
    adjectives_f = []
    for i in location_event.flags:
        flags.append(i)
        # print(i.flag_components)
    for flag in flags:
        for comp in flag.flag_components:
            for verb in range(0, len(comp.verbs)):
                # print(flag.flag_components)
                verbs_f.append(verb)
            for adj in range(0, len(comp.adjectives)):
                adjectives_f.append(adj)
    event_dummy = Event(0, flags, event_type='observation', verbs=verbs_f, adjectives=adjectives_f, loc=location_event)
    return event_dummy


def test_event_constructor_item(item):
    flags = []
    verbs_f = []
    adjectives_f = []

    for i in item.flags:
        flags.append(i)
        # print(i.flag_components)
    for flag in flags:
        for comp in flag.flag_components:
            # print(comp.verbs)
            for verb in range(0, len(comp.verbs)):
                # print(flag.flag_components)
                verbs_f.append(verb)
            for adj in range(0, len(comp.adjectives)):
                adjectives_f.append(adj)
    event_dummy = Event(0, flags=flags, event_type='observation_item', verbs=verbs_f, adjectives=adjectives_f,
                        nouns=[item.name], loc=None)
    return event_dummy


def get_time():
    global Hour, Minute, Day
    nowtime = datetime.now()
    Hour = nowtime.hour
    # raw_input(Hour)
    Minute = nowtime.minute
    Day = nowtime.today().weekday()


def main():
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    # (self,date,flags,event_type,verbs=[],adjectives=[],nouns=[]


##    for i in range(0,5):
##      event_dummy =test_event_constructoritem(random.choice(Disinventory.items))
##     # test_event_constructor(locations)
##      event_dummy.loc=discover.location
##    #,owner,event,time)
##      story_dummy = Story(owner = discover,events = [event_dummy] ,time=random.choice(times))
##      story_dummy.construct(story_dummy.events[0])
# associate(##raw_input())
##
##     print(tell_location(discover.location))
##    pass
##

def init():
    get_time()
    discover_time(Hour)
    discover = Character(100, 2500, HomeLoc, Disinventory, 100, 50)
    discover.routine_start()


if __name__ == '__main__':
    discover = Character(100, 2500, HomeLoc, Disinventory, 100, 50)
    discover.routine_start()
    discover.goal_processing()
    discover.goal_processing()
    discover.goal_processing()
    discover.rethink_events()
    main()
