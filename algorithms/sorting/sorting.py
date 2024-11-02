"""Sorting Algorithms"""
from typing import List

def bubble_sort(arr):
    """Bubble Sort - O(n^2)"""
    n = len(arr)
    arr = arr.copy()
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped: break
    return arr

# selection insertion
