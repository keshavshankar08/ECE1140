# Track Object - A entire track network
class Track():
    def __init__(self):
        self.lines: list[Line] = []

        # ----- Initializing with preload data -----
        # Create red line
        red_line = Line()
        red_line.lineColor = 0

        # Red line block information
        red_line_default_blocks = [2,3,4,5,6,8,11,12,13,14,18,19,20,22,23,24,26,29,30,31,34,36,37,40,41,42,46,49,50,54,55,56,57,58,59,61,62,63,64,65,68,69,70,73,74,75]
        red_line_station_blocks = [7,17,21,25,35,45,48,60]
        red_line_station_names = ["Shadyside", "Herron Ave", "Swissville", "Penn Station", "Steel Plaza", "First Ave", "Station Square", "South Hills Junction"]
        red_line_crossing_blocks = [47]
        red_line_junction_blocks = [9,0,10,16,1,15,27,28,76,33,72,32,38,39,71,44,67,43,52,53,66]
        red_line.graph = {
            0:[9],
            1:[16,2],
            2:[1,3],
            3:[2,4],
            4:[3,5],
            5:[4,6],
            6:[5,7],
            7:[6,8],
            8:[7,9],
            9:[8,0,10],
            10:[9,11],
            11:[10,12],
            12:[11,13],
            13:[12,14],
            14:[13,15],
            15:[14,16],
            16:[1,15,17],
            17:[16,18],
            18:[17,19],
            19:[18,20],
            20:[19,21],
            21:[20,22],
            22:[21,23],
            23:[22,24],
            24:[23,25],
            25:[24,26],
            26:[25,27],
            27:[26,76,28],
            28:[27,29],
            29:[28,30],
            30:[29,31],
            31:[30,32],
            32:[31,33],
            33:[32,72,34],
            34:[33,35],
            35:[34,36],
            36:[35,37],
            37:[36,38],
            38:[37,71,39],
            39:[38,40],
            40:[39,41],
            41:[40,42],
            42:[41,43],
            43:[42,44],
            44:[43,67,45],
            45:[44,46],
            46:[45,47],
            47:[46,48],
            48:[47,49],
            49:[48,50],
            50:[49,51],
            51:[50,52],
            52:[51,53,66],
            53:[52,54],
            54:[53,55],
            55:[54,56],
            56:[55,57],
            57:[56,58],
            58:[57,59],
            59:[58,60],
            60:[59,61],
            61:[60,62],
            62:[61,63],
            63:[62,64],
            64:[63,65],
            65:[64,66],
            66:[65,52],
            67:[44,68],
            68:[67,69],
            69:[68,70],
            70:[69,71],
            71:[70,38],
            72:[33,72],
            73:[72,74],
            74:[73,75],
            75:[74,76],
            76:[75,27]
        }

        # Fill red Line
        for i in range(77):
            blk = Block()
            blk.block_number = i
            if(i in red_line_default_blocks):
                blk.block_type = "Default"
            elif(i in red_line_station_blocks):
                blk.block_type = "Station"
                blk.station_name = red_line_station_names[red_line_station_blocks.index(i)]
            elif(i in red_line_junction_blocks):
                blk.block_type = "Junction"
                blk.switch_direction = 0
                blk.traffic_light_color = 0
            elif(i in red_line_crossing_blocks):
                blk.block_type = "Crossing"
            red_line.blocks.append(blk)
            
        # Create green line
        green_line = Line()
        green_line.line_color = 1
        
        # Green line block information
        green_line_default_blocks = [3,4,5,6,7,8,10,11,14,15,17,18,20,21,23,24,25,26,27,30,32,33,34,35,36,37,38,40,41,42,43,44,45,46,47,49,50,51,52,53,54,55,59,60,61,64,66,67,68,69,70,71,72,74,75,79,80,81,82,83,84,86,87,89,90,91,92,93,94,95,97,98,99,102,103,104,106,107,108,109,110,111,112,113,115,116,117,118,119,120,121,122,124,125,126,127,128,129,130,131,133,134,135,136,137,138,139,140,142,143,144,145,146,147,148,149]
        green_line_station_blocks = [2,9,16,22,31,39,48,56,65,73,88,96,105,114,123,132,141]
        green_line_station_names = ["Pioneer", "Edgebrook", "Jalappa", "Whited", "South Bank", "Central", "Inglewood", "Overbrook", "Glenbury", "Dormont", "Mt Lebanon", "Poplar", "Castle Shannon", "Dormont", "Glenbury", "Overbrook", "Inglewood", "Central"]
        green_line_crossing_blocks = [19]
        green_line_junction_blocks = [13,12,1,28,29,150,57,0,58,65,62,0,77,101,76,85,86,100]
        green_line.graph = {
            0:[63],
            1:[13],
            2:[1],
            3:[2],
            4:[3],
            5:[4],
            6:[5],
            7:[6],
            8:[7],
            9:[8],
            10:[9],
            11:[10],
            12:[11],
            13:[12],
            14:[13,15],
            15:[14,16],
            16:[15,17],
            17:[16,18],
            18:[17,19],
            19:[18,20],
            20:[19,21],
            21:[20,22],
            22:[21,23],
            23:[22,24],
            24:[23,25],
            25:[24,26],
            26:[25,27],
            27:[26,28],
            28:[29],
            29:[30],
            30:[31],
            31:[32],
            32:[33],
            33:[34],
            34:[35],
            35:[36],
            36:[37],
            37:[38],
            38:[39],
            39:[40],
            40:[41],
            41:[42],
            42:[43],
            43:[44],
            44:[45],
            45:[46],
            46:[47],
            47:[48],
            48:[49],
            49:[50],
            50:[51],
            51:[52],
            52:[53],
            53:[54],
            54:[55],
            55:[56],
            57:[0,58],
            58:[59],
            59:[60],
            60:[61],
            61:[62],
            62:[63],
            63:[64],
            64:[65],
            65:[66],
            66:[67],
            67:[68],
            68:[69],
            69:[70],
            70:[71],
            71:[72],
            72:[73],
            73:[74],
            74:[75],
            75:[76],
            76:[77],
            77:[78,101],
            78:[77,79],
            79:[78,80],
            80:[79,81],
            81:[80,82],
            82:[81,83],
            83:[82,84],
            84:[83,85],
            85:[86],
            86:[87],
            87:[88],
            88:[89],
            89:[90],
            90:[91],
            91:[92],
            92:[93],
            93:[94],
            94:[95],
            95:[96],
            96:[97],
            97:[98],
            98:[99],
            99:[100],
            100:[85],
            101:[102],
            102:[103],
            103:[104],
            104:[105],
            105:[106],
            106:[107],
            107:[108],
            108:[109],
            109:[110],
            110:[111],
            111:[112],
            112:[113],
            113:[114],
            114:[115],
            115:[116],
            116:[117],
            117:[118],
            118:[119],
            119:[120],
            120:[121],
            121:[122],
            122:[123],
            123:[124],
            124:[125],
            125:[126],
            126:[127],
            127:[128],
            128:[129],
            129:[130],
            130:[131],
            131:[132],
            132:[133],
            133:[134],
            134:[135],
            135:[136],
            136:[137],
            137:[138],
            138:[139],
            139:[140],
            140:[141],
            141:[142],
            142:[143],
            143:[144],
            144:[145],
            145:[146],
            146:[147],
            147:[148],
            148:[149],
            149:[150],
            150:[28]
        }

        # Fill green line
        for i in range(151):
            blk = Block()
            blk.block_number = i
            # Set block types and specific information
            if(i in green_line_default_blocks):
                blk.block_type = "Default"
            elif(i in green_line_station_blocks):
                blk.block_type = "Station"
                blk.station_name = green_line_station_names[green_line_station_blocks.index(i)]
            elif(i in green_line_junction_blocks):
                blk.block_type = "Junction"
                blk.switch_direction = 0
                blk.traffic_light_color = 0
            elif(i in green_line_crossing_blocks):
                blk.block_type = "Crossing"
            green_line.blocks.append(blk)

        # Store lines in track
        self.lines.insert(0, red_line)
        self.lines.insert(1, green_line)

# Line Object - A single line from the entire track network
class Line:
    def __init__(self):
        self.line_color = ""
        self.blocks: list[Block] = []
        self.graph: dict[int, list[int]] = {}

# Block Object - A single block linked to a single Track
class Block:
    def __init__(self):
        self.block_number = 0
        self.block_type = 0
        self.block_occupancy = False
        self.track_fault_status = False
        self.maintenance_status = False
        self.switch_direction = False
        self.traffic_light_color = False
        self.station_name = ""
        self.crossing_status = False
            
    def get_block_number_string(self):
        return str(self.block_number)
    
    def get_block_type_string(self):
        if(self.block_type == 0):
            return "Default"
        elif(self.block_type == 1):
            return "Junction"
        elif(self.block_type == 2):
            return "Station"
        elif(self.block_type == 3):
            return "Crossing"
        
    def get_block_occupancy_string(self):
        return "Occupied" if(self.block_occupancy) else "Unoccupied"
    
    def get_track_fault_status_string(self):
        return "Detected" if(self.track_fault_status) else "Undetected"
    
    def get_maintenance_status_string(self):
        return "Active" if(self.maintenance_status) else "Inactive"
    
    # Returns switch direction string
    def get_switch_direction_string(self, line_int):
        # Junction switch-receiver pairs
        red_line_junction_switch_ends = [9,16,27,33,38,44,52]
        red_line_junction_receiver_ends = [[0,10],[1,15],[28,76],[72,32],[39,71],[67,43],[53,66]]
        green_line_junction_switch_ends = [13,28,57,63,77,85]
        green_line_junction_receiver_ends = [[12,1],[29,150],[0,58],[62,0],[101,76],[86,100]]

        # Find correct display string
        if(line_int == 0):
            listPos = red_line_junction_switch_ends.index(self.block_number)
            return str(red_line_junction_switch_ends[listPos]) + "-" + str(red_line_junction_receiver_ends[listPos][0]) if(not self.switch_direction) else str(red_line_junction_switch_ends[listPos]) + "-" + str(red_line_junction_receiver_ends[listPos][1])
        elif(line_int == 1):
            listPos = green_line_junction_switch_ends.index(self.block_number)
            return str(green_line_junction_switch_ends[listPos]) + "-" + str(green_line_junction_receiver_ends[listPos][0]) if(not self.switch_direction) else str(green_line_junction_switch_ends[listPos]) + "-" + str(green_line_junction_receiver_ends[listPos][1])
    
    def get_switch_direction_string_list(self, line_int):
        # Junction switch-receiver pairs
        red_line_junction_switch_ends = [9,16,27,33,38,44,52]
        red_line_junction_receiver_ends = [[0,10],[1,15],[28,76],[72,32],[39,71],[67,43],[53,66]]
        green_line_junction_switch_ends = [13,28,57,63,77,85]
        green_line_junction_receiver_ends = [[12,1],[29,150],[0,58],[62,0],[101,76],[86,100]]

        if(line_int == 0):
            listPos = red_line_junction_switch_ends.index(self.block_number)
            return [str(red_line_junction_switch_ends[listPos]) + "-" + str(red_line_junction_receiver_ends[listPos][0]), str(red_line_junction_switch_ends[listPos]) + "-" + str(red_line_junction_receiver_ends[listPos][1])]
        elif(line_int == 1):
            listPos = green_line_junction_switch_ends.index(self.block_number)
            return [str(green_line_junction_switch_ends[listPos]) + "-" + str(green_line_junction_receiver_ends[listPos][0]), str(green_line_junction_switch_ends[listPos]) + "-" + str(green_line_junction_receiver_ends[listPos][1])]

    def get_switch_direction_bool(self, direction, line_int):
        # Junction switch-receiver pairs
        red_line_junction_switch_ends = [9,16,27,33,38,44,52]
        red_line_junction_receiver_ends = [[0,10],[1,15],[28,76],[72,32],[39,71],[67,43],[53,66]]
        green_line_junction_switch_ends = [13,28,57,63,77,85]
        green_line_junction_receiver_ends = [[12,1],[29,150],[0,58],[62,0],[101,76],[86,100]]
        
        first_num = int(direction.split('-')[0])
        second_num = int(direction.split('-')[1])
        if(line_int == 0):
            list_pos_switch = red_line_junction_switch_ends.index(first_num)
            return False if(second_num == red_line_junction_receiver_ends[list_pos_switch][0]) else True
        elif(line_int == 1):
            list_pos_switch = green_line_junction_switch_ends.index(first_num)
            return False if(second_num == green_line_junction_receiver_ends[list_pos_switch][0]) else True

    def get_traffic_light_color_string(self):
        return "Green" if(self.traffic_light_color) else "Red"
    
    def get_traffic_light_color_bool(self, color):
        return True if(color == "Green") else False
    
    def get_crossing_status_bool(self, status):
        return True if(status == "Active") else False
        
    # Returns crossing status string
    def getCrossingActiveString(self):
        return "Active" if(self.crossing_status == True) else "Inactive"