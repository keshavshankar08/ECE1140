from PyQt6.QtCore import QObject, QDateTime
import sys
sys.path.append(".")
from signals import signals
from CONSTANTS import constants
from Modules.Train_Model.Backend.Train import Train


class TrainList(QObject):
    def __init__(self):
        super().__init__()
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
    
    def addTrain(self, id):
        if id in self.allTrains:
            raise ValueError(f"Train with ID {id} already exists in the train list.")
        train = Train()
        train.train_id = int(id)
        self.allTrains[id] = train
        
    def removeTrain(self, id):
        if id in self.allTrains:
            self.allTrains.pop(id)
        else:
            raise KeyError(f"{id} not found in train list.")
        
    def updateAllTrains(self):
        for id in self.allTrains:
            if isinstance(self.allTrains[id], Train):
                self.allTrains[id].TrainModelUpdateValues()
            
    def eBrake(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].eBrake(value)
        
    def sBrake(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].sBrake(value)
        
    def interiorLights(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].interiorLights(value)
        
    def exteriorLights(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].exteriorLights(value)
        
    def leftDoors(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].leftDoors(value)
        
    def rightDoors(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].rightDoors(value)
        
    def receiveTemperature(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveTemperature(value)
        
    def setPowerCommand(self, id, value): 
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].setPowerCommand(value)
        
    def receiveBeacon(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveBeacon(value)
        
    def receiveSpeedLimit(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveSpeedLimit(value)
        
    def receiveAuthority(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveAuthority(value)
        
    def receivePolarity(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receivePolarity(value)
        
    def receiveSuggestedSpeed(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveSuggestedSpeed(value)
        
    def receivePassengers(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receivePassengers(value)
    
    def receiveGradient(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveGradient(value)
            
    def receiveTunnel(self, id, value):
        if isinstance(self.allTrains[id], Train):
            self.allTrains[id].receiveTunnel(value)
            
        
    
trainList = TrainList()

