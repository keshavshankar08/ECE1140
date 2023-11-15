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
        self.track_instance_copy = Track()
        self.active_trains_instance_copy = ActiveTrains()
        self.queue_trains = QueueTrains()
        self.route_queue = RouteQueue()
        self.hourly_ticket_sales = 0

        #receive update from main backend
        signals.ctc_office_update_backend.connect(self.backend_update_backend)

        #receive updates from ctc frontend
        signals.ctc_office_frontend_update.connect(self.frontend_update_backend)

    #sends updates from ctc backend to ctc frontend
    def send_frontend_update(self):
        signals.ctc_office_frontend_update.emit(self.track_instance_copy, self.active_trains_instance_copy, self.hourly_ticket_sales)

    #sends update to main backend
    def send_main_backend_update(self):
        signals.ctc_office_backend_update.emit(self.track_instance_copy, self.active_trains_instance_copy, self.hourly_ticket_sales)

    #updates active trains instance
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    #updates track instance
    def update_copy_track_instance(self, updated_track_instance):
        self.track_instance_copy = updated_track_instance

    #updates ticket sales
    def update_ticket_sales(self, updated_ticket_sales):
        self.hourly_ticket_sales = updated_ticket_sales

    #Main backend handler
    def backend_update_backend(self, track_instance, active_trains, ticket_sales):
        self.update_copy_active_trains(active_trains)
        self.update_copy_track_instance(track_instance)
        self.update_ticket_sales(ticket_sales)
        self.send_frontend_update()
        self.send_main_backend_update()

    #Handler for update from ctc frontend
    def frontend_update_backend(self, track_instance, active_trains, ticket_sales):
        #update local instance variables
        self.update_copy_track_instance(track_instance)
        self.update_copy_active_trains(active_trains)
        self.update_ticket_sales(ticket_sales)

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
