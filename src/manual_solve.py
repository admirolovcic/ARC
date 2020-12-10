#!/usr/bin/python

import os, sys
import json
import numpy as np
import re
from collections import Counter

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.
"""
def solve_3631a71a(x):
    width = 29
    height = 29
    for i in range(width +1):
        for j in range(height+1):
            if(x[i,j] == 9):
                if(i<2 & j<2):
                    pass
                elif(i<2):
                    x[i,j] = x[i, width - j - 2]
                elif(j<2):
                    x[i,j] = x[height - i + 2, j]
                else:  
                    c1 = x[i, width - j + 2]
                    c2 = x[height - i + 2, j]
                    c3 = x[height - i + 2, width - j + 2]
                    c = Counter([c1, c2, c3])
                    most_common = c.most_common(1)[0][0]
                    #print(f"{x[i,j]} changed to {most_common} at {i}, {j}" )
                    x[i,j] = most_common
                    
    return x
"""

def solve_681b3aeb(x):
    flat_list = x.flatten()
    c = Counter(flat_list)
    most_common = c.most_common(3)
    color1 = most_common[1][0]
    color1_count = most_common[1][1]
    color2 = most_common[2][0]
    color2_count = most_common[2][1]
    
    #resize array so it can more easily be traversed with a 3x3 array
    zero_padding_v = np.zeros((2,14))
    zero_padding_h = np.zeros((10,2))
    resized_x = np.hstack((zero_padding_h, x, zero_padding_h))
    resized_x = np.vstack((zero_padding_v, resized_x, zero_padding_v))
    possible_color1_matrices = []
    possible_color2_matrices = []
    
    for i in range(11):
        for j in range(11):
            arr_slice = resized_x[i:i+3,j:j+3]
            count_of_color1 = list(arr_slice.flatten()).count(color1)
            count_of_color2 = list(arr_slice.flatten()).count(color2)
            if(count_of_color1 == color1_count):
                possible_color1_matrices.append(arr_slice)
            if(count_of_color2 == color2_count):
                possible_color2_matrices.append(arr_slice)
    
    for m1 in possible_color1_matrices:
        for m2 in possible_color2_matrices:
            candidate = m1 + m2
            if(list(candidate.flatten()).count(0) == 0):
                return candidate

# def solve_05269061(x):
#     return x


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

