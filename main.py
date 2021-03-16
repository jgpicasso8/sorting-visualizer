from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np
import copy


def swap(arr, i, j):
    """Helper function to swap elements i and j of list arr."""

    if i != j:
        arr[i], arr[j] = arr[j], arr[i]

# Quicksort Function (In-Place)
def Quicksort(arr, start, end):

    if start >= end:
        return

    pivot = arr[end]
    pivotIdx = start

    for i in range(start, end):
        if arr[i] < pivot:
            swap(arr, i, pivotIdx)
            pivotIdx += 1
        yield arr
    swap(arr, end, pivotIdx)
    yield arr

    yield from Quicksort(arr, start, pivotIdx - 1)
    yield from Quicksort(arr, pivotIdx + 1, end)


# Merge Helper Function for merge sort
def merge(arr, start, mid, end):

    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if arr[leftIdx] < arr[rightIdx]:
            merged.append(arr[leftIdx])
            leftIdx += 1
        else:
            merged.append(arr[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(arr[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(arr[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        arr[start + i] = sorted_val
        yield arr


# Merge Sort function
def MergeSort(arr, start, end):

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from MergeSort(arr, start, mid)
    yield from MergeSort(arr, mid + 1, end)
    yield from merge(arr, start, mid, end)
    yield arr


# Bubble sort function
def BubbleSort(arr):
    for i in range(LIST_SIZE - 1):
        for j in range(0, LIST_SIZE - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr


# Selection sort function
def selectionSort(arr, index=0):
    for j in range(index, LIST_SIZE - 1):
        min_idx = j
        for k in range(j + 1, LIST_SIZE):
            if arr[min_idx] > arr[k]:
                min_idx = k
            yield arr
        arr[j], arr[min_idx] = arr[min_idx], arr[j]


# CONSTANTS
LIST_SIZE = 50
ALG_COUNT = 4
ROW_COUNT = 2
COL_COUNT = 2
BAR_WIDTH = 0.6
ALG_NAMES = [ 'Quicksort: θ( nlog(n) )', 'Bubble Sort: θ( n^2 )',
              'Selection Sort: θ( n^2 )', 'Merge Sort: θ( nlog(n) )']

# Creates a random list of 50 elements using seed 123
np.random.seed(123)
init_list = list(np.random.randint(0, 100, size=LIST_SIZE))

# Creates deep copies of original_list for each sorting algorithm
list_copies = [None] * ALG_COUNT
for count in range(ALG_COUNT):
    list_copies[count] = copy.deepcopy(init_list)

# Creates a list of generators yielded by each sorting algorithm function
generators = [Quicksort(list_copies[2], 0, LIST_SIZE - 1), BubbleSort(list_copies[0]),
              selectionSort(list_copies[1]), MergeSort(list_copies[3], 0, LIST_SIZE - 1)]

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
plt.get_current_fig_manager().window.state('zoomed')
plt.show()

# Enables pyplot to clean up memory
plt.close(fig)
