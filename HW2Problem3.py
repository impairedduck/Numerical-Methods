#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:15:03 2025

@author: tylerhatch

HW2 Problem 3
"""
import numpy as np

# function to perform LU decomposition with partial pivoting given an A matrix
def lu_decomposition(A, tol=1e-10):
    n = A.shape[0]
    
    # make a copy of A
    A = A.copy()
    
    # permutation array
    P_idx = np.arange(n)
    
    # create L and U matrix
    L = np.eye(n)
    U = np.zeros((n, n))
    
    # lu decomposition from pesudo code
    for k in range (n-1):
        # find pivot
        pivot_idx = k + np.argmax(np.abs(A[k:n, k]))
        max_val = np.abs(A[pivot_idx, k])
        
        # swap rows if necessary 
        if pivot_idx != k:
            A[[k, pivot_idx]] = A[[pivot_idx, k]]
            P_idx[[k, pivot_idx]] = P_idx[[pivot_idx, k]]
            
            # swap already calcualted parts of L
            if k > 0:
                L[[k, pivot_idx], :k] = L[[pivot_idx, k], :k]
              
        # multipliers
        for i in range(k+1, n):
            L[i, k] = A[i, k] / A[k, k]
            
            # update A matrix
            A[i, k:] = A[i, k:] - L[i, k] * A[k, k:]
            
    # create the U matrix from the modified A matrix
    for i in range(n):
        for j in range(i, n):
            U[i, j] = A[i, j]
            
    # create permutation matrix from the permutation array
    P = np.zeros((n, n))
    for i in range(n):
        P[i, P_idx[i]] = 1
    return L, U, P
            

# function for forward subsitiution using logic from pseudo code
def forward_substitution(L, b):
    # defining shape based on size of L
    n = L.shape[0]
    y = np.zeros(n)
    
    for i in range(n):
        sum_val = 0
        for j in range(i):
            sum_val += L[i, j] * y[j]
        y[i] = (b[i] - sum_val)  # L has 1's on diagonal
    return y
            
# function for backward subsitution based on logic from pseudo code
def back_substitution(U, y):
    n = U.shape[0]
    x = np.zeros(n)
    
    for i in range(n-1, -1, -1):
        sum_val = 0
        for j in range(i+1, n):
            sum_val += U[i, j] * x[j]
        x[i] = (y[i] - sum_val) / U[i, i]
    return x
    
# function to calculate the inverse of a matrix using previous functions
def matrix_inverse(A):
    n = A.shape[0]
    
    # perform LU decomposition
    L, U, P = lu_decomposition(A)
    
    # solve for each column of the inverse
    A_inv = np.zeros((n, n))
    
    for j in range(n):
        e = np.zeros(n)
        e[j] = 1
        
        # permutation to e
        b = P @ e
        
        # solving Ly = Pb
        y = forward_substitution(L, b)
        
        # solving Ux = y
        x = back_substitution(U, y)
        
        A_inv[:, j] = x
    return A_inv
            
# get matrix size from user input
n = int(input("Enter the size of the matrix (NxN): "))   
 
# user input to create matrix       
print("\nEnter the elements of the matrix row by row:")
A = np.zeros((n, n))

# for loop to get input for each value in matrix
for i in range(n):
    row_input = input(f"Row {i+1}: ")
    row_values = [float(x) for x in row_input.split()]
    A[i] = row_values

# display A matrix
print("Your matrix is: ")
print(A)

#display inverted matrix
inverseA = matrix_inverse(A) 
print("The inverted matrix is: ")
print(inverseA)
            
# using numpy function to check accuracy
correctA = np.linalg.inv(A)
print("The correct output is: ")
print(correctA)
            
            
            
            
            
            
            
            
            