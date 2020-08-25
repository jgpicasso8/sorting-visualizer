def swap(A, i, j):
    """Helper function to swap elements i and j of list A."""

    if i != j:
        A[i], A[j] = A[j], A[i]


def Quicksort(A, start, end):
    """In-place quicksort."""

    if start >= end:
        return

    pivot = A[end]
    pivotIdx = start

    for i in range(start, end):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A

    yield from Quicksort(A, start, pivotIdx - 1)
    yield from Quicksort(A, pivotIdx + 1, end)


# Merge Function
def merge(A, start, mid, end):
    """Helper function for merge sort."""

    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A


# Merge sort function
def MergeSort(A, start, end):
    """Merge sort."""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from MergeSort(A, start, mid)
    yield from MergeSort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A


# Insertion sort function
def InsertionSort(arr):
    state = False
    for i in range(1, LIST_SIZE):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            yield arr, j, state
            state = False
            j -= 1
        state = True
        arr[j + 1] = key


# Bubble sort function
def BubbleSort(arr):
    for i in range(LIST_SIZE - 1):
        for j in range(0, LIST_SIZE - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr


# Selection sort function
def selection_sort(arr, index=0):
    for j in range(index, LIST_SIZE - 1):
        min_idx = j
        for k in range(j + 1, LIST_SIZE):
            if arr[min_idx] > arr[k]:
                min_idx = k
            yield arr
        arr[j], arr[min_idx] = arr[min_idx], arr[j]
