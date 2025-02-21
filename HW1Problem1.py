#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 19:45:37 2025

@author: tylerhatch

Programming HW1, Problem 1
"""
from math import sqrt

# user input for values of a, b, and c
a = float(input("Value for a: "))
b = float(input("Value for b: "))
c = float(input("Value for c: "))

imaginaryRoots = False

if b ** 2 >= 4 * a * c:
    # roots when b^2 is greater than or equal to 4ac
    firstRoot = (-b + sqrt(b ** 2 -(4 * a * c))) / (2 * a)
    secondRoot = (-b - sqrt(b ** 2 -(4 * a * c))) / (2 * a)
    
    # round roots to 3 decimal places
    firstRoot = round(firstRoot, 3)
    secondRoot = round(secondRoot, 3)

elif b ** 2 < 4 * a * c:
    # when there are imaginary roots
    imaginaryRoots = True

# check for double and imaginary roots for print statemetns
if imaginaryRoots == True:
    print("There are no real roots")
else:
    if firstRoot != secondRoot:
        print("The first root is " + str(firstRoot))
        print("The second root is: " + str(secondRoot))
    elif firstRoot == secondRoot:
        print("The double roots are: " + str(firstRoot))

