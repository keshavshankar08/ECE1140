#CTC_Train.py

class Route:
    def __init__(self):
        #create a counter
        self.stops = []
        self.stop_time = []
        self.dwell_time = []

class RouteQueue:
    def __init__(self):
        self.routes: list[Route] = []

    def add_route(self, add_route):
        self.routes.append(add_route)

    def remove_route(self, remove_route_index):
        self.routes.pop(remove_route_index)

class Train:
    def __init__(self):
        self.train_ID = 0
        self.authorit_list = []
        self.current_authority = 0
        self.suggested_speed_list = []
        self.current_suggested_speed = 0
        self.departure_time = ""
        #TODO -- Fill given a route object

class ActiveTrains:
    def __init__(self):
        self.active_trains: list[Train] = []

    def add_train(self, add_train):
        self.active_trains.append(add_train)

    def remove_train(self, remove_train_index):
        self.active_trains.pop(remove_train_index)

class QueueTrains:
    def __init__(self):
        self.queue_trains: list[Train] = []

    def add_train(self, add_train):
        self.queue_trains.append(add_train)

    def remove_train(self, remove_train_index):
        self.queue_trains.pop(remove_train_index)
