"""Module with implementations of sorting algorithms as step generators."""
from typing import List, Tuple, Generator

def bubble_sort(data: List[int]) -> Generator[Tuple[List[int], List[int]], None, None]:
        """
        Step generator for Bubble sort algorithm.
        
        Args:
            data: a list of numbers to sort
        """
        n = len(data)
        for i in range(n):
            for j in range(n - i - 1):
                # Yield current state and highlighted bars
                yield data, [j, j+1], 'compare'
                if data[j] > data[j+1]:
                    # Swap elements
                    data[j], data[j+1] = data[j+1], data[j]
                    yield data, [j, j+1], 'swap'


def quick_sort(data: List[int]) -> Generator[Tuple[List[int], List[int]], None, None]:
    """Generator kroków dla QuickSort (wersja iteracyjna)"""
    stack = [(0, len(data) - 1)]
    while stack:
        low, high = stack.pop()
        pivot = data[high]
        i = low - 1
        yield data.copy(), [high], 'pivot'
        for j in range(low, high):
            yield data.copy(), [j, high], 'compare'
            if data[j] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                yield data.copy(), [i, j], 'swap'
        data[i+1], data[high] = data[high], data[i+1]
        yield data.copy(), [i+1, high], 'pivot'
        if low < i:
            stack.append((low, i))
        if i+2 < high:
            stack.append((i+2, high))


def selection_sort(data: List[int]) -> Generator[Tuple[List[int], List[int]], None, None]:
    """
    Step generator for selection sort algorithm.

    Args:
        data: a list of numbers to sort
    """
    n = len(data)

    for i in range(n):
        index_of_smallest = i
        for j in range(i + 1, n):
            yield data, [index_of_smallest, j]
            if data[j] < data[index_of_smallest]:
                index_of_smallest = j
        data[i], data[index_of_smallest] = data[index_of_smallest], data[i]

    yield data, [j, j+1]         
        
