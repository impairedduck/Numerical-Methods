#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 20:37:10 2025

@author: tylerhatch

Programming HW1, Problem 2
"""

import matplotlib.pyplot as plt
import numpy as np

# variables for different values in the equation
initial = 10
time = 20
decay = 0.01

# create 50 values of time in the range specified by the time variable
timeValues = np.linspace(0, time, 50)

# labeling axes
plt.xlabel("Time (s)")
plt.ylabel("Number of Radioactive Atoms")

# for loop to have different values of lambda
for i in range(4):
    radioativeAtoms = initial * np.exp(-decay * timeValues)
    # plot the result of the equation and label each curve 
    plt.plot(timeValues, radioativeAtoms,label=r"$\lambda = $%.2f" % decay)
    # multiply lambda value by 10 for the next iteration
    decay = decay * 10

# display the labels that I created for each value of lambda
plt.legend()

plt.title("Radioactive Decay with Varying $\lambda$")
plt.show()