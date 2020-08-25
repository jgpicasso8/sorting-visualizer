from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np
import copy


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


# CONSTANTS
LIST_SIZE = 100
ALG_COUNT = 2
ROW_COUNT = 2
COL_COUNT = 1
BAR_WIDTH = 0.6
ALG_NAMES = ['Bubble Sort', 'Selection Sort']
# ['Quicksort', 'Merge Sort', 'Bubble Sort',
#            'Insertion Sort']#, 'Timsort', 'Heap Sort']

# Creates a random list of 50 elements using seed 123
np.random.seed(123)
init_list = list(np.random.randint(0, 100, size=LIST_SIZE))

# Creates deep copies of original_list for each sorting algorithm
list_copies = [None] * ALG_COUNT
for count in range(ALG_COUNT):
    list_copies[count] = copy.deepcopy(init_list)

# Creates a list of generators yielded by each sorting algorithm function
generators = [BubbleSort(list_copies[0]), selection_sort(list_copies[1])]# Quicksort(list_copies[1], 0, LIST_SIZE - 1)]

'''[Quicksort(list_copies[0], 0, LIST_SIZE - 1),
              MergeSort(list_copies[1], 0, LIST_SIZE - 1),
              BubbleSort(list_copies[2])]#,
              #InsertionSort(list_copies[3])]'''

# Sets Style for Figure
style.use('Solarize_Light2')

# Creates Figure
fig = plt.figure(figsize=(15, 10))

# List for BarContainer objects for each bar graph
bar_container = [None] * ALG_COUNT

# Creates subplots 1 - ALG_COUNT
for i in range(ALG_COUNT):
    # Adds 1 subplot to Figure
    plt.subplot(ROW_COUNT, COL_COUNT, i + 1)
    # Adds bar graph to subplot. plt.bar() returns BarContainer objects
    bar_container[i] = plt.bar(range(LIST_SIZE), height=list_copies[i], color='DarkTurquoise', width=BAR_WIDTH)
    # Adds title to subplot
    plt.title(ALG_NAMES[i])

# When next(generator[#]) throws StopIteration
# active will prevent try statements from executing
active = [True] * ALG_COUNT


# Is called by FuncAnimation repeatedly to update fig Figure
def update_fig(A):
    # Iterates for each bar in fig
    for bar in range(ALG_COUNT):
        # If condition checks if StopIteration was thrown previously
        if active[bar]:
            # Try/except checks for StopIteration
            try:
                # Generator for given bar/sorting alg.
                tmp_list = next(generators[bar])
                # The height of each rect in a given BarContainer is updated
                for rect in range(LIST_SIZE):
                    bar_container[bar][rect].set_height(tmp_list[rect])
            except StopIteration:
                # StopIteration condition is met
                active[bar] = False


# Creates an animation by repeatedly calling function update_fig()
ani = FuncAnimation(fig=fig, func=update_fig, interval=1, frames=1)

# Display Figure
plt.show()

# Enables pyplot to clean up memory
plt.close(fig)
