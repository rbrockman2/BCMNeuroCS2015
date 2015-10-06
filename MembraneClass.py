# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 2015

@author: The Entire First Year Neuroscience Graduate Student Contingent
    (plus Elizabeth Lackey from second year, of course)

BCM Computation for Neuroscience Fall 2015

Final Group Assignment
"""
import matplotlib.pyplot as plot
from ChannelClass import Channel
import numpy as np
debug = False


class Membrane():
    """This class represents a membrane which can have multiple types of
    channels embedded in it.

    Uday and Kim spearheaded writing this class.
    """
    def __init__(self):
        """This function creates an instance of the membrane class with
        our default membrane properties. User will also have option to set the
        parameters. Temperature is in Kelvin. Times are in msec."""
        self.channel_set = []
        self.Vm = -65  # mV
        self.T = 310  # K
        self.simulation_time = 100  # ms
        self.dt = 0.01  # ms
        self.noise_amp = 1E-13  # scale factor for added Gaussian noise

    def get_membrane_parameters(self):
        """This function will set either set the properties of the membrane
        to default values or will allow the user to set them."""
        UseDefaultYN = input("Would you like to use defaults for Vm,\
 temperature, simulation time and time step (dt)? (y/N): ")
        if UseDefaultYN.lower() != 'y':
            IsMembraneVoltageVerified = False
            while IsMembraneVoltageVerified is False:
                membraneVoltageStr = input("At what voltage would you like to\
 clamp the membrane (mV)?: ")
                try:
                    self.Vm = float(membraneVoltageStr)
                except ValueError:
                    print("Error: Membrane voltage must be a number.")
                else:
                    if self.Vm < -200 or self.Vm > 400:
                        print("Warning: Membrane voltage is outside -200mV to\
 400mV range.")
                        IsItOK = input("Is this OK? (y/N): ")
                        if IsItOK.lower() == 'y':
                            IsMembraneVoltageVerified = True
                        else:
                            IsMembraneVoltageVerified = False
                    else:
                        IsMembraneVoltageVerified = True

            IsTempVerified = False
            while IsTempVerified is False:
                Temperature = input("Enter Temperature (0K - 400K): ")
                try:
                    self.Temp = int(Temperature)
                except ValueError:
                    print("Error: Temperatures are outside expected range\
 (0K - 400K).")
                else:
                    if self.Temp < 0 or self.Temp > 400:
                        print("Error: Temperatures are outside expected range\
 (0K - 400K).")
                    else:
                        IsTempVerified = True

            IsSimTimeVerified = False
            while IsSimTimeVerified is False:
                SimTime = input("Enter Total Simulation Time (msec): ")
                try:
                    self.simulation_time = int(SimTime)
                except ValueError:
                    print("Error: Simulation Time was not entered as a\
 positive integer.")
                else:
                    if self.simulation_time <= 0:
                        print("Error: Simulation Time was not entered as a\
 positive integer.")
                    else:
                        IsSimTimeVerified = True

            IsDtVerified = False
            while IsDtVerified is False:
                dtStep = input("Enter time step (dt) (should be <1msec): ")
                try:
                    self.dt = float(dtStep)
                except ValueError:
                    print("Error: time step was not entered as a positive\
 integer.")
                else:
                    if self.dt <= 0:
                        print("Error: time step was not entered as a positive\
 integer.")
                    elif self.dt > self.simulation_time:
                        print("Error: time step entered is longer than\
 simulation time.")
                    else:
                        IsDtVerified = True

    def create_channel_set(self, **input_dict):
        '''Takes a dictionary of dictionaries as input. If the input is empty,
        query user for more information. If the input has a channel object as a
        dictionary entry, appends the channel object to channel_set.'''
        if len(input_dict) == 0:
            more_channels = True
            while more_channels is True:
                self.channel_set.append(Channel())
                continue_query = input("Add more channels?  (y/N): ")
                if continue_query.lower() == 'y':
                    more_channels = True
                else:
                    more_channels = False
        else:
            for channel_name, channel_obj in input_dict.items():
                self.channel_set.append(channel_obj)

    def compute_current(self):
        """This function calculates the time series of membrane current values
        by adding together the time series of current values for each channel
        type
        """
        total_current_TS = []

        for channel in self.channel_set:
            # Calculate channel current object time series.
            channel_current_TS_local =\
                channel.compute_current_TS(self.Vm, self.simulation_time,
                                           self.dt, self.T)
            if total_current_TS == []:
                total_current_TS = channel_current_TS_local
            else:
                # Add series from single channel type to total.
                # Time series are converted to lists to maintain type
                #   consistency.
                total_current_TS = np.add(total_current_TS,
                                          channel_current_TS_local).tolist()
        return total_current_TS

    @staticmethod
    def add_noise(time_series, noise_amp):
        """This function adds noise to a time series to make it more
        biologically realistic.

        Inputs:
            time_series:  a list of values that need Gaussian noise to be added
            noise_amp:  scale factor for additive Gaussian noise

        Outputs:
            array of channel_data with noise added

        Worked on by:  Gabe S. and Elizabeth L.
        """
        # Use numpy to create Gaussian noise.
        noise = np.random.normal(size=len(time_series))
        scaled_noise = noise * noise_amp  # Scale noise.
        noisy_TS = np.add(time_series, scaled_noise).tolist()  # Add noise.
        return noisy_TS

    @staticmethod
    def plot_current_TS(current_TS, dt=1E5):
        """
        Plots a current time series.

        Inputs:
            current_TS:  a list of current values in amps
            dt: the time step size for the current time series in ms

        Worked on by:  Gabe and Carli.
        """
        if debug is True:
            print("Time Step in ms:  {0}".format(dt))
            print("Length of the time series:  {0}".format(len(current_TS)))

        # Create x_axis list of time values.
        x_axis = []
        i = 0
        idx = 0
        while idx < len(current_TS):
            x_axis += [i]
            i += dt
            idx += 1

        # Convert y_axis list of current values to nanoamps for display.
        nano_current = []
        for item in current_TS:
            item = item*(10**9)  # Convert to nanoamps for graph prettiness.
            nano_current += [item]
        y_axis = nano_current

        if debug is True:
            print("y_axis length:  {0}".format(len(y_axis)))
            print("x_axis length:  {0}".format(len(x_axis)))

        plot.plot(x_axis, y_axis, label='time', color='maroon',
                  linestyle='-')
        plot.xlabel('Time (ms)')
        plot.ylabel('Net current (nA)')
        plot.title('Membrane Current Time Series')
        plot.grid()
        plot.show()

    def make_plot(self):
        """Computes and plots the membrane current time series including
        Gaussian noise."""
        current_TS = self.compute_current()
        noisy_TS = Membrane.add_noise(current_TS, self.noise_amp)

        Membrane.plot_current_TS(noisy_TS, self.dt)
