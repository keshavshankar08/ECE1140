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
        ##TODO Make red and green trains different
        self.current_block = -1 # the head of the train's current block
        self.current_authority_changed = False # indicates when authority has been changed by wayside
        #^^ authority is minus changed value
        self.authority_reset_ready = False # indicates when ctc should reset trains authority
        self.current_direction = False # false = southbound, true = northbound
        self.current_line = line # 0 = red, 1 = green
        self.stop_index = 0 # stop that the train is at
        self.authority_stop_queue = [] # make a list of the route

        #set train ID
        self.train_ID = str(next(Train.id_obj))
        while(len(self.train_ID) != 4):
            self.train_ID = "0" + self.train_ID

        #create track/line object to call function from
        track = Track()

        #get all stops in block number form
        if line == 0:
            block_stops = track.red_line_station_to_block(route.stops)
        elif line == 1:
            block_stops = track.green_line_station_to_block(route.stops)
        
        #make the authority list
        self.authority_stop_queue.append([0])

        #get the left path for red and green lines
        if self.current_line == 0:
            for i in range(len(route.stops)):
                #if it's the last stop, return to yard at -1
                if(i == 0):
                    #for first stop, get authority from yard **[1:] removes first element (previous stop)
                    self.authority_stop_queue.append(track.lines[0].get_left_path(0, block_stops[i]))
                else:
                    #otherwise, get the length of the shortest path between the stops **[1:] removes first element (previous stop)
                    self.authority_stop_queue.append(track.lines[0].get_left_path(block_stops[i-1], block_stops[i]))

            #set authority to go back to the yard
            self.authority_stop_queue.append(track.lines[0].get_left_path(block_stops[len(block_stops)-1], 0))

        elif self.current_line == 1:
            for i in range(len(route.stops)):
                #if it's the last stop, return to yard at -1
                if(i == 0):
                    #for first stop, get authority from yard **[1:] removes first element (previous stop)
                    self.authority_stop_queue.append(track.lines[1].get_left_path(0, block_stops[i]))
                else:
                    #otherwise, get the length of the shortest path between the stops **[1:] removes first element (previous stop)
                    self.authority_stop_queue.append(track.lines[1].get_left_path(block_stops[i-1], block_stops[i]))


            #set authority to go back to the yard
            self.authority_stop_queue.append(track.lines[1].get_left_path(block_stops[len(block_stops)-1], 0))

        #the suggested speed inbetween each station
        self.suggested_speed_list = [20] * len(self.authority_stop_queue)
        self.suggested_speed_list[0] = 0

        #set the current parameters
        self.current_authority = 0
        self.current_suggested_speed = self.suggested_speed_list[self.stop_index]
        self.current_authority_stop_queue = self.authority_stop_queue[self.stop_index]
        
        #set departure time
        self.departure_time = QTime.fromString(route.stop_time[0], "hh:mm:ss")
        if line == 0:
            time_between = track.red_line.get_time_between(0, route.stops[0])
            self.departure_time = self.departure_time.addSecs(time_between * -1).toString()

        elif line == 1:
            time_between = track.green_line.get_time_between(0, route.stops[0])
            self.departure_time = self.departure_time.addSecs(time_between * -1).toString()

        else:
            self.departure_time = "0"

        print(self.authority_stop_queue)

    #function to get the train to the next stop
    def next_stop(self):
        #iterate the stop index by 1
        self.stop_index += 1

        #update the current authority and speed
        self.current_authority = len(self.authority_stop_queue[self.stop_index])
        self.current_suggested_speed = self.suggested_speed_list[self.stop_index]
        self.current_authority_stop_queue = self.authority_stop_queue[self.stop_index]

    def update_authority(self, track):
        #first check if if the list is empty
        if len(self.authority_stop_queue[self.stop_index]) == 0:
            return

        if(self.current_line == 0):
            #if the first block is occupied, remove it from the route
            if track.red_line.blocks[self.authority_stop_queue[self.stop_index][0]].block_occupancy == True:
                self.authority_stop_queue[self.stop_index] = self.authority_stop_queue[self.stop_index][1:]

        if(self.current_line == 1):
            #if the first block is occupied, remove it from the route
            if track.green_line.blocks[self.authority_stop_queue[self.stop_index][0]].block_occupancy == True:
                self.authority_stop_queue[self.stop_index] = self.authority_stop_queue[self.stop_index][1:]
                
        #update current block
        self.current_block = self.authority_stop_queue[self.stop_index][0]

        #update current direction for each possible line
        if(self.current_line == 0):
            if(self.current_block == 66):
                self.current_direction = not self.current_direction
            if(self.current_block == 10):
                self.current_direction = not self.current_direction
        if(self.current_line == 1):
            if(self.current_block == 100):
                self.current_direction = not self.current_direction
            if(self.current_block == 1):
                self.current_direction = not self.current_direction

        #update current authority
        self.current_authority = len(self.authority_stop_queue[self.stop_index])

        print(f'Authority: ',self.current_authority,'\nCurrent Block:',self.current_block,'\nCurrent Direction: ',self.current_direction)

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