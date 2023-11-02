#CTC OFfice Backend
#This holds both the route class and a route queue
#This holds helper functions also

import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class CTCBackend():
    def __init__(self):
        signals.ctc_office_backend_update.connect(self.update_CTC)
        self.track_instance_copy = Track()
        self.active_trains = ActiveTrains()
        self.queue_trains = QueueTrains()
        self.route_queue = RouteQueue()

    def update_ui(self):
        signals.ctc_office_frontend_update(self.track_instance_copy)

    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    #main function to carry out all necessary functions in a cycle
    def update_CTC(self, trackInstance):
        self.trackInstanceCopy = trackInstance
        self.update_ui()

        #updates main instance at end of cycle
        signals.ctc_office_track_update.emit(self.trackInstanceCopy)
        #signals.ctc_office_active_trains_update.emit()

    def verify_schedule(route_schedule):
        pass

    def verify_time_between(route_schedule):
        pass

    def verify_route_order(route_stops):
        pass