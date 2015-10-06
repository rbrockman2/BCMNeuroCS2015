README.md

Run main.py to access the program.

This program models the behavior of a number of ion channels of different
types embedded in a cell membrane.  There can be a different number of ion
channels of each type.  Each ion channel type can also have different
voltage and temperature dependent kinetics.  Random opening and closing of
individual channels is modeled.

The model assumes that all of the channels in the membrane are clamped to the
same voltage throughout the simulation run.  The final output of the program
is a graph representing the membrane current as a function of time, with 
added gaussian noise.