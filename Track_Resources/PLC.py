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
    
    # Main handler for PLC
    def update_plc(self, track_instance, active_trains_instance, file_name, line_number, wayside_number):
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(active_trains_instance)
        self.update_plc_program(file_name, line_number, wayside_number)
        self.route_verification()
        self.send_plc_update()

    # Send updates from plc to wayside backend
    def send_plc_update(self):
        signals.sw_wayside_plc_update.emit(self.track_instance_copy, self.active_trains_instance_copy)

    # Update local instance of track
    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    # Update local instance of active trains
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    # Update PLC program for a wayside controller on a line
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
    
    # Interprets PLC code for a wayside controller block
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
                if(curr_device == "SW" and self.track_instance_copy.lines[line_number].blocks[block_number].block_type == 1):
                    # read - read in variables for switch
                    if(token_line[0] == "READ"):
                        occupancies = self.get_pre_junction_occupancies(line_number, block_number)
                        ss = occupancies[0]
                        sl = occupancies[1]
                        sr = occupancies[2]
                        for blk in ss:
                            ss_register = ss_register or self.track_instance_copy.lines[line_number].blocks[blk].block_occupancy
                        for blk in sl:
                            sl_register = sl_register or self.track_instance_copy.lines[line_number].blocks[blk].block_occupancy
                        for blk in sr:
                            sr_register = sr_register or self.track_instance_copy.lines[line_number].blocks[blk].block_occupancy

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
                elif(curr_device == "CR" and self.track_instance_copy.lines[line_number].blocks[block_number].block_type == 3):
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
            sb, sl, sr = self.track_instance_copy.lines[line_number].blocks[block_number].get_tri_junction_blocks(line_number)
            self.track_instance_copy.lines[line_number].blocks[sb].switch_direction = sd_register
            self.track_instance_copy.lines[line_number].blocks[sl].switch_direction = sd_register
            self.track_instance_copy.lines[line_number].blocks[sr].switch_direction = sd_register
            self.track_instance_copy.lines[line_number].blocks[sb].traffic_light_color = tls_register
            self.track_instance_copy.lines[line_number].blocks[sl].traffic_light_color = tll_register
            self.track_instance_copy.lines[line_number].blocks[sr].traffic_light_color = tlr_register
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

    # Gets SS, SL, and SR blocks
    def get_pre_junction_occupancies(self, line_number, block_number):
        if(line_number == 0):
            junc_9 = [[9,8,7,6,5],[0],[10,11,12,13,14]]
            junc_16 = [[16,17,18,19,20],[1,2,3,4,5],[15,14,13,12,11]]
            junc_27 = [[27,26,25,24,23],[28,29,30,31,32],[76,75,74,73,72]]
            junc_33 = [[33,34,35,36,37],[72,73,74,75,76],[32,31,30,29,28]]
            junc_38 = [[38,37,36,35,34],[39,40,41,42,43],[71,70,69,68,67]]
            junc_44 = [[44,45,46,47,48],[67,68,69,70,71],[43,42,41,40,39]]
            junc_52 = [[52,51,50,49,48],[53,54,55,56,57],[66,65,64,63,62]]
            if(block_number == 9):
                return junc_9
            elif(block_number == 16):
                return junc_16
            elif(block_number == 27):
                return junc_27
            elif(block_number == 33):
                return junc_33
            elif(block_number == 38):
                return junc_38
            elif(block_number == 44):
                return junc_44
            elif(block_number == 52):
                return junc_52
        elif(line_number == 1):
            junc_13 = [[13,14,15,16,17],[12,11,10,9,8],[1,2,3,4,5]]
            junc_28 = [[28,27,26,25,24],[29,30,31,32,33],[150,149,148,147,146]]
            junc_57 = [[57,56,55,54,53],[0],[58,59,60,61,62]]
            junc_63 = [[63,64,65,66,67],[58,59,60,61,62],[0]]
            junc_77 = [[77,78,79,80,81],[101,102,103,104,105],[76,75,74,73,72]]
            junc_85 = [[85,84,83,82,81],[86,87,88,89,90],[100,99,98,97,96]]
            if(block_number == 13):
                return junc_13
            elif(block_number == 28):
                return junc_28
            elif(block_number == 57):
                return junc_57
            elif(block_number == 63):
                return junc_63
            elif(block_number == 77):
                return junc_77
            elif(block_number == 85):
                return junc_85

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
        self.execute_plc_program()

    # Executes PLC program for each wayside controller
    def execute_plc_program(self):
        for device in self.track_instance_copy.red_line_device_blocks_ws1:
            self.interpreter(0, 1, device)
        for device in self.track_instance_copy.red_line_device_blocks_ws2:
            self.interpreter(0, 2, device)
        for device in self.track_instance_copy.red_line_device_blocks_ws1:
            self.interpreter(1, 1, device)
        for device in self.track_instance_copy.red_line_device_blocks_ws2:
            self.interpreter(1, 2, device)