import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *

class PLC():
    def __init__(self):
        self.track_instance_copy = Track()
        self.active_trains_instance_copy = 1#ActiveTrains()

        # receives updates from wayside backend
        signals.sw_wayside_update_plc.connect(self.update_plc)

        self.green_line_wayside1_token_list = [[]]
        self.green_line_wayside2_token_list = [[]]
        self.red_line_wayside1_token_list = [[]]
        self.red_line_wayside2_token_list = [[]]

        self.green_line_wayside1 = []
        self.green_line_wayside2 = []
        self.red_line_wayside1 = []
        self.red_line_wayside2 = []
    
    # Handles all plc updates and execution
    def update_plc(self, track_instance, active_trains_instance, file_name, line_number, wayside_number):
        # update local instances of variables
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(active_trains_instance)

        # update stored plc data
        self.update_plc_program(file_name, line_number, wayside_number)

        # carry out logic on track with route
        self.route_verification()

        # send updated signals to main backend
        self.send_plc_update()

    # Send updates from plc to wayside backend
    def send_plc_update(self):
        signals.sw_wayside_plc_update.emit(self.track_instance_copy, self.active_trains_instance_copy)

    # Updates local instance of track
    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    # Updates local instance of active trains
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    # Updates PLC program for a wayside controller on a line
    def update_plc_program(self, file_name, line_number, wayside_number):
        if(line_number == 0):
            if(wayside_number == 1):
                self.red_line_wayside1_token_list = self.tokenizer(file_name)
            elif(wayside_number == 2):
                self.red_line_wayside2_token_list = self.tokenizer(file_name)
        elif(line_number == 1):
            if(wayside_number == 1):
                self.green_line_wayside1_token_list = self.tokenizer(file_name)
            elif(wayside_number == 2):
                self.green_line_wayside2_token_list = self.tokenizer(file_name)

    # Converts PLC program to a list of tokens
    def tokenizer(self, file_name):
        token_list = [[]]
        file_in = open(file_name, "r")
        line = "init"
        while(line):
            line = file_in.readline()
            if(line == ""):
                break
            line = line.strip()
            line_tokens = line.split(",")
            token_list.append(line_tokens)
        del token_list[0]
        return token_list
    
    # Executes PLC code for a wayside controller
    def interpreter(self):
        # should take in which line, which wayside
        # loop through each device on wayside
        # use plc's tokens to do logic depending on type of device
        # use logic output to set devices on track
        pass

    # Will verify suggested authority and speed for all trains based on track
    def route_verification(self):
        # should take in which line
        # go through every section and check blocks occupied and what direction trains going
        # do logic on changing authority depending on section occupancies by juncitons
            # essentially, check surrounding sections of junction. 
            # check which way loop travel is
            # check which way 1 width sections travel is
            # use this to see if trains get get off loop
            # if not, trains have to get off 1 width section into loop before other trains can get off
        pass