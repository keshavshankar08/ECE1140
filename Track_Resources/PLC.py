import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class PLC():
    def __init__(self):
        self.track_instance_copy = Track()
        self.active_trains_instance_copy = ActiveTrains()

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
                print(self.green_line_wayside1_token_list)
            elif(wayside_number == 2):
                self.green_line_wayside2_token_list = self.tokenizer(file_name)
                print(self.green_line_wayside2_token_list)

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
    
    # Executes PLC code for a wayside controller block
    def interpreter(self, line_number, wayside_number, block_number):
        # get the tokens for the required wayside
        tokens = self.get_tokens(line_number, wayside_number)

        # token state storage variables
        curr_device = ""
        set_device_stage = False
        curr_device_var = ""
        stack = []

        # inputs to PLC devices
        ss_register = False
        sl_register = False
        sr_register = False
        cf_register = False
        cb_register = False

        # ouputs from PLC
        sd_register = False
        tls_register = False
        tll_register = False
        tlr_register = False
        cs_register = False

        # loop through every line of tokens
        for token_line in tokens:
            # SW device logic identified
            if(token_line[0] == "SW"):
                curr_device = "SW"
                set_device_stage = True
            # CR device logic identified
            elif(token_line[0] == "CR"):
                curr_device = "CR"
                set_device_stage = True
            else:
                set_device_stage = False

            # Once device identified
            if(set_device_stage == False):
                # if device is switch
                if(curr_device == "SW"):
                    # read - read in variables for switch
                    if(token_line[0] == "READ"):
                        ss_register, sl_register, sr_register = self.get_pre_junction_occupancies(line_number, block_number)
                    # condition - get which output register
                    elif(token_line[0] == "COND"):
                        curr_device_var = token_line[1]
                    # operation - compute and add to stack for calculation
                    elif(token_line[0] == "OPP"):
                        # not gate - not the variable identified and add to stack
                        if(token_line[1] == "NOT"):
                            if(token_line[2] == "SS"):
                                stack.append(not(ss_register))
                            elif(token_line[2] == "SL"):
                                stack.append(not(ss_register))
                            elif(token_line[2] == "SR"):
                                stack.append(not(ss_register))
                        # no change gate - add the variable to stack
                        elif(token_line[1] == "NC"):
                            if(token_line[2] == "SS"):
                                stack.append(ss_register)
                            elif(token_line[2] == "SL"):
                                stack.append(sl_register)
                            elif(token_line[2] == "SR"):
                                stack.append(sr_register)
                            elif(token_line[2] == "0"):
                                stack.append(False)
                        # save gate - store stack var to designated output
                        elif(token_line[1] == "SV"):
                            if(curr_device_var == "TLL"):
                                tll_register = stack[0]
                            stack.clear()
                        # and gate - and all elements in stack and store to designated output
                        elif(token_line[1] == "AND"):
                            if(curr_device_var == "SD"):
                                for log in stack:
                                    sd_register = log and sd_register
                            elif(curr_device_var == "TLS"):
                                for log in stack:
                                    tls_register = log and tls_register
                            elif(curr_device_var == "TLL"):
                                for log in stack:
                                    tll_register = log and tll_register
                            elif(curr_device_var == "TLR"):
                                for log in stack:
                                    tlr_register = log and tlr_register
                            stack.clear()
                # if device is crossing
                elif(curr_device == "CR"):
                    if(token_line[0] == "READ"):
                        cf_register, cb_register = self.get_pre_crossing_occupancies(line_number)
                    elif(token_line[0] == "COND"):
                        curr_device_var = token_line[1]
                    elif(token_line[0] == "OPP"):
                        if(token_line[1] == "NOT"):
                            if(token_line[2] == "CF"):
                                stack.append(not(cf_register))
                            elif(token_line[2] == "CB"):
                                stack.append(not(cb_register))
                        elif(token_line[1] == "NC"):         
                            if(token_line[2] == "CF"):
                                stack.append(cf_register)
                            elif(token_line[2] == "CB"):
                                stack.append(cb_register)
                        elif(token_line[1] == "OR"):
                            if(curr_device_var == "CS"):
                                for log in stack:
                                    cs_register = log or cs_register
                            stack.clear()
        if(self.track_instance_copy.lines[line_number].blocks[block_number].block_type == 1):
            self.track_instance_copy.lines[line_number].blocks[block_number].switch_direction = sd_register
            self.track_instance_copy.lines[line_number].blocks[block_number].switch_direction = sd_register # left one
            self.track_instance_copy.lines[line_number].blocks[block_number].switch_direction = sd_register # right one
            self.track_instance_copy.lines[line_number].blocks[block_number].traffic_light_color = tls_register
            self.track_instance_copy.lines[line_number].blocks[block_number].traffic_light_color = tll_register # left one
            self.track_instance_copy.lines[line_number].blocks[block_number].traffic_light_color = tlr_register # right one
        elif(self.track_instance_copy.lines[line_number].blocks[block_number].block_type == 3):
            self.track_instance_copy.lines[line_number].blocks[block_number].crossing_status = cs_register


    # Gets the tokens for a specific wayside controller
    def get_tokens(self, line_number, wayside_number):
        if(line_number == 0):
            if(wayside_number == 1):
                return self.red_line_wayside1_token_list
            elif(wayside_number == 2):
                return self.red_line_wayside2_token_list
        elif(line_number == 1):
            if(wayside_number == 1):
                return self.green_line_wayside1_token_list
            elif(wayside_number == 2):
                return self.green_line_wayside2_token_list

    # Gets SS, SL, and SR for a junction
    def get_pre_junction_occupancies(self, line_number, block_number):
        SS = SL = SR = False
        if(line_number == 0):
            pass
        elif(line_number == 1):
            junc_13 = [[13,14,15,16,17],[12,11,10,9,8],[1,2,3,4,5]]
            junc_28 = [[28,27,26,25,24],[29,30,31,32,33],[150,149,148,147,146]]
            junc_57 = [[57,56,55,54,53],[0],[58,59,60,61,62]]
            junc_63 = [[63,64,65,66,67],[58,59,60,61,62],[0]]
            junc_77 = [[77,78,79,80,81],[101,102,103,104,105],[76,75,74,73,72]]
            junc_85 = [[85,84,83,82,81],[86,87,88,89,90],[100,99,98,97,96]]
            if(block_number == 13):
                for section in range(3):
                    for blk in junc_13[section]:
                        if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                            if(section == 0): 
                                SS = True
                                break
                            elif(section == 1):
                                SL = True
                                break
                            elif(section == 2):
                                SR = True
                                break
            elif(block_number == 28):
                for section in range(3):
                    for blk in junc_28[section]:
                        if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                            if(section == 0): 
                                SS = True
                                break
                            elif(section == 1):
                                SL = True
                                break
                            elif(section == 2):
                                SR = True
                                break
            elif(block_number == 57):
                for section in range(3):
                    for blk in junc_57[section]:
                        if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                            if(section == 0): 
                                SS = True
                                break
                            elif(section == 1):
                                SL = True
                                break
                            elif(section == 2):
                                SR = True
                                break
            elif(block_number == 63):
                for section in range(3):
                    for blk in junc_63[section]:
                        if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                            if(section == 0): 
                                SS = True
                                break
                            elif(section == 1):
                                SL = True
                                break
                            elif(section == 2):
                                SR = True
                                break
            elif(block_number == 77):
                for section in range(3):
                    for blk in junc_77[section]:
                        if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                            if(section == 0): 
                                SS = True
                                break
                            elif(section == 1):
                                SL = True
                                break
                            elif(section == 2):
                                SR = True
                                break
            elif(block_number == 85):
                for section in range(3):
                    for blk in junc_85[section]:
                        if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                            if(section == 0): 
                                SS = True
                                break
                            elif(section == 1):
                                SL = True
                                break
                            elif(section == 2):
                                SR = True
                                break
        return SS,SL,SR

    # Gets CF and CB
    def get_pre_crossing_occupancies(self, line_number):
        CF = CB = False
        if(line_number == 0):
            pass
        elif(line_number == 1):
            cross_19 = [[20,21,22,23,24],[18,17,16,15,14]]
            for section in cross_19:
                for blk in section:
                    if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                        if(section == 0):
                            CF = True
                            break
                        if(section == 1):
                            CB = True
                            break
        return CF, CB

        
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