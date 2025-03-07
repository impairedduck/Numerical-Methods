#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:13:35 2025

@author: tylerhatch

HW2: Problem: 1
"""
import numpy as np
import matplotlib.pyplot as plt

# function to evaluate given input with colebrook equation
def colebrook_equation(f, Re, epsilon, D):
    # converting epsilon  from mm to m
    epsilonM = epsilon / 1000
    
    # returns colebrook equation
    return 1/np.sqrt(f) + 2 * np.log10(epsilonM / (3.7 * D) + 2.51 / (Re * np.sqrt(f)))


# secant method to determine f
def secant_method(Re, epsilon, D, f0=0.02, f1=0.01, maxIter=100, tol=1e-6):
    for i in range(maxIter):
        # evaluate the colebrook equation at the two initial guesses
        func_f0 = colebrook_equation(f0, Re, epsilon, D)
        func_f1 = colebrook_equation(f1, Re, epsilon, D)
        
        # check for division by 0
        if func_f1 - func_f0 == 0:
            return f1, i
        
        # formula for secant method to calculate next iteration
        fNew = f1 - (func_f1 * (f0 - f1)) / (func_f0 - func_f1)
        
        # check for convergence
        if abs(fNew - f1) < tol:
            return fNew, i + 1
        
        # update values for next iteration
        f0, f1 = f1, fNew
        
        # if max iterations are reached, return best answer
    return f1, maxIter

# function to calculate friction factor using the Swamee-Jain equation
def swamee_jain(Re, epsilon, D):
    # convert epsilon from mm to m
    epsilon_m = epsilon / 1000
    return 1.325 / ((np.log(epsilon_m/(3.7*D) + 5.74/(Re**0.9)))**2) 

# function to calculate friction factor for a range of Re and D
def friction_factor(epsilon):
    ReValues = np.logspace(4, 6, 20) # 20 points ranging from 10^4 to 10^6
    Dvalues = np.logspace(-1, 1, 20) 
    
    # creating lists to store data
    ReList = []
    DList = []
    fList = []
    
    # initialize 2D arrays for friction factors for contour plotting
    colebrookFriction = np.zeros((len(ReValues), len(Dvalues)))
    swameeJainFriction = np.zeros((len(ReValues), len(Dvalues)))
    
    # calculating friction factor for Re and D
    for i, Re in enumerate(ReValues):
        for j, D in enumerate(Dvalues):
            # colebrook equation using secant method
            f_colebrook, _ = secant_method(Re, epsilon, D)
            
            # store in 2D array for contour plotting
            colebrookFriction[i, j] = f_colebrook
            
            # save values in lists
            ReList.append(Re)
            DList.append(D)
            fList.append(f_colebrook)
            
            # Swamee-Jain equation
            f_swamee_jain = swamee_jain(Re, epsilon, D)
            swameeJainFriction[i, j] = f_swamee_jain
    
    return ReList, DList, fList, ReValues, Dvalues, colebrookFriction, swameeJainFriction

def pressure_gradient(Q, D, epsilon, rho, mu):
    # velocity from flow rate:
    V = Q / (np.pi * D**2 / 4)
    
    # reynold's number
    Re = rho * V * D / mu
    
    # calculate friction factor using Swamee Jain equation
    f = swamee_jain(Re, epsilon, D)
    
    # calcualting pressure gradient
    pressureGradient = f * (2 * rho / (np.pi**2 * D**3)) * Q**2
    return pressureGradient, Re, f

# constants
epsilon = 0.003 # in mm
D = 2
rho = 1000
mu = 1e-3
g = 9.81


ReList, DList, fList, ReValues, Dvalues, colebrookFriction, swameeJainFriction = friction_factor(epsilon)

# printing results
print("\nResults:")
print("Reynolds Number | Diameter (m) | Friction Factor")
print("-" * 50)
for i in range(len(ReList)):
    print(f"{ReList[i]:.2e} | {DList[i]:.4f} | {fList[i]:.6f}")

# printing other relevant statistics
print("\nStatistics: ")
print("Number of calculations: " + str(len(fList)))
print("Minimum f value: " + str(min(fList)))
print("Maximum f value:" + str(max(fList)))



# plotting for part b to follow:
Re_grid, D_grid = np.meshgrid(ReValues, Dvalues, indexing="ij")

# create figure and adjust subplot layout
fig = plt.figure(figsize=(12, 6))
fig.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.8, wspace=0.4, hspace=0.1)

# plot friction factor from Colebrook equation
plt.subplot(121)
contour = plt.contourf(Re_grid, D_grid, colebrookFriction, cmap="viridis")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Reynolds Number (Re)")
plt.ylabel("Pipe Diameter (m)")
plt.title("Friction Factor vs. Reynolds Number")
plt.clim(-0.01, 0.035)

# plot friction factor from Swamee-Jain equation
plt.subplot(122)
plt.contourf(Re_grid, D_grid, swameeJainFriction, cmap="viridis")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Reynolds Number (Re)")
plt.ylabel("Pipe Diameter (m)")
plt.title("Swamee-Jain Friction Factor vs. Reynolds Number")
plt.clim(-0.01, 0.035)

# add legend
cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])
cbar = fig.colorbar(contour, cax=cbar_ax)
cbar.set_label("Friction Factor (f)")

# calculations for part c
# creating values of Q for plotting
Qvalues = np.linspace(0.1, 30, 100)

# calcualting the pressure gradient for different values of flow rate
ReValues = []
fValues = []
pressureGradients = []

# add values to lists for all Q values
for Q in Qvalues:
    pressure_gradient_value, Re, f = pressure_gradient(Q, D, epsilon, rho, mu)
    pressureGradients.append(pressure_gradient_value)
    ReValues.append(Re)
    fValues.append(f)


# convert lists to numpy arrays for plotting
pressureGradients = np.array(pressureGradients)
ReValues = np.array(ReValues)
fValues = np.array(fValues)

# plot pressure gradient vs flow rate
plt.figure(figsize=(10, 6))
plt.plot(Qvalues, pressureGradients)
plt.xlabel('Volume Flow Rate, Q (m³/s)')
plt.ylabel('Pressure Gradient, ΔP/L (Pa/m)')
plt.title('Pressure Gradient vs. Flow Rate')
plt.grid(True)

# add a second y-axis for Reynolds number
ax2 = plt.gca().twinx()
ax2.plot(Qvalues, ReValues, 'r--')
ax2.set_ylabel('Reynolds Number (Re)', color='r')
ax2.tick_params(axis='y', labelcolor='r')





















