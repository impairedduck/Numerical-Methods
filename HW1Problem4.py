#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:26:03 2025

@author: tylerhatch

Programming HW1, Problem 4
"""
import matplotlib.pyplot as plt
import numpy as np

g = 10
m = 10
c = 50
dt = 0.1
terminalVelocity = (g * m) / c
    

# part a

def velocity_one(t):
    output = terminalVelocity * (1 - np.exp(-(c / m) * t))
    return output 

# x and y values for plot
xValues = np.linspace(0, 2, 20)
# for loop to calculate y-axis values based on x-values
yValues = []
for i in xValues:
    yValues.append(velocity_one(i))
    

# label everything
plt.xlabel("Time (s)")
plt.ylabel("Veloity (m/s)")
plt.title("Velocity vs Time")
plt.plot(xValues, yValues, label="Part a", color="blue")



# part b
nSteps = int(2 / dt)
# create a list full of zeros to store values while iterating through the equation
v = np.zeros(nSteps)

# flag to ensure that the time to get to 99.99% of terminal velocity is collected once
flag = True
terminalTime = 0
# for-loop to iterate through the equation
for i in range(nSteps - 1):
    v[i+1] = v[i] + (g - (c/m) * v[i]) * dt
    
    # if statement to collect time it takes to reach terminal velocity
    if v[i] >= 0.9999 * terminalVelocity and flag == True:
        terminalTime = v[i]
        flag = False
    
# print the results of the previous if statement
print("The time to reach 99.99% the terminal velocity is " + str(terminalTime))

# create x-axis values for time
t = np.linspace(0, 2, nSteps)

# plot
plt.plot(t, v, label="Part b", color="orange")
plt.legend()






