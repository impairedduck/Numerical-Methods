#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:29:49 2025

@author: tylerhatch

Programming HW1, Problem 3
"""

# sorts list in ascending order
def bubble_sort(list):
    n = len(list)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if list[j] > list[j + 1]:
                # swap the elements in the list
                list[j], list[j + 1] =  list[j + 1], list[j]
                swapped = True
            
        if not swapped:
            break
    return list

# calculates average of list
def list_mean(list):
    return sum(list) // len(list)

# calculates median of list
def list_median(list):
    mid = int(len(list) // 2)
    # check if list is even in length
    if len(list) % 2:
        return list[int(mid)]
    else:
        return (list[mid] + list[mid - 1]) / 2
    
# calculates mode of list
def list_mode(list):
    frequency = {}
    
    for i in list:
        if i in frequency:
            frequency[i] += 1
        else:
            frequency[i] = 1
    maxCount = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == maxCount]
    return modes

# create list to sort
lst=[88, 12, 69, 71, 45, 31, 95, 56, 17, 17]

# display unsorted list
print("The list of integers is: " + str(lst))

# sort list and print
print("The sorted list is: " + str(bubble_sort(lst)))

# find average and print
print("The average of the list is: " + str(list_mean(lst)))

# find median and print
print("The median of this list is: " + str(list_median(lst)))

# find mode and print
print("The mode of this list is: " + str(list_mode(lst)[0]))






