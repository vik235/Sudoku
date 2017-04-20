# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 18:45:14 2017

@author: vigupta
"""

assignments = []

def inner(a,b):
    assert len(a)==len(b)
    inner=[]
    for i in range(len(a)):
        inner.append(a[i]+b[i])
    return inner    

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    pass


rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
boxes

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
diagonal_units=[]
diagonal_units.append(inner(rows,cols))
diagonal_units.append(inner(rows,cols[::-1]))
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
diagnonal_unitlist=row_units + column_units + square_units+diagonal_units
diagonal_units=dict((s, [u for u in diagnonal_unitlist if s in u]) for s in boxes)
diagonal_peers= dict((s, set(sum(diagonal_units[s],[]))-set([s])) for s in boxes)


def grid_values(values):
    assert len(values)==81
    s = [box for box in boxes]
    v = [st.replace('.','123456789') for st in values]
    return dict(zip(s,v))

def eliminate(values):
    unsolved_boxes= [box for box in boxes if len(values[box]) !=1 ]
    for unsolved_box in unsolved_boxes: 
        for digit in '123456789':
            if digit in [values[solved_peers] for solved_peers in diagonal_peers[unsolved_box] if len(values[solved_peers]) ==1]:
                values[unsolved_box]=values[unsolved_box].replace(digit,'')
    return values

def only_choice(values):    
     for unit in diagnonal_unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
     return values
 
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
            twins=[box for box in unit if len(values[box])==2]
            if len(twins)>1 :
                for potential_twin in set(cross('123456789','123456789')):
                    if ([values[box] for box in twins].count(potential_twin)+[values[box] for box in twins].count(potential_twin[::-1]))==2:
                        digits=potential_twin.split()
                        boxes_to_clean=[box for box in unit if len(values[box])>2]
                        for box in boxes_to_clean:
                            for strvalues in digits:
                                for digit in strvalues:
                                    values[box]=values[box].replace(digit,'')    
    return values               
          

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    
        
    
def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudok
    If after an iteration of both functions, the sudoku remains the same, return the sudok
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        #values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

    
    

