# This can handle the system time which is adjustable from 0.5x to 50x

# ----- Pseudocode -----

# The general idea is that
# 1x time = 1 seconds / cycle
# 2x time = 1*2 seconds / cycle
# 50x time = 1*50 seconds / cycle
# 0.5x time = 1*0.5 seconds / cycle

# So the algorithm goes like this

systemSpeedChosen = 1.0 # This will be whatever the user chooses from 0.5x - 50x

systemSpeedConstant = 1.0 # This is the constant for 1 seconds / cycle

systemSpeedCalculated = systemSpeedConstant*systemSpeedChosen # This will give the new system speed in number of seconds / cycle

systemSpeedConversionConstant = 1000.0 # This is the constant for 1000 mS / 1 second

systemSpeed = systemSpeedCalculated * systemSpeedConversionConstant # This takes the speed speed 

# We can put this all in a class and have a function of it that ouputs the systemSpeed in ms to the signals.py

# The idea is that we can use something like delay(systemSpeed) at the end of looping structure for the backend program
# so that the system just takes a delay before the next loop cycle

# This class would be called to update the signals.py with the systemSpeed whenever the main_ui detects the user changed the system speed slider