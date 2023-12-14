#CTC_Train.py

import sys
import itertools
import copy
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
        self.train_route = route
        self.station_departure_time = QTime()
        self.distance_from_yard = -1
        self.passenger_count = 0

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
                    first_authority = track.lines[0].get_left_path(0, block_stops[i])
                    self.authority_stop_queue.append([0] + first_authority)
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
                    first_authority = track.lines[1].get_left_path(0, block_stops[i])
                    self.authority_stop_queue.append([0] + first_authority)
                else:
                    #otherwise, get the length of the shortest path between the stops **[1:] removes first element (previous stop)
                    self.authority_stop_queue.append(track.lines[1].get_left_path(block_stops[i-1], block_stops[i]))

            #set authority to go back to the yard
            self.authority_stop_queue.append(track.lines[1].get_left_path(block_stops[len(block_stops)-1], 0))

        #the suggested speed inbetween each station
        self.suggested_speed_queue = copy.deepcopy(self.authority_stop_queue)
        for i, speed in enumerate(self.suggested_speed_queue):
            for j in range(len(speed)):
                if(j == len(speed)-1):
                    speed[j] = 0
                else:
                    if(self.current_line == 0):
                        if(j == len(speed)-2):
                            speed[j] = 10
                        elif(j == len(speed)-3):
                            speed[j] = 15
                        else:
                            speed[j] = track.red_line_speed_limit[self.authority_stop_queue[i][j]]
                    if(self.current_line == 1):
                        if(j == len(speed) - 2):
                            speed[j] = 10
                        elif(j == len(speed)-3):
                            speed[j] = 15
                        else:
                            speed[j] = track.green_line_speed_limit[self.authority_stop_queue[i][j]]

        #set the current parameters
        self.current_authority = 0
        self.current_suggested_speed = 0
        self.current_suggested_speed_stop_queue = self.suggested_speed_queue[self.stop_index]
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
        print(self.suggested_speed_queue)

    #function to get the train to the next stop
    def next_stop(self):
        #iterate the stop index by 1
        self.stop_index += 1

        #update the current authority and speed
        self.current_authority = len(self.authority_stop_queue[self.stop_index])
        self.current_suggested_speed = self.suggested_speed_queue[self.stop_index][0]
        self.current_suggested_speed_stop_queue = self.suggested_speed_queue[self.stop_index]
        self.current_authority_stop_queue = self.authority_stop_queue[self.stop_index]

    #function to check if a train is at a station stop
    def station_stop(self):
        #the train is at a station block, return true
        #and (self.current_suggested_speed == 0)
        if((self.current_authority == 0)):
            return True
        
    #function that will use dwell time, then go to the next stop
    def update_stop(self, system_time):
        #get system time in readable format
        system_time_comp = QTime.fromString(system_time.toString("hh:mm:ss"), "hh:mm:ss")

        #if the index is 0, exit function
        if(self.stop_index == 0):
            return

        #if the train is stopped and time equals station
        if(self.current_authority == -1):
            if(system_time_comp == self.station_departure_time):
                self.next_stop()

        #if station is a stop, set departure time and make authority 0
        if(self.station_stop() == True):
            #get dwell time
            dwell = QTime.fromString(self.train_route.dwell_time[self.stop_index-1], "m:ss")
            dwell_secs = QTime(0,0).secsTo(dwell)

            #get next departure time
            self.station_departure_time = system_time_comp.addSecs(dwell_secs)

            #set authority to -1 to avoid updating again
            self.current_authority = -1

    def update_authority(self, track):
        #first check if if the list is empty
        if len(self.authority_stop_queue[self.stop_index]) == 0:
            return
        
        if(self.current_line == 0):
            #if the first block is occupied, remove it from the route
            if track.red_line.blocks[self.authority_stop_queue[self.stop_index][0]].block_occupancy == True:
                #update current block
                self.current_block = self.authority_stop_queue[self.stop_index][0]
                self.authority_stop_queue[self.stop_index] = self.authority_stop_queue[self.stop_index][1:]
                #update current speed
                self.current_suggested_speed = self.suggested_speed_queue[self.stop_index][0]
                self.suggested_speed_queue[self.stop_index] = self.suggested_speed_queue[self.stop_index][1:]

        if(self.current_line == 1):
            #if the first block is occupied, remove it from the route
            if track.green_line.blocks[self.authority_stop_queue[self.stop_index][0]].block_occupancy == True:
                #update current block
                self.current_block = self.authority_stop_queue[self.stop_index][0]
                self.authority_stop_queue[self.stop_index] = self.authority_stop_queue[self.stop_index][1:]
                #update current speed
                self.current_suggested_speed = self.suggested_speed_queue[self.stop_index][0]
                self.suggested_speed_queue[self.stop_index] = self.suggested_speed_queue[self.stop_index][1:]

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

        #update current authority only if authority has been changed by sw wayside
        if(not self.current_authority_changed):
            self.current_authority = len(self.authority_stop_queue[self.stop_index])

        if(self.authority_reset_ready):
            self.authority_reset_ready = False
            self.current_authority_changed = False

        print(f'speed list: ',self.suggested_speed_queue[self.stop_index])
        print(f'authority list: ',self.authority_stop_queue[self.stop_index])
        print(f'current speed: ',self.current_suggested_speed)
        print(f'current block: ', self.current_block)

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
