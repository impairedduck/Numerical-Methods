#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:12:55 2025

@author: tylerhatch

Programming Homework 4
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_derivatives(u, v, D, m, A, rhoAir, nuAir, g):
    # avoid division by zero with velocity magnitude
    vel = np.sqrt(u**2 + v**2)
    if vel < 1e-10:
        vel = 1e-10
    
    # calculate Reynolds number
    Re = vel * D / nuAir
    if Re < 1e-10:
        Re = 1e-10
    
    # Drag coefficient
    Cd = 24 / Re + 1.5
    
    # calculate derivatives with proper drag force direction
    # drag is proportional to velocity magnitude * velocity direction
    du_dt = -0.5 * Cd * rhoAir * A * vel * u / m
    
    # for vertical motion, include buoyancy
    buoyancy_term = g * (1.0 - (np.pi/6) * rhoAir * D**3 / m)
    # make sure buoyancy doesn't cause nan
    if not np.isfinite(buoyancy_term):
        buoyancy_term = 0
        
    dv_dt = -0.5 * Cd * rhoAir * A * vel * v / m + buoyancy_term
    
    du_dt = -0.5 * Cd * rhoAir * A * vel * u / m
    if not np.isfinite(du_dt):
        du_dt = 0
    
    return du_dt, dv_dt


def rk4(u, v, dt, D, m, A, rhoAir, nuAir, g):
    # step 1
    k1u, k1v = calculate_derivatives(u, v, D, m, A, rhoAir, nuAir, g)
    
    # step 2
    k2u, k2v = calculate_derivatives(u + 0.5 * dt * k1u, 
                                     v + 0.5 * dt * k1v, 
                                     D, m, A, rhoAir, nuAir, g)
    
    # step 3
    k3u, k3v = calculate_derivatives(u + 0.5 * dt * k2u, 
                                     v + 0.5 * dt * k2v, 
                                     D, m, A, rhoAir, nuAir, g)
    
    # step 4
    k4u, k4v = calculate_derivatives(u + dt * k3u, 
                                     v + dt * k3v, 
                                     D, m, A, rhoAir, nuAir, g)
    
    # update variables with new k values
    uNew = u + (dt/6.0) * (k1u + 2*k2u + 2*k3u + k4u)
    vNew = v + (dt/6.0) * (k1v + 2*k2v + 2*k3v + k4v)
    
    return uNew, vNew
    
    
def solve_ODE(D, initialVelocity, dt, tEnd, height = 1.8):
    # constants
    rhoWater = 1000 # kg/m^3
    rhoAir = 1.293 # kg/m^3
    nuAir = 1.5e-5 # m^2/s
    g = 9.81 # m/s^2    
    
    # particle variables
    m = (np.pi/6) * rhoWater * D**3
    A = np.pi * D**2 / 4
    
    # initial conditions
    u0 = initialVelocity
    v0 = 0
    x0 = 0
    y0= height
    
    # array to store results
    nSteps = int(tEnd / dt) + 1
    t = np.zeros(nSteps)
    u = np.zeros(nSteps)
    v = np.zeros(nSteps)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    
    # initial values of arrays
    t[0] = 0
    u[0] = u0
    v[0] = v0
    x[0] = x0
    y[0] = y0
    
   # iterate through RK4
    i = 0
    while i < nSteps - 1 and y[i] > 0:  # iterate until particle hits ground
        u[i + 1], v[i + 1] = rk4(u[i], v[i], dt, D, m, A, rhoAir, nuAir, g)
        
        # update positions
        x[i + 1] = x[i] + u[i + 1] * dt
        y[i + 1] = y[i] - v[i + 1] * dt  
        
        t[i + 1] = t[i] + dt
        i += 1
     
  # change arrays to the actual simulation length if ended early
    if i < nSteps - 1:
        t = t[:i+1]
        u = u[:i+1]
        v = v[:i+1]
        x = x[:i+1]
        y = y[:i+1]
    
    return t, u, v, x ,y

def verify_stability():
    # parameters
    D = 32e-6 # micrometers
    initialVelocity = 10 # m/s
    tEnd = 5 # seconds

    # different time steps to test for convergence
    dtValues = [1e-2, 1e-3, 1e-4]
    
    # plotting the results
    plt.figure(figsize=(12, 10))
    
    # plotting results u and v vs time
    plt.subplot(2, 2, 1)
    for dt in dtValues:
        t, u, v, x, y = solve_ODE(D, initialVelocity, dt, tEnd)
        plt.plot(t, u, label=f'dt = {dt}')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Horizontal Velocity (m/s)')
    plt.title('Horizontal Velocity vs Time')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Vertical velocity over time
    plt.subplot(2, 2, 2)
    for dt in dtValues:
        t, u, v, x, y = solve_ODE(D, initialVelocity, dt, tEnd)
        plt.plot(t, v, label=f'dt = {dt}')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Vertical Velocity (m/s)')
    plt.title('Vertical Velocity vs Time')
    plt.legend()
    plt.grid(True)
    
# generate results for part 1
verify_stability()

# properties of aerosols
diameters = [1, 2, 4, 8, 16, 32, 64, 128]
velocities = [1.5, 10, 20, 30, 40]

# conditions for iterations
dt = 1e-4
tEnd = 10

print("\nDISTANCE TRAVELED BEFORE HITTING FLOOR (meters)")
print("Size (μm) | 1.5 m/s | 10 m/s | 20 m/s | 30 m/s | 40 m/s")
print("-" * 65)

for d in diameters:
    d_m = d * 1e-6  # meters
    distances = []
        
    for v in velocities:
        _, _, _, x, y = solve_ODE(d_m, v, dt, tEnd)
        distances.append(x[-1])
            
    print(f"{d:8} | {distances[0]:7.3f} | {distances[1]:6.3f} | {distances[2]:6.3f} | {distances[3]:6.3f} | {distances[4]:6.3f}")
print("\nTIME TO REACH FLOOR (seconds)")
print("Size (μm) | 1.5 m/s | 10 m/s | 20 m/s | 30 m/s | 40 m/s")
print("-" * 65)
    
for d in diameters:
    d_m = d * 1e-6  # meters
    times = []
    
    for v in velocities:
        t, _, _, _, _ = solve_ODE(d_m, v, dt, tEnd)
        times.append(t[-1])
            
    print(f"{d:8} | {times[0]:7.3f} | {times[1]:6.3f} | {times[2]:6.3f} | {times[3]:6.3f} | {times[4]:6.3f}")

    
# extra credit
def solve_extra_credit():
    # parameters
    diameters = [1, 16, 128]
    velocities = [1.5, 20, 40]  
    angles = np.linspace(0, 90, 10)
    dt = 1e-4
    tEnd = 10
    
    print("\nPART 5: OPTIMAL ANGLE FOR MAXIMUM DISTANCE")
    print("Size (μm) | 1.5 m/s | 20 m/s | 40 m/s")
    print("-" * 45)
    
    for d in diameters:
        d_m = d * 1e-6  # meters
        max_distance_angles = []
        
        for v in velocities:
            max_distance = 0
            best_angle = 0
            
            for angle in angles:
                # radians
                angle_rad = np.deg2rad(angle)
                
                # initial velocity calculations
                u0 = v * np.cos(angle_rad)
                v0 = v * np.sin(angle_rad)
                
                # change solve_ODE to use angles
                try:
                    _, _, _, x, y = solve_ODE(d_m, u0, dt, tEnd)
                    
                    # check if this angle gives better distance
                    if x[-1] > max_distance:
                        max_distance = x[-1]
                        best_angle = angle
                except:
                    pass  # skip failed calculations
            
            max_distance_angles.append(best_angle)
            
        print(f"{d:8} | {max_distance_angles[0]:7.1f}° | {max_distance_angles[1]:6.1f}° | {max_distance_angles[2]:6.1f}°")
    
    print("\nPART 5: OPTIMAL ANGLE FOR MAXIMUM TIME IN AIR")
    print("Size (μm) | 1.5 m/s | 20 m/s | 40 m/s")
    print("-" * 45)
    
    for d in diameters:
        d_m = d * 1e-6  # meters
        max_time_angles = []
        
        for v in velocities:
            max_time = 0
            best_angle = 0
            
            for angle in angles:
                # radians
                angle_rad = np.deg2rad(angle)
                
                # initial velocity calculations
                u0 = v * np.cos(angle_rad)
                v0 = v * np.sin(angle_rad)
                
                # modify solve_ODE to handle angled initial velocity
                try:
                    t, _, _, _, _ = solve_ODE(d_m, u0, dt, tEnd)
                    
                    # check if this angle gives better time
                    if t[-1] > max_time:
                        max_time = t[-1]
                        best_angle = angle
                except:
                    pass
            
            max_time_angles.append(best_angle)
            
        print(f"{d:8} | {max_time_angles[0]:7.1f}° | {max_time_angles[1]:6.1f}° | {max_time_angles[2]:6.1f}°")

# call the function to execute part 5
solve_extra_credit()









    