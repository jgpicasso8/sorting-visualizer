from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np
import copy

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
