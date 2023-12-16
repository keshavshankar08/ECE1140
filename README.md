# ECE1140
[ECE 1140](https://catalog.upp.pitt.edu/preview_course_nopop.php?catoid=223&coid=1193695) is a class in the University of Pittsburgh's Electrical and Computer Engineering Department that focus' on systems and project engineering.

1. [Description](#description)
2. [Collaborators](#collaborators)
3. [Licensing](#licensing)
4. [Installation and Setup](#installation-and-setup)
5. [Usage and Configuration](#usage-and-configuration)
6. [Demo](#demo)

## Description
Our main project in this class was creating a full-stack train system simulator. The main idea was to apply all systems and project engineering processes to make a emulation of the [Pittsburgh Light Rail](https://en.wikipedia.org/wiki/Pittsburgh_Light_Rail)

## Collaborators
| Name | GitHub | Module |
| ----------- | ----------- | ----------- |
| Tim Horrell | [Tim](https://github.com/tdhorrell) | CTC |
| Keshav Shankar | [Keshav](https://github.com/keshavshankar08) | SW Track Controller |
| Nate Ginck | [Nate](https://github.com/nateginck) | HW Track Controller |
| Ben Shuttleworth | [Ben](https://github.com/benshuttle28) | Track Model |
| Alex Ivensky | [Alex](https://github.com/alexivensky) | Train Model |
| John Deibert | [John](https://github.com/jdeibert17) | SW Train Controller |

## Installation and Setup
This section covers all directions to successfully install and run the application.

Prerequisites: [Python](https://www.python.org/downloads/) 3.7.9 or greater

## Usage and Configuration
### Main Launcher 

User Interface 

Open the main launcher by opening the application, either by shortcut or from program files. 

Module Launchers 

Launch individual modules by selecting the corresponding button under the “Modules” section. 

System Clock 

System Time 

Update system time by altering the value by scrolling or editing the text. 

System Speed Multiplier 

Update the system speed multiplier by altering the text or scrolling. The range of accepted values is 0.5x to 50x speed. 

System Pause 

Press the ‘Pause’ button to stop the system clock and all modules. 

System Resume 

After the system is paused, press ‘Resume’ to start the system clock and resume the system. 

Admin 

Enter the admin code and press ‘Enter Admin Mode.’ If the code is correct, admin mode will open with key inputs. 

 

### CTC 

User Interface 

Launch the SW Wayside from the main launcher by clicking “SW Wayside” 

Current Line 

Select the desired line of operation 

Time 

A live display of the system time 

Upload Schedule (Automatic Mode) 

This button opens a file explorer. Select and upload a valid schedule file built from the schedule builder to add to the queue. 

Open Schedule Builder (Automatic Mode) 

This button opens the schedule builder application. This enables schedules to be made for the future. 

Manual Mode 

Add Stop 

Select add stop to add a stop to the schedule being built 

Delete Selected Stop 

Highlight the stop to be deleted from the table. Selecting this button will remove that stop from the schedule. 

Clear All Stops 

This button deletes all stops from the schedule 

Dispatch 

This button finalizes the schedule and adds it to the queue. The train will dispatch at a time estimated to arrive at the first stop on time. 

Queue 

Train Queue 

This displays all trains actively in the queue awaiting the time to leave the yard. 

Selecting a train will display its schedule below, in the ‘Selected Schedule’ table. 

Selected Schedule 

This table displays the selected schedule of the train in the queue. 

Dispatched Trains 

Dispatched Trains 

This displays all trains actively on the track, including their suggested speed and authority. 

Selecting a train displays the selected schedule of the train. 

Selected Schedule 

This table displays the schedule of the train selected in the dispatched trains table. 

Line Status 

Block 

Select the desired block to view information and toggle maintenance. 

Track Fault/Maintenance Status 

This indicator shows yellow when a block is set to maintenance. 

This indicator shows red when a track fault is registered on the block. 

Block Occupancy 

This shows block occupancy of the current block. It will show green when the block is occupied. 

Notable Blocks 

This display summarizes blocks that are under maintenance, have fault status, or occupied. 

Hourly Ticket Sales 

This displays the hourly ticket sales of the current line. 

Python 

The version of Python used for this program was 3.12.0. Please ensure that this is the installed version. 

 

### Hardware Wayside Controller 

Arduino 

The Arduino Mega 2560 is the supported hardware component for the Wayside Controller. An LCD display can be added using the Communication 20 and Communication 21 pins. Documentation can be found here: 

https://docs.arduino.cc/hardware/mega  

The Arduino Mega 2560 is the supported hardware component for the Wayside Controller. An LCD display can be added using the Communication 20 and Communication 21 pins. Documentation can be found here: https://docs.arduino.cc/hardware/mega-2560 

The cable used to connect the Arduino to the computer running the program is a USB to Printer Cable.  

Before running the Main Backend, the Arduino Mega 2560 requires a file to be uploaded to it. This file is called Arduino.ino and is located in the HardwareWayside/Backend/Arduino folder.  

Using Arduino IDE 2.2.1, the file can be compiled and uploaded to the Arduino Mega. The documentation for this can be found here: https://www.arduino.cc/en/software 

Ensure that the LiquidCrystal_I2C library is installed in the Arduino IDE. 

 

Pyserial 

If any libraries or dependencies are causing problems upon running the program, a certain library is likely missing. For the Hardware Wayside module, ensure the Pyserial is installed. Using pip this can be done by writing pip install pyserial in the terminal. 

Pyserial 3.4 is the latest stable tested version used for the program. Please ensure that this version is installed for reliable results. Documentation for Pyserial can be found here: https://pyserial.readthedocs.io/en/latest/pyserial.html 

Python 

The version of Python used for this program was 3.12.0. Please ensure that this is the installed version.  

 

### Software Wayside Controller 

User Interface 

Launch the SW Wayside from the main launcher by clicking “SW Wayside” 

Mode selection 

In the top left, there is a combo box where you can select either “Automatic” or “Manual” mode. Manual mode allows manual control of all track devices, and automatic mode automatically controls all track devices. 

Line selection 

Below the Mode selection, there is a combo box where you can select either “Red Line” or “Green Line”. This box is only unlocked once a mode is selected. 

View Track Map 

To the right of the Line selection, the “View Track Map” button will open an image of the current line selected. This button is only unlocked once a line is selected. 

Wayside Selection 

Below the Line selection, there is a combo box where you can select either “Wayside 1” or “Wayside 2”. This box is only unlocked once a line is selected. 

Upload PLC Program 

To the right of the wayside selection, the “Upload PLC Program” button opens a file explorer on the device, allowing you to select a .txt file with the plc program for a wayside controller. This button is only unlocked once a wayside is selected. 

Block Selection 

Below the wayside selection, there is a combo box where you can select a block from the long list of blocks for the selected wayside. This box is only unlocked once a wayside is selected. 

Block Information 

Below the block selection, all the block type, block occupancy, track fault status, maintenance status, switch direction, traffic light color, station name, and crossing status. This information only unlocks once a block is selected. Furthermore, the junction information, station information, and crossing information only show up when the blocks type is one of those types, respectively. 

Manual toggles 

In the junction, station, and crossing boxes, when in manual mode, the “tx” or (transmit) buttons appear as well as a combo box to manually change the value of a specific device using the combo box, then transmit that signal using the tx button. 

Python 

The version of Python used for this program was 3.7.9. Please ensure that this is the installed version or greater. 

### Track Model  

1. User Interface 

a. Launch Track Model interface from the Main Launcher 

b. Load Track Model 

i. A track model file must be loaded when the module is opened. To do this, click 			the button labeled "Load Track Model" and select the desired .xlsx file from the 			file dialog box. 

c. Line Selector Dropdown 

i. After a Track Model file is loaded, the line selector box becomes available. The 			user can select to see a map of the Red Line or Green Line by selecting the line 			name from the dropdown box. 

d. Failure Modes 

i. The three failure modes for the Track Model are listed in the top menu. Each 			radio button can be selected to generate that failure. 

ii. The failure mode is generated for a single block. This block is determined by 			which block the user has currently selected, which can be seen in the "Block 			Number" section under Block Information in the right-side display.  

e. Environment Temperature 

i. The environment temperature of the simulation can be changed using the spin 			box on the right side of the screen. The value shown in the box is in degrees 			Fahrenheit and is defaulted to 68 degrees when the module is opened.  

ii. The current temperature can be changed either by using the arrows next to the 			temperature value, or simply by typing in a new temperature value.  

f. Block Information  

i. The information for a given block will be shown when that block is left-clicked 			on.  

ii. Information such as the block number, length, grade, speed limit, elevation, 			cumulative elevation, and track heater status will be displayed for all blocks.  

iii. Certain information pertaining to the block's infrastructure, like the traffic 			light, switch direction, crossing status, and beacon data will only be shown if the 			selected block contains that infrastructure.  

g. Train Information 

i. Information for a given train will be shown when an occupied block is selected.  

ii. The train ID, direction of travel, authority, current speed, acceleration, and 			passenger occupancy will all be displayed. 

h. Station Information 

i. Information for a given station will be shown when a block containing a station 			is selected.  

ii. The station name and number of tickets sold will be shown at all times. The 			number of tickets sold represents how many passengers are waiting at the station. 			iii. When a station block is occupied by a train, the number of passengers 				boarding and disembarking the train will also be shown.  

i. Block Colors 

i. A key is shown above the track map indicating that a green block is an 				unoccupied block, and a red block is an occupied block. The grey block on each 			map is the train yard.  

2. Track Map 

a. Traffic Lights 

i. Circles exist at each block of a junction to represent the current traffic light 			color. A red light means a train is not allowed to proceed beyond the block that 			contains the traffic light. Conversely, a green light means a train may proceed 			beyond the block with the traffic light. 

b. Railway Crossing Lights 

i. Circles exist at railway crossing blocks to indicate the status of the crossing. If 			the light is white, the crossing is in the inactive state, meaning the gates are up 			and traffic can cross the tracks. When the light is orange, the crossing is in an 			active state, meaning the gates are down and traffic cannot cross due to a train in 			close proximity to the crossing block.  

### Train Model 

User Interface 

Launch Train Model interface from the Main Launcher. 

Train Selection 

In the top left, there is a combo box where you can select any active train in the system. Upon selection, the train’s values will be displayed in the Train Model UI. 

By default, there is no train selected, and all interface elements are deactivated. A train must be selected for the UI to be functional. 

Train Information 

In the UI, all of the chosen train’s information can be viewed. This includes crew count, passenger count, mass, length, width, lights, doors, temperature, brake status, velocity, acceleration, and power. It also includes beacon information, which contains current station name if the train is at a station.  

The UI also includes advertisements for passengers at the bottom. 

Failure Modes 

The UI includes a selection of failure modes to simulate failure scenarios. These include signal pickup failure, brake failure, and engine failure. The failure modes can be activated or deactivated by clicking the corresponding checkboxes. 

Emergency Brake 

The UI includes a push button for the passenger emergency brake. Once activated by a passenger, it can only be deactivated by the Train Controller. 

### Train Controller 

User Interface 

a. Launch Train Controller interface from the Main Launcher. 

b. Train Selection 

In the top left, there is a combo box where you can select any active train in the system. Upon selection, the train’s values will be displayed in the Train Controller UI. 

By default, there is no train selected, and all interface elements are deactivated. A train must be selected for the UI to be functional. 

 

c. Train Information 

In the UI, all of the chosen train’s information can be viewed. This includes commanded speed, current speed, power, authority, and station name. 

d. Failure Modes 

The UI includes a selection of failure modes to simulate failure scenarios. These include signal pickup failure, brake failure, and engine failure. The failure modes will be sent from the train model. When a failure is activated, the emergency brake will automatically turn on. When there are no failures left, the emergency brake will be allowed to manually be turned off. 

e. Driver Throttle 

The UI includes a slider for the driver to change the commanded speed. The driver will only be allowed to change the commanded speed when he selects the manual mode button in the top right of the UI. 

f. Braking 

The UI includes a slider for the driver to change the status of the emergency brake. The emergency brake only has two states, on or off. When the brake is applied, the power will go to 0 and will slow down the train. The driver will only be allowed to change the emergency brake when he selects the manual mode button in the top right of the UI. 

The UI includes a slider for the driver to change the status of the service brake. The service brake only has two states, on or off. When the brake is applied, the power will go to 0 and will slow down the train. The driver will only be allowed to change the service brake when he selects the manual mode button in the top right of the UI. 

g. Utilities 

The UI includes push buttons for the driver to change the status of the exterior and interior lights. The buttons can be pushed to activate whether the lights will be on or off. When the on button is pushed, then the lights will be activated and vice versa. The driver will only be allowed to change the lights when he selects the manual mode button in the top right of the UI. 

The UI includes push buttons for the driver to change the status of the right and left doors. The buttons can be pushed to activate whether the doors will be closed or opened. When the closed button is pushed, then the doors will be shut closed and vice versa. The driver will only be allowed to change the doors when he selects the manual mode button in the top right of the UI. 

The UI includes a spin box for the driver to change the status of the temperature. The spin box can be toggled upwards or downwards to increase or decrease the desired temperature within the train. The driver will only be allowed to change the temperature when he selects the manual mode button in the top right of the UI. 

h. Engineer 

The UI includes spin boxes for the engineer to change the status of the Kp and Ki values. The spin boxes can be toggled upwards or downwards to increase or decrease the desired Kp or Ki of the system. The engineer will only be allowed to change the Kp and Ki values when he inputs the correct password, which is located right above the spin boxes of the Kp and Ki values. 

## Demo
https://youtu.be/68byBlV1OcU

