#################################################################################################################################
# Unnamed TA Simulator
# Version 1.0
# Author: ASARG
# Description: Implements the tile automata model as designed by Angel Cantu, Austin Luchsinger, Robert Schweller, and Tim Wylie.
#################################################################################################################################
# Unnamed TASimulator Manual

Table of Contents
Sections
1 - Application
2 - Models Overview
3 - File I/O
4 - Feature Map
5 - Change Log


#############################
Section 1 - Application

## 1.1 Requirements
  Required:
    -Python 3+
    -PyQt5 (install using pip)
  Optional:


## 1.2 Usage
  Running:
    >python3 general_TA_simulator.py


## 1.3 Menu Overview
Main Menu
 + File
    - New 
    - Load
    - Save As
    - Exit
 + Tools
    - Edit
    - Rotate
    - Combine
    - Slow Mode
    - Time Elapsed
 + Available Moves
    - 
 + Papers
    - 
    
## 1.4 Menu Functions
1.4.1 File Menu
1.4.1.1 New
  This menu option opens the editor so you may begin making a new system.
  
1.4.1.2 Load
  This menu option will prompt the user for a file and then attempt to open it. 

  The application will only load XML files.
  
1.4.1.3 Save As . . .
  This menu option will prompt the user for a file name and location to log the information to. It will overwrite a file if it already exists.

1.4.1.4 Exit
  This closes the application.

1.4.2 Tools Menu
1.4.2.1 Edit
  When clicked, opens the editor with the current system loaded.
  
1.4.2.2 Rotate
  Rotates the current system
  
1.4.2.3 Combine
  Prompts the user to select a valid file and attempts to combine the system in the file with the current loaded system
  
1.4.2.4 Slow Mode
  This is a radio button that, when selected, adds a brief delay in between steps while the play option is selected.

1.4.2.5 Time Elapsed
  This is just text that shows the user how many "time steps" have occured at the current step.

1.4.3 Available Moves
1.4.3.1 

1.4.4 Papers
1.4.4.1
  
## 1.3 Controls
  Once a system is loaded: 
  -WASD will move the assembly
  -The mouse scroll wheel can zoom in and out
  -J will show you the previous step of an assembly
  -K will press "play" to simulate what a system would do
  -L will show you the next step of the assembly

  you can also use the toolbar buttons, which include:
  -First 
  -Previous
  -Play/Pause
  -Next
  -Last

#############################
Section 2 - Models Overview

## 2.1 Basic Model
## 2.2 Freezing Model
## 2.3 Non-Freezing Model

#############################
Section 3 - File I/O

3.1 XML format
  The editor can create an XML file for you, but should you desire to check or build your own XML file an example simple system XML file is shown below. 
  
  ****DESCRIPTION OF XML FILE HERE****

EXAMPLE:
    <?xml version='1.0' encoding='utf-8'?>
<System Temp="1">
	<AllStates>
		<State Label="A" Color="f03a47" />
		<State Label="B" Color="3f88c5" />
		<State Label="C" Color="323031" />
	</AllStates>
	<InitialStates>
		<State Label="A" Color="f03a47" />
		<State Label="B" Color="3f88c5" />
	</InitialStates>
	<SeedStates>
		<State Label="A" Color="f03a47" />
	</SeedStates>
	<VerticalTransitions>
		<Rule Label1="A'" Label2="B" Label1Final="A'" Label2Final="A" />
	</VerticalTransitions>
	<HorizontalTransitions>
		<Rule Label1="B" Label2="B" Label1Final="B" Label2Final="C" />
	</HorizontalTransitions>
	<VerticalAffinities>
		<Rule Label1="A" Label2="B" Strength="1" />
	</VerticalAffinities>
	<HorizontalAffinities>
		<Rule Label1="B" Label2="B" Strength="1" />
	</HorizontalAffinities>
</System>
    
#############################
Section 4 - Feature Map
  -Add companion papers to section
  -Adding list of available moves
    



#############################
Section 5 - Changelog

## 5.1 Version 1.0
    - Initial version distributed to others
    
