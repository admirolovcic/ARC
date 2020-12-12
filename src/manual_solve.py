#!/usr/bin/python
"""
Student name(s): Admir Olovcic
Student ID(s): 20235852
https://github.com/admirolovcic/ARC

"""


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
Problem 1:
Problem statement - this excercise is analogous to fixing a stained patterned persian rug with the added complication of a two step offset. The general procedure
is for the algorithm to look for any brown patches or "stains" and fix them by looking up the symetrical fields. 
"""

def solve_3631a71a(x):
    #traversable width
    width = 29
    #traversable height
    height = 29
      
    for i in range(width +1):
        for j in range(height+1):
            #if field is brown (stain)
            if(x[i,j] == 9):
                #since pattern is offset, we have no info on the first 2 x 2 sub array. 
                if(i<2 & j<2):
                    pass
                #if the field falls in either the first 2 rows or the first 2 columns, we have only one possible field to lookup from. The one along the same row/column as applicable. 
                elif(i<2):
                    x[i,j] = x[i, width - j - 2]
                elif(j<2):
                    x[i,j] = x[height - i + 2, j]
                    
                #Else, the field will have 3 symetrical fields to look up from. We take the most common value in case one of the other fields also falls with in a "stain".
                else:  
                    c1 = x[i, width - j + 2]
                    c2 = x[height - i + 2, j]
                    c3 = x[height - i + 2, width - j + 2]
                    c = Counter([c1, c2, c3])
                    most_common = c.most_common(1)[0][0]
                    x[i,j] = most_common #return answer                   
    return x

"""
solved correctly - 1, 4 and test grid 1. 
due to the nature of the problem, attempting to visually compare the input and output for debugging proved nauseating so no further attempt was made to 
debug as it would require code to be written that is outside the scope of this assignment. 

Discussion: numpy was the only library required. To be sure, if the solution were to be deployed on more test data, the likelyhood is that it would fail due to 
changes in the size in input array or similar. The solution is therefore likely an over-fit for the task but within scope of assignment. 
"""


"""
Problem 2
Problem is very reminiscent of Tetris without the rotation and with the output being a 3x3 array. 
Algorithm will traverse the input array with a 3x3 grid and save any resultant arrays that contain all of the members of a certain shape (members with same color).
Finally, the algorithm will perform a cross analysis and by member wise addition (numpy array addition) will extract a resulting array where there is no black color 
left. 
"""


def solve_681b3aeb(x):
    # get the colors of the shapes
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
    
    #initialize shape matrices
    possible_color1_matrices = []
    possible_color2_matrices = []
    
    #traverse the input array with a 3x3 array and save all arrays containing all of the members of a color set. 
    for i in range(11):
        for j in range(11):
            arr_slice = resized_x[i:i+3,j:j+3]
            count_of_color1 = list(arr_slice.flatten()).count(color1)
            count_of_color2 = list(arr_slice.flatten()).count(color2)
            if(count_of_color1 == color1_count):
                possible_color1_matrices.append(arr_slice)
            if(count_of_color2 == color2_count):
                possible_color2_matrices.append(arr_slice)
    
    #perform memberwise addition on all the sets and extract the result where no "0"'s exist.
    for m1 in possible_color1_matrices:
        for m2 in possible_color2_matrices:
            candidate = m1 + m2
            if(list(candidate.flatten()).count(0) == 0):
                return candidate

"""
Correctly solved grids - all

Discussion:
in this case again NumPy was sufficient with the addition of Counter. The traversal of the array was done using a nested for loop and the extraction was preconditioned
on the fact that there was no rotation involved. Approach used standard array slicing and standard list rules to test for grid content. It is becoming clear that a
pattern extraction library would be useful with this class of problem. Something like linq in C# so that statements like x.where(x =>  x.value > 0) can be used. 

"""

"""
Problem 3:
    
This problem is essentially a shape extraction exercise with a color switch. 
The algorithm will again traverse the grid with a 2x2 array and extract the colour when it finds one instance where all the members are the same. This is then assigned 
to the primary_color variable. The other non-0 color is then assigned to the secondary_color variable. 
Algorithm will then remove any row or column not containing the primary color leaving just the shape to be extracted. 
Finally, the resulting array is shrunk to 3x3 array. 

"""

def solve_5ad4f10b(x):
    main_color = None
    #traverse input with a 2x2 array and return the color of the first homogenous subset encountered
    for i in range(len(x)-2):
        if(main_color != None):
            break
        for j in range(len(x[0])-2):
            scanner = x[i:i+2,j:j+2]
            set_of_colors = list(set(scanner.flatten()))
            if((len(set_of_colors) == 1) & (set_of_colors[0] != 0)):
                main_color = set_of_colors[0]
                break
            
    # Get secondary color by getting the other non-zero color in the input grid     
    flat_x = x.flatten()
    list_of_all_colors = list(set(flat_x))
    list_of_all_colors.remove(0)
    list_of_all_colors.remove(main_color)
    secondary_color = list_of_all_colors[0]
    
    #get the limits of the shape we want to extract
    array_width = len(x[0])
    array_height = len(x)
    
    for i in range(array_width):
        column = x[:,i]
        if((main_color in column)):
            start_column = i
            break
        
    for i in range(array_width):
        column = x[:,array_width -i -1]
        if((main_color in column)):
            end_column = array_width - i
            break    
    
    for i in range(array_height):
        row = x[i,:]
        if((main_color in row)):
            start_row = i
            break
    
    for i in range(array_height):
        row = x[array_height -i -1,:]
        if((main_color in row)):
            end_row = array_height - i
            break 
        
    #isolate the shape    
    isolated_shape = x[start_row:end_row,start_column:end_column]        
    shape_length = len(isolated_shape[0])
    shape_height = len(isolated_shape)
    
    #initialize output
    output_array = np.array([[0,0,0],[0,0,0],[0,0,0]])
    
    #check each of the 9 subdivisions for primary color
    for i in range(int(shape_height/3)):
        for j in range(int(shape_length/3)):
            start_i = int((i * shape_length) / 3)
            start_j = int((j * shape_length) / 3)
            subdivision = isolated_shape[start_i : start_i + int(shape_length/3), start_j : start_j + int(shape_height/3)]
            if(main_color in list(subdivision.flatten())):
                #if color is contained in subdivision, assign secondary color to the appropriate cell
                output_array[i,j] = secondary_color
    
    return output_array
"""
Discussion:

Correctly solved grids: all

As discussed in Chollet, this problem has numerous algorithmic solutions and the real measure of AI should be the ability to abstract and recognise patterns. 
While some of these can be solved by a human child quite readily, the fact that the abstract 
problem definition is instinctual and not really explainable, it follows that pattern recognition will need to be augmented by models of other Neurological Processes.
At the moment computers can outperform humans on at least two high level Cognitive Processes, namely memory and logic (pattern recognition utilizes the two). I suspect that the concept of instinct is going 
to be difficult for computers to model since it is not readily describable even to humans, or even to the individual human. We tend to call a lot of this "Gut Instinct".
Current AI models are data-hungry and too application-specific. Humans can abstract from much less data and we don't really know the mechanics behind this. 
Chollet discusses this on p.11

From a procedural perspective, again matrix manipulation using numpy was sufficient as detailed in comments.   
"""
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

