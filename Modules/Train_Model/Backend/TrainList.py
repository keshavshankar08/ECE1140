from PyQt6.QtCore import QObject
import sys
sys.path.append(".")
from signals import signals
from Modules.Train_Model.Backend.Train import Train

# class to represent a database of active Train objects 
# note, this is distinct from the ActiveTrains list in the CTC as it contains actual Train Model objects

class TrainList(QObject):
    def __init__(self):
        super().__init__()
        # dictionary to store a database of all trains in the system
        self.allTrains = {} # id, Train
        
        #### SIGNALS
        signals.trainModel_backend_update.connect(self.updateAllTrains)
        signals.ctc_added_train.connect(self.addTrain)
        # Train Controller
        signals.train_controller_send_power_command.connect(self.setPowerCommand)
        signals.train_controller_int_lights_status.connect(self.interiorLights)
        signals.train_controller_ext_lights_status.connect(self.exteriorLights)
        signals.train_controller_left_door_status.connect(self.leftDoors)
        signals.train_controller_right_door_status.connect(self.rightDoors)
        signals.train_controller_service_brake_status.connect(self.sBrake)
        signals.train_controller_emergency_brake_status.connect(self.eBrake)
        signals.train_controller_temperature_value.connect(self.receiveTemperature)
        # Track Model
        signals.track_model_speed_limit.connect(self.receiveSpeedLimit)
        signals.track_model_authority.connect(self.receiveAuthority)
        signals.track_model_beacon.connect(self.receiveBeacon)
        signals.track_model_suggested_speed.connect(self.receiveSuggestedSpeed)
        signals.track_model_block_grade.connect(self.receiveGradient)
        signals.track_model_send_passengers.connect(self.receivePassengers)
    
    # adds a train to the train dictionary, if it does not exist
    def addTrain(self, id):
        if id in self.allTrains: # error check
            raise ValueError(f"Train with ID {id} already exists in the train list.")
        train = Train()
        train.train_id = int(id)
        self.allTrains[id] = train
        
    # removes a train from the dictionary, if it exists
    def removeTrain(self, id):
        if id in self.allTrains:
            self.allTrains.pop(id)
        else:
            raise KeyError(f"{id} not found in train list.")
        
    # updates instantaneous train values
    def updateAllTrains(self):
        for id in self.allTrains:
            if isinstance(self.allTrains[id], Train):
                self.allTrains[id].TrainModelUpdateValues()
       
    #### PYQT SLOTS
         
    # updates e-brake values
    def eBrake(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].eBrake(value)
    
    # updates s-brake values
    def sBrake(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].sBrake(value)
    
    # updates interior lights
    def interiorLights(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].interiorLights(value)
    
    # updates exterior lights  
    def exteriorLights(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].exteriorLights(value)
    
    # updates left doors 
    def leftDoors(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].leftDoors(value)
    
    # updates right doors   
    def rightDoors(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].rightDoors(value)
    
    # updates right doors  
    def receiveTemperature(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveTemperature(value)
    
    # sets power command from train controller  
    def setPowerCommand(self, id, value): 
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].setPowerCommand(value)
    
    # receives beacon from track circuit
    def receiveBeacon(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveBeacon(value)
    
    # receives speed limit from track circuit
    def receiveSpeedLimit(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveSpeedLimit(value)
    
    # receives authority from track circuit
    def receiveAuthority(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveAuthority(value)
    
    # receives track polarity
    def receivePolarity(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receivePolarity(value)
    
    # receives suggested speed from track circuit
    def receiveSuggestedSpeed(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveSuggestedSpeed(value)
    
    # receives net passenger change
    def receivePassengers(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receivePassengers(value)

    # receives slope of block
    def receiveGradient(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveGradient(value)
    
    # receives tunnel status
    def receiveTunnel(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveTunnel(value)
            
        
# creates singleton instance of TrainList that is shared among modules, if necessary
trainList = TrainList()

