# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 2015

@author: Dr. Paul and Robert Theron Brockman II

BCM Computation for Neuroscience Fall 2015

Final Group Assignment

"""

from MembraneClass import Membrane

if __name__ == "__main__": 
    myMembrane = Membrane()
    myMembrane.get_membrane_parameters()
    myMembrane.create_channel_set()
    myMembrane.make_plot()
    