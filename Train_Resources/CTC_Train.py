#CTC_Train.py

import sys
import itertools
from PyQt6.QtCore import QTime
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

    def __init__(self, route, line):
        #set train ID
        self.train_ID = str(next(Train.id_obj))
        while(len(self.train_ID) != 4):
            self.train_ID = "0" + self.train_ID
        
        #make a list of all authorities
        self.authority_list = []

        #create track/line object to call function from
        track = Track()
        
        #get all stops in block number form
        if line == "Red":
            block_stops = track.red_line_station_to_block(route.stops)
        elif line == "Green":
            block_stops = track.green_line_station_to_block(route.stops)
        
        #make the authority list
        self.authority_list.append(0)
        for i in range(len(route.stops)):
            #if it's the last stop, return to yard at -1
            if(i == 0):
                #for first stop, get authority from yard
                self.authority_list.append(len(track.lines[0].get_shortest_path(0, block_stops[i], [])))
            else:
                #otherwise, get the length of the shortest path between the stops
                self.authority_list.append(len(track.lines[0].get_shortest_path(block_stops[i-1], block_stops[i], [])))

            #set authority to go back to the yard
            self.authority_list.append(-1)

        #the suggested speed inbetween each station
        self.suggested_speed_list = [20] * len(self.authority_list)
        self.suggested_speed_list[0] = 0

        self.stop_index = 0

        #set the current authority
        self.current_authority = self.authority_list[self.stop_index]

        #the current suggested speed
        self.current_suggested_speed = self.suggested_speed_list[self.stop_index]
        
        #set departure time
        self.departure_time = QTime.fromString(route.stop_time[0], "hh:mm:ss")
        if line == "Red":
            time_between = track.red_line.get_time_between(0, route.stops[0])
            self.departure_time = self.departure_time.addSecs(time_between * -1).toString()

        elif line == "Green":
            time_between = track.green_line.get_time_between(0, route.stops[0])
            self.departure_time = self.departure_time.addSecs(time_between * -1).toString()

        else:
            self.departure_time = "0"

    #function to get the train to the next stop
    def next_stop(self):
        #iterate the stop index by 1
        self.stop_index += 1

        #update the current authority and speed
        self.current_authority = self.authority_list[self.stop_index]
        self.current_suggested_speed = self.suggested_speed_list[self.stop_index]

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
