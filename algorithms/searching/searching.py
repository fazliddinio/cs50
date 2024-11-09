"""
Searching Algorithms Implementation
"""
from typing import List, Optional


def linear_search(arr: List[int], target: int) -> int:
    """
    Linear Search
    Time: O(n) | Space: O(1)
    Returns index of target or -1 if not found
    """
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def binary_search(arr: List[int], target: int) -> int:
    """
    Binary Search (iterative)
    Time: O(log n) | Space: O(1)
    Array must be sorted
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(arr: List[int], target: int, left: int = None, right: int = None) -> int:
    """
    Binary Search (recursive)
    Time: O(log n) | Space: O(log n)
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_leftmost(arr: List[int], target: int) -> int:
    """
    Find leftmost (first) occurrence of target
    Time: O(log n) | Space: O(1)
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    if left < len(arr) and arr[left] == target:
        return left
    return -1


def binary_search_rightmost(arr: List[int], target: int) -> int:
    """
    Find rightmost (last) occurrence of target
    Time: O(log n) | Space: O(1)
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    if left > 0 and arr[left - 1] == target:
        return left - 1
    return -1


def jump_search(arr: List[int], target: int) -> int:
    """
    Jump Search
    Time: O(√n) | Space: O(1)
    Array must be sorted
    """
    n = len(arr)
    step = int(n ** 0.5)
    prev = 0
    
    # Jump to find block
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return -1
    
    # Linear search in block
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return -1
    
    if arr[prev] == target:
        return prev
    return -1


def exponential_search(arr: List[int], target: int) -> int:
    """
    Exponential Search
    Time: O(log n) | Space: O(1)
    Good for unbounded searches
    """
    if not arr:
        return -1
    
    if arr[0] == target:
        return 0
    
    # Find range for binary search
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2
    
    # Binary search in range
    left = i // 2
    right = min(i, len(arr) - 1)
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def interpolation_search(arr: List[int], target: int) -> int:
    """
    Interpolation Search
    Time: O(log log n) for uniform distribution, O(n) worst
    Space: O(1)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        if left == right:
            if arr[left] == target:
                return left
            return -1
        
        # Estimate position
        pos = left + ((target - arr[left]) * (right - left) // (arr[right] - arr[left]))
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return -1


if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 11
    
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print()
    print(f"Linear search:      {linear_search(arr, target)}")
    print(f"Binary search:      {binary_search(arr, target)}")
    print(f"Binary (recursive): {binary_search_recursive(arr, target)}")
    print(f"Jump search:        {jump_search(arr, target)}")
    print(f"Exponential search: {exponential_search(arr, target)}")
    print(f"Interpolation:      {interpolation_search(arr, target)}")
    
    # Test leftmost/rightmost
    arr2 = [1, 2, 2, 2, 3, 4, 5]
    print(f"\nArray with duplicates: {arr2}")
    print(f"Leftmost 2:  {binary_search_leftmost(arr2, 2)}")
    print(f"Rightmost 2: {binary_search_rightmost(arr2, 2)}")

# large test
