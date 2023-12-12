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

        self.green_line_wayside1_token_list = self.tokenizer("Track_Resources/PLC_Programs/Green Line/ws1.txt")
        self.green_line_wayside2_token_list = self.tokenizer("Track_Resources/PLC_Programs/Green Line/ws2.txt")
        self.red_line_wayside1_token_list = self.tokenizer("Track_Resources/PLC_Programs/Red Line/ws1.txt")
        self.red_line_wayside2_token_list = self.tokenizer("Track_Resources/PLC_Programs/Red Line/ws2.txt")

        self.green_line_wayside1 = []
        self.green_line_wayside2 = []
        self.red_line_wayside1 = []
        self.red_line_wayside2 = []
    
    # Main handler for PLC
    def update_plc(self, track_instance, active_trains_instance, file_name, line_number, wayside_number):
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(active_trains_instance)
        self.update_plc_program(file_name, line_number, wayside_number)
        if(len(self.green_line_wayside1_token_list) != 0 and len(self.green_line_wayside2_token_list) != 0 and len(self.red_line_wayside1_token_list) != 0 and len(self.red_line_wayside2_token_list) != 0):
            self.route_verification()
            self.execute_plc_program()
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
        if(file_name != ""):
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
                                stack.append(not(sl_register))
                            elif(token_line[2] == "SR"):
                                stack.append(not(sr_register))
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
                                sd_register = stack[0] and stack[1]
                            elif(curr_device_var == "TLS"):
                                tls_register = stack[0] and stack[1]
                            elif(curr_device_var == "TLL"):
                                if(line_number == 0):
                                    tll_register = stack[0] and stack[1] and stack[2]
                                elif(line_number == 1):
                                    tll_register = stack[0] and stack[1]
                            elif(curr_device_var == "TLR"):
                                tlr_register = stack[0] and stack[1]
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
            cross_47 = [[48,49,50,51,52],[46,45,44,43,67,68,42]]
            for section in cross_47:
                for blk in section:
                    if(self.track_instance_copy.lines[1].blocks[blk].block_occupancy):
                        if(section == 0):
                            CF = True
                            break
                        if(section == 1):
                            CB = True
                            break
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
    
    # Gets a sections occupancy for a line
    def get_section_occupancy(self, line_number, section_number):
        if(line_number == 0):
            for block in self.track_instance_copy.red_line_sections[section_number]:
                if(self.track_instance_copy.lines[0].blocks[block].block_occupancy == True):
                    return True
            return False
        if(line_number == 1):
            for block in self.track_instance_copy.green_line_sections[section_number]:
                if(self.track_instance_copy.lines[1].blocks[block].block_occupancy == True):
                    return True
            return False
        
    # Gets the section a block is in
    def get_section_number(self, line_number, block_number):
        if(line_number == 0):
            section_num = 0
            for section in self.track_instance_copy.red_line_sections:
                for block in section:
                    if(block_number == block):
                        return section_num
                section_num += 1
        if(line_number == 1):
            section_num = 0
            for section in self.track_instance_copy.green_line_sections:
                for block in section:
                    if(block_number == block):
                        return section_num
                section_num += 1

    # Gets the new authority depending on what section the train is in
    def get_authority(self, line_number, block_number, direction):
        section_number = self.get_section_number(line_number, block_number)
        if(line_number == 0):
            if(not direction):#southbound
                return abs(block_number - self.track_instance_copy.red_line_sections[section_number][0])
            elif(direction):#northbound
                return abs(block_number - self.track_instance_copy.red_line_sections[section_number][-1])
        elif(line_number == 1):
            if(not direction):#southbound
                return abs(block_number - self.track_instance_copy.green_line_sections[section_number][0])
            elif(direction):#northbound
                return abs(block_number - self.track_instance_copy.green_line_sections[section_number][-1])
    
    # Will verify suggested authority and speed for all trains based on track
    def route_verification(self):
        for train in self.active_trains_instance_copy.active_trains:
            if(train.current_line == 0):
                # get all sections' statuses
                block_status = []
                for i in range(len(self.track_instance_copy.red_line_sections)):
                    block_status.append(self.get_section_occupancy(i, 1))

                curr_section = self.get_section_number(0, train.current_block)

                if(not train.current_authority_changed):
                    # go through and adjust auth to stop train when needed
                    if(curr_section == 0):
                        if(not train.current_direction):
                            if(block_status[1]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction)
                                    train.current_authority_changed = True
                    elif(curr_section == 1):
                        if(not train.current_direction):
                            if(block_status[3]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                        else:
                            if(block_status[0]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 2):
                        if(not train.current_direction):
                            if(block_status[3]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                        else:
                            if(block_status[1]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 3):
                        if(not train.current_direction):
                            if(block_status[4]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                        else:
                            if(block_status[1]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 4):
                        if(not train.current_direction):
                            if(block_status[6] or block_status[8]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 5):
                        if(not train.current_direction):
                            pass
                        else:
                            if(block_status[3] or block_status[1] or block_status[0] or block_status[2]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 6):
                        if(not train.current_direction):
                            if(block_status[7]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                        else:
                            if(block_status[5]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 7):
                        if(not train.current_direction):
                            if(block_status[9] or block_status[10]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 8):
                        if(not train.current_direction):
                            pass
                        else:
                            if(block_status[6]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 9):
                        if(not train.current_direction):
                            pass
                        else:
                            if(block_status[8]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                elif(train.current_authority_changed and not train.authority_reset_ready):
                    if(train.current_authority == 0):
                        train.authority_reset_ready = True   
            # green line verfication
            elif(train.current_line == 1):
                # get the block status'
                block_status = []
                for i in range(len(self.track_instance_copy.green_line_sections)):
                    block_status.append(self.get_section_occupancy(i, 1))

                # if the train is on 1 block
                curr_section = self.get_section_number(1, train.current_block)

                if(train.current_authority_changed == False):
                    if(curr_section == 1):
                        if(not train.current_direction):
                            if(block_status[2]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 2):
                        if(not train.current_direction):
                            if(block_status[3] or block_status[4]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 3):
                        if(not train.current_direction):
                            if(block_status[4] or block_status[5]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 4):
                        if(not train.current_direction):
                            if(block_status[5]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 5):
                        if(not train.current_direction):
                            if(block_status[6] or block_status[7]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 6):
                        if(not train.current_direction):
                            pass
                        else:
                            if(block_status[8]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                    elif(curr_section == 8):
                        if(not train.current_direction):
                            pass
                        else:
                            if(block_status[1] or block_status[0]):
                                if(self.get_authority(0, train.current_block, train.current_direction) < train.current_authority):
                                    train.current_authority = self.get_authority(0, train.current_block, train.current_direction) 
                                    train.current_authority_changed = True
                elif(train.current_authority_changed and not train.authority_reset_ready):
                    if(train.current_authority == 0):
                        train.authority_reset_ready = True

    # Executes PLC program for each wayside controller
    def execute_plc_program(self):
        for device in self.track_instance_copy.red_line_device_blocks_ws1:
            self.interpreter(0, 1, device)
        for device in self.track_instance_copy.red_line_device_blocks_ws2:
            self.interpreter(0, 2, device)
        for device in self.track_instance_copy.green_line_device_blocks_ws1:
            self.interpreter(1, 1, device)
        for device in self.track_instance_copy.green_line_device_blocks_ws2:
            self.interpreter(1, 2, device)