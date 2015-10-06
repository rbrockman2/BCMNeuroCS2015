# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 2015

@author: The Entire First Year Neuroscience Graduate Student Contingent
    (plus Elizabeth Lackey from second year, of course)

BCM Computation for Neuroscience Fall 2015

Final Group Assignment
"""
from MembraneClass import Membrane

if __name__ == "__main__":
    myMembrane = Membrane()
    myMembrane.get_membrane_parameters()
    myMembrane.create_channel_set()
    myMembrane.make_plot()
