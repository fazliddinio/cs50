"""
Sorting Algorithms Implementation
"""
from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Bubble Sort
    Time: O(n²) | Space: O(1)
    """
    n = len(arr)
    arr = arr.copy()
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    
    return arr


def selection_sort(arr: List[int]) -> List[int]:
    """
    Selection Sort
    Time: O(n²) | Space: O(1)
    """
    n = len(arr)
    arr = arr.copy()
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Insertion Sort
    Time: O(n²) | Space: O(1)
    """
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return arr


def merge_sort(arr: List[int]) -> List[int]:
    """
    Merge Sort
    Time: O(n log n) | Space: O(n)
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick Sort
    Time: O(n log n) avg, O(n²) worst | Space: O(log n)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr: List[int]) -> List[int]:
    """
    Heap Sort
    Time: O(n log n) | Space: O(1)
    """
    arr = arr.copy()
    n = len(arr)
    
    def heapify(n: int, i: int):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    
    return arr


def counting_sort(arr: List[int]) -> List[int]:
    """
    Counting Sort (for non-negative integers)
    Time: O(n + k) | Space: O(k) where k is range of input
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    for num in arr:
        count[num] += 1
    
    result = []
    for i, c in enumerate(count):
        result.extend([i] * c)
    
    return result


if __name__ == "__main__":
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    
    print(f"Original: {test_arr}")
    print(f"Bubble:   {bubble_sort(test_arr)}")
    print(f"Selection:{selection_sort(test_arr)}")
    print(f"Insertion:{insertion_sort(test_arr)}")
    print(f"Merge:    {merge_sort(test_arr)}")
    print(f"Quick:    {quick_sort(test_arr)}")
    print(f"Heap:     {heap_sort(test_arr)}")
    print(f"Counting: {counting_sort(test_arr)}")

# benchmark

# optimized
