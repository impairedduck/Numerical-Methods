#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:14:18 2025

@author: tylerhatch

HW2: Problem: 2

Gauss Elimination with Pivoting
"""

import numpy as np

# function to locate pivot
def pivot(a, b, s, n, k):
    p = k
    big = abs(a[k, k] / s[k])
    
    # search through rows to find the largest pivot
    for i in range(k + 1, n):
        dummy = abs(a[i, k] / s[i])
        if dummy > big: 
            big = dummy
            p = i
    
    # if the row with the pivot is not the current row, then swap them
    if p!= k:
        for j in range(k, n):
            dummy = a[p, j]
            a[p, j] = a[k, j]
            a[k, j] = dummy
    
    # swap elements in b vector too
    dummy = b[p]
    b[p] = b[k]
    b[k] = dummy
    
    # scaling factor
    dummy = s[p]
    s[p] = s[k]
    s[k] = dummy
    return p


# function to perform forward elimination
def eliminate(a, s, n, b, tol, er):
    er = 0
    
    for k in range(n-1):
        # check pivot
        pivot(a, b, s, n, k)
        
        # check for singular matrix
        if abs(a[k, k] / s[k]) < tol:
            er = -1
            return er
        
        # eliminate numbers below the pivot 
        for i in range(k + 1, n):
            factor = a[i, k] / a[k, k]
            
            # update the other rows
            for j in range(k+1, n):
                a[i, j] = a[i, j] - factor * a[k, j]
                
            # update b vector
            b[i] = b[i] - factor * b[k]
            
    if abs(a[n-1, n-1] / s[n-1]) < tol:
        er = -1
        
    return er

# function to perform backward substitution
def substitute(a, n, b, x):
    x[n-1] = b[n-1] / a[n-1, n-1]
    
    # back substiution
    for i in range(n-2, -1, -1):
        sum_val = 0
        
        # calculate the sum value 
        for j in range(i + 1, n):
            sum_val = sum_val + a[i, j] * x[j]

    # solving for new variable
    x[i] = (b[i] - sum_val) / a[i, i]
    
    return


# function to solve the system
def gauss(a, b, n, x, tol=1e-10):
    # copy the original matrix
    aCopy = a.copy()
    bCopy = b.copy()
    
    s = np.zeros(n)
    er = 0
    
    # scaling factor for each row
    for i in range(n):
        s[i] = abs(aCopy[i, 0])
        for j in range(1, n):
            if abs(aCopy[i, j]) > s[i]:
                s[i] = abs(aCopy[i, j])
                
    # call the elimination function
    er = eliminate(aCopy, s, n, bCopy, tol, er)


    # if not singular, do the backwards substitution
    if er != -1:
        substitute(aCopy, n, bCopy, x)
        
    return er

# user input for size of matrix
n = int(input("Enter size of matrix (nxn): "))

# creating the matrix specified by user to be filled with values
a = np.zeros((n, n))
b = np.zeros(n)
x = np.zeros(n)

# user input for the numbers in the matrix
print("Enter the coefficents of the matrix: ")

# first loop for the rows
for i in range(n):
    # second loop for the columns
    for j in range(n):
        a[i, j] = float(input(f"a[{i+1},{j+1}]: "))
        
        
print("Enter the values in the b matrix:")
for i in range(n):
    b[i] = float(input(f"b[{i+1}]: "))
    

er = gauss(a,b,n,x)

# print results

if er == 1:
    print("The matrix is singular, it can't be solved")
else:
    print("Solution")
    for i in range(n):
        print(f"x[{i+1}] = {x[i]}")


# check to see if solution is correct
# 10x10 matrix
A = np.array([
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [11,12,13,14,15,16,17,18,19,20],
    [10,9,8,7,6,5,4,3,2,1],
    [20,19,18,17,16,15,14,13,12,11],
    [20,21,22,23,24,25,26,27,28,29],
    [1,2,3,4,5,6,7,8,9,10],
    [10,9,8,7,6,5,4,3,2,1],
    [30,31,32,33,34,35,36,37,38,39],
    [40,41,42,43,44,45,46,47,48,49],
    [1,2,3,4,5,6,7,8,9,10]
])


b = np.array([1, 6, 5, 3, 8, 9, 7, 5, 4, 7])

x = np.linalg.solve(A, b)
print("Numpy function Solution:")
print(x)









