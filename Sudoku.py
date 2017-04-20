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


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers in the unit.
    
    #Work on each units and create a list of possible twins in that unit.
    #Once the possible twins are narrowed down to, find a list of peer unit boxes that has to be cleaned via constraint prop. 
    for unit in unitlist:
            twins=[box for box in unit if len(values[box])==2]
            if len(twins)>1 :
                for potential_twin in set(cross('123456789','123456789')):
                    if ([values[box] for box in twins].count(potential_twin)+[values[box] for box in twins].count(potential_twin[::-1]))==2:
                        digits=potential_twin.split()
                        boxes_to_clean=[box for box in unit if values[box] != potential_twin if values[box] != potential_twin[::-1]]
                        for box in boxes_to_clean:
                            for strvalues in digits:
                                for digit in strvalues:
                                    values[box]=values[box].replace(digit,'')    
    return values               


    
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid)==81
    s = [box for box in boxes]
    v = [st.replace('.','123456789') for st in grid]
    return dict(zip(s,v))
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    pass

def eliminate(values):
    unsolved_boxes= [box for box in boxes if len(values[box]) !=1 ]
    for unsolved_box in unsolved_boxes: 
        for digit in '123456789':
            if digit in [values[solved_peers] for solved_peers in peers[unsolved_box] if len(values[solved_peers]) ==1]:
                values[unsolved_box]=values[unsolved_box].replace(digit,'')
    return values
    pass

def only_choice(values):    
     for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
     return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
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
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
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



def eliminate_d(values):
    unsolved_boxes= [box for box in boxes if len(values[box]) !=1 ]
    for unsolved_box in unsolved_boxes: 
        for digit in '123456789':
            if digit in [values[solved_peers] for solved_peers in diagonal_peers[unsolved_box] if len(values[solved_peers]) ==1]:
                values[unsolved_box]=values[unsolved_box].replace(digit,'')
    return values

def only_choice_d(values):    
     for unit in diagnonal_unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
     return values
 
def naked_twins_d(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in diagnonal_unitlist:
            twins=[box for box in unit if len(values[box])==2]
            if len(twins)>1 :
                for potential_twin in set(cross('123456789','123456789')):
                    if ([values[box] for box in twins].count(potential_twin)+[values[box] for box in twins].count(potential_twin[::-1]))==2:
                        digits=potential_twin.split()
                        boxes_to_clean=[box for box in unit if values[box] != potential_twin if values[box] != potential_twin[::-1]]
                        for box in boxes_to_clean:
                            for strvalues in digits:
                                for digit in strvalues:
                                    values[box]=values[box].replace(digit,'')    
    return values               
          

def search_d(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle_d(values)
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
    
        
    
def reduce_puzzle_d(values):
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
        values = eliminate_d(values)
        # Use the Only Choice Strategy
        values = only_choice_d(values)
        # Use the Naked Twins Strategy
        values = naked_twins_d(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

    
    


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #Create _d functions to take into accoutn of the new constraints introduced in diagonal sudoku
    #Call the wrapper function that does DFS and tries to reduce the sudoku using naked twins, elimination, and only_choice strategies
    values={}
    values=grid_values(grid)
    return search_d(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
