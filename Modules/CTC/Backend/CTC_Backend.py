#CTC OFfice Backend
#This holds both the route class and a route queue
#This holds helper functions also

import sys
import re
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class CTCBackend():
    def __init__(self):
        signals.ctc_office_backend_update.connect(self.backend_update)
        signals.ctc_office_frontend_update.connect(self.backend_update)

        self.track_instance_copy = Track()
        self.active_trains = ActiveTrains()
        self.queue_trains = QueueTrains()
        self.route_queue = RouteQueue()

    def send_frontend_update(self):
        signals.ctc_office_frontend_update.emit(self.track_instance_copy)

    def send_frontend_update(self):
        signals.ctc_office_frontend_update(self.track_instance_copy)

    def send_main_backend_update(self):
        signals.ctc_office_backend_update(self.track_instance_copy)

    #main function to carry out all necessary functions in a cycle
    def backend_update(self, updated_track):
        #update local instance of track
        self.track_instance_copy = updated_track

        #send updated signals to wayside frontend
        self.send_frontend_update()

        #all the backend logic function calls

        #updates main instance at end of cycle
        self.send_main_backend_update()

    def verify_schedule(route_schedule):
        pass

    def verify_time_between(route_schedule):
        pass

    def verify_route_order(route_stops):
        pass


#Helper Functions
def validate_time_hours(input_time):
    regex = "^(?:[01]?[0-9]|2[0-3]):[0-5]?[0-9](?::[0-5]?[0-9])?$"

    p = re.compile(regex)

    if(input_time == None):
        return False
    
    if(re.search(p, input_time)):
       return True
    else:
        return False
    
def validate_time_minutes(input_time):
    regex = "^[0-5]?[0-9](?::[0-5]?[0-9])?$"

    p = re.compile(regex)

    if(input_time == None):
        return False
    
    if(re.search(p, input_time)):
       return True
    else:
        return False
