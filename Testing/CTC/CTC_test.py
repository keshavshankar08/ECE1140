import unittest
import sys
sys.path.append(".")
from Train_Resources.CTC_Train import *

class TestAuthourity(unittest.TestCase):
    #Calculate authority function
    #Function to calculate authority
    def calculate_authority(self, stop):
        #make a list of the route
        self.authority_stop_queue = []
        #create track/line object to call function from
        self.track = Track()

        #get all stops in block number form
        self.block_stops = [stop]

        #make the authority list
        for i in range(len(self.block_stops)):
            #if it's the last stop, return to yard at -1
            if(i == 0):
                #for first stop, get authority from yard **[1:] removes first element (previous stop)
                self.authority_stop_queue.append(self.track.lines[1].get_shortest_path(0, self.block_stops[i], [])[1:])
            else:
                #otherwise, get the length of the shortest path between the stops **[1:] removes first element (previous stop)
                self.authority_stop_queue.append(self.track.lines[1].get_shortest_path(self.block_stops[i-1], self.block_stops[i], [])[1:])

        return self.authority_stop_queue

    #Test cases
    def test_authority(self):
        self.assertEqual(self.calculate_authority(73), [[63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]], f'Authority List is Incorrect\n\nThe following are not equal:\n{self.calculate_authority(73)}\n{[[63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]]}')

if __name__ == '__main__':
    unittest.main()
