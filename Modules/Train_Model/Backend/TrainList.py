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
            self.allTrains[id].TrainModelUpdateValues()
            
    def eBrake(self, id, value):
        self.allTrains[id].eBrake(value)
        
    def sBrake(self, id, value):
        self.allTrains[id].sBrake(value)
        
    def interiorLights(self, id, value):
        self.allTrains[id].interiorLights(value)
        
    def exteriorLights(self, id, value):
        self.allTrains[id].exteriorLights(value)
        
    def leftDoors(self, id, value):
        self.allTrains[id].leftDoors(value)
        
    def rightDoors(self, id, value):
        self.allTrains[id].rightDoors(value)
        
    def receiveTemperature(self, id, value):
        self.allTrains[id].receiveTemperature(value)
        
    def setPowerCommand(self, id, value): 
        self.allTrains[id].setPowerCommand(value)
        
    def receiveBeacon(self, id, value):
        self.allTrains[id].receiveBeacon(value)
        
    def receiveSpeedLimit(self, id, value):
        self.allTrains[id].receiveSpeedLimit(value)
        
    def receiveAuthority(self, id, value):
        self.allTrains[id].receiveAuthority(value)
        
    def receivePolarity(self, id, value):
        self.allTrains[id].receivePolarity(value)
        
    def receiveSuggestedSpeed(self, id, value):
        self.allTrains[id].receiveSuggestedSpeed(value)
        
    def receivePassengers(self, id, value):
        self.allTrains[id].receivePassengers(value)
    
    def receiveGradient(self, id, value):
        self.allTrains[id].receiveGradient(value)
            
        
    
trainList = TrainList()


# what I need from Tim:
    # signal for when train is dispatched, id to assign, line it is on (if that's relevant)
    # signal for when train returns to yard, id of train to remove from dictionary
# what I need from Tim, Ben, John (don't think this concerns wayside but could be wrong):
    # modify signals so that their first parameter is train ID.
        # that way, signals can go to specific train and not every train
