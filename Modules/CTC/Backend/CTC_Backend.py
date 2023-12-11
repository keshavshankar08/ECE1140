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
        self.system_time = QTime()
        self.hourly_ticket_sales = 0

        #Update system time
        signals.current_system_time.connect(self.update_current_time)

        #receive update from main backend
        signals.ctc_office_update_backend.connect(self.backend_update_backend)

        #receive updates from ctc frontend
        signals.ctc_office_frontend_update.connect(self.frontend_update_backend)

    #Update Current Time
    def update_current_time(self, time):
        self.system_time = time

    #sends updates from ctc backend to ctc frontend
    def send_frontend_update(self):
        signals.ctc_office_update_frontend.emit(self.track_instance_copy, self.active_trains_instance_copy, self.hourly_ticket_sales)

    #sends update to main backend
    def send_main_backend_update(self):
        signals.ctc_office_backend_update.emit(self.track_instance_copy, self.active_trains_instance_copy, self.hourly_ticket_sales)

    #updates active trains instance
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    def update_queue_trains(self, updated_queue_trains):
        self.queue_trains = updated_queue_trains

    #updates track instance
    def update_copy_track_instance(self, updated_track_instance):
        self.track_instance_copy = updated_track_instance

    #updates ticket sales
    def update_ticket_sales(self, updated_ticket_sales):
        self.hourly_ticket_sales = updated_ticket_sales

    #Main backend handler
    def backend_update_backend(self, track_instance, active_trains, ticket_sales):
        self.update_trains()
        self.update_train_progress(track_instance)
        self.update_copy_active_trains(active_trains)
        self.update_copy_track_instance(track_instance)
        self.update_ticket_sales(ticket_sales)
        self.send_frontend_update()
        self.send_main_backend_update()

    #Handler for update from ctc frontend
    def frontend_update_backend(self, track_instance, active_trains, ticket_sales, queue_trains):
        #update local instance variables
        self.update_copy_track_instance(track_instance)
        self.update_copy_active_trains(active_trains)
        self.update_ticket_sales(ticket_sales)
        self.update_queue_trains(queue_trains)

    #This function moves trains from the queue to active
    def update_trains(self):
        #get system time
        system_comp_time = QTime.fromString(self.system_time.toString("hh:mm:ss"), "hh:mm:ss")

        #loop through queue and check time
        for i, train in enumerate(self.queue_trains.queue_trains):
            comp_time = QTime.fromString(train.departure_time, "hh:mm:ss")
            if(system_comp_time >= comp_time):
                self.active_trains_instance_copy.active_trains.append(train)
                self.queue_trains.remove_train(i)
                self.active_trains_instance_copy.active_trains[len(self.active_trains_instance_copy.active_trains) - 1].next_stop()
                signals.ctc_added_train.emit(int(train.train_ID))

    #This function will update active trains and update their progress
    def update_train_progress(self, track):
        for train in self.active_trains_instance_copy.active_trains:
            train.update_authority(track)
            
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