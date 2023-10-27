import PyQt6
from PyQt6.QtCore import QObject


#<> = constructed
#<><> = done
#think about number of trains, maybe use train id
#think about automatic/manuel mode
#INPUTS
    #need L doors and r doors <><>
    #need int lights and ext lights <><>
    #need emergency button and service brake, incorporate emergency button as also passenger emergency <>
    #need authority <>
    #need commanded speed <>
    #need beacon info<>
    #need current speed <>
    #need temperature <>
    #need KP and KI <>
    #need BOWER <>
#OUTPUTS
    #braking
    #commanded speed
    #R and L doors
    #int lights and ext lights
    #temperature
    #KP and KI
    #commanded power

class trainController:
    def __init__(self):
        #KP and KI values
        self.KP = 0.0
        self.KI = 0.0

        #Door values, True = Closed, False = Open
        self.Rdoor = True
        self.Ldoor = True

        #Light Values, True = On, False = Off
        self.intLights = True
        self.extLights = True

        #Temperature, technically ranges from 0.0 to inf(try and limit it to 58.0 to 85.0)
        self.trainTemp = 0.0

        #Commanded Speed and current speed (range from any value up to speed limit)
        self.commandedSpeed = 0.0
        self.currentSpeed = 0.0

        #Commanded Power
        self.commandedPower = 0.0

        #Authority and Beacon Info
        self.authority = 0.0
        self.beaconInfo = " "

        #Emergency button, used for passengers and driver
        #True = On, False = Off
        self.emergencyBrake = False

        # Service Brake - ranges from 0.0 (no brake) to 1.0 (full brake)
        self.serviceBrake = 0.0

        #automatic/manuel mode, True = auto, False = manuel
        self.mode = False

        #train Id to know what train is which
        self.trainID = " "

    #this sets the train ID
    def setTrainID(self, trainNumber):
        self.trainID = trainNumber

    #accessor for the train ID
    def getTrainID(self):
        return self.trainID


    #this function will toggle the emergency brake
    def toggleEmergencyBrake(self):
        self.emergencyBrake = not self.emergencyBrake

    #this function will toggle the doors back and forth
    def toggleDoors(self):
        self.Rdoor = not self.Rdoor
        self.Ldoor = not self.Ldoor

    #this function will toggle the lights back and forth
    def toggleLigths(self):
        self.intLights = not self.intLights
        self.extLights = not self.extLights

    

    




    
