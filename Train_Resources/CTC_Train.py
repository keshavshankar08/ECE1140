#CTC_Train.py

import sys
import itertools
sys.path.append(".")
from Track_Resources.Track import *

class Route:
    def __init__(self):
        #create a container
        self.stops = []
        self.stop_time = []
        self.dwell_time = []

class RouteQueue:
    def __init__(self):
        self.routes: list[Route] = []

    def add_route(self, add_route):
        self.routes.append(add_route)

    def remove_route(self, remove_route_index):
        self.routes.pop(remove_route_index)

class Train:
    #keep train IDs
    id_obj = itertools.count()

    def __init__(self, route):
        #set train ID
        self.train_ID = str(next(Train.id_obj))
        while(len(self.train_ID) != 4):
            self.train_ID = "0" + self.train_ID
        
        #make a list of all authorities
        self.authority_list = []

        #create track/line object to call function from
        track = Track()
        
        block_stops = track.red_line_station_to_block(route.stops)
        print(block_stops)
        
        for i in range(len(route.stops)):
            #if it's the last stop, return to yard at -1
            if(i == (len(route.stops) - 1)):
                self.authority_list.append(-1)
                print(self.authority_list)

            else:
                #otherwise, get the length of the shortest path between the stops
                self.authority_list.append(len(track.lines[0].get_shortest_path(block_stops[i], block_stops[i+1], [])))
                print(self.authority_list)

        #the current authority
        self.current_authority = 0

        #the suggested speed inbetween each station
        self.suggested_speed_list = [20] * len(self.authority_list)

        #the current suggested speed
        self.current_suggested_speed = 0
        
        self.departure_time = ""

class ActiveTrains:
    def __init__(self):
        self.active_trains: list[Train] = []

    def add_train(self, add_train):
        self.active_trains.append(add_train)

    def remove_train(self, remove_train_index):
        self.active_trains.pop(remove_train_index)

class QueueTrains:
    def __init__(self):
        self.queue_trains: list[Train] = []

    def add_train(self, add_train):
        self.queue_trains.append(add_train)

    def remove_train(self, remove_train_index):
        self.queue_trains.pop(remove_train_index)
