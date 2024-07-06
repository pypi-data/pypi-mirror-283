
def quicksort(numbers):
    """
    Sorts a list of numbers using the quicksort algorithm.
    
    :param numbers: List of numbers to sort
    :return: Sorted list of numbers
    """
    if len(numbers) <= 1:
        return numbers
    pivot = numbers[len(numbers) // 2]
    left = [x for x in numbers if x < pivot]
    middle = [x for x in numbers if x == pivot]
    right = [x for x in numbers if x > pivot]
    return quicksort(left) + middle + quicksort(right)
