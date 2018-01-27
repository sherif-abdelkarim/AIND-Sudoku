import time

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i]+cols[i] for i in range(len(rows))], [rows[i] + cols[::-1][i] for i in range(len(rows))]] 
unitlist = row_units + column_units + square_units + diagonal_units # adds the diagonals to the units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # diagonals are included with the peers 

def solved(values):
    ''' 
    Checks to see if the puzzle is solved
    Args:
        values(dict) - a dictionary representing the state of the board.    
    Returns:
        a boolean - True if the puzzle is solved and False otherwise

    '''
    return all(len(values[s]) == 1 for s in boxes)
    
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Doesn't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
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
    values = {boxes[i]: grid[i] if not grid[i] == '.' else '123456789' for i in range(len(grid)) }
    return values

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

def eliminate(values):   
    '''
    Eliminates the value of solved box from the values in its peers
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the value of the solved box 
        eliminated from peers.
    ''' 
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        for peer in peers[box]:
            replacement = values[peer].replace(values[box], "")
            values = assign_value(values, peer, replacement)
    return values

def only_choice(values):
    '''
    If there is only one box in a unit that has a certain digit, 
    the box is assigned value of that digit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the value of the digit assigned to the box 
    ''' 
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                replacement = digit
                values = assign_value(values, dplaces[0], replacement)  
    return values

def naked_twins(values):
    """Eliminates values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Finds all twins in the whole board and stores them in an array called twins
    twins = []
    for unit in unitlist:
        for box1 in unit:
            for box2 in unit:
                if (not box1==box2) and (values[box1]==values[box2]) and len(values[box1]) == 2 and len(values[box2]) == 2:
                    sorted_twin = [box1,box2]
                    sorted_twin.sort()
                    twin = (sorted_twin[0],sorted_twin[1])
                    if(twin not in twins):
                        twins.append((box1,box2))

    values_copy = values.copy() #copies the values so that the twins values can be accessed later without being affected by the deletion of digits
    for twin in twins:
        digit1 = values_copy[twin[0]][0] # getting the values of the twins from the copy of values
        digit2 = values_copy[twin[0]][1]
        common_peers = set(peers[twin[0]]).intersection(peers[twin[1]])
        for box in common_peers:
            replacement = values[box].replace(digit1, "").replace(digit2, "")
            values = assign_value(values, box, replacement)
    return values
    # Eliminate the naked twins as possibilities for their peers

def naked_triplets(values): 
    """Eliminates values using the naked triplets strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked triplets eliminated from peers.
    """
    # Finds all twins in the whole board and stores them in an array called twins
    triplets = []
    for unit in unitlist:
        for box1 in unit:
            for box2 in unit:
                for box3 in unit:
                    if (not (box1==box2 or box2==box3 or box1==box3) and (values[box1]==values[box2] and values[box2]==values[box3]) and len(values[box1]) == 3):
                        sorted_triplet = [box1,box2,box3]
                        sorted_triplet.sort()
                        triplet = (sorted_triplet[0],sorted_triplet[1],sorted_triplet[2])
                        if(triplet not in triplets):
                            triplets.append((box1,box2,box3))

    values_copy = values.copy() #copies the values so that the triplets values can be accessed later without being affected by the deletion of digits
    for triplet in triplets:
        digit1 = values_copy[triplet[0]][0] # getting the values of the triplets from the copy of values
        digit2 = values_copy[triplet[0]][1] # it is okay to get all the digits from one of the triplets only since they are identical
        digit3 = values_copy[triplet[0]][2]
        common_peers = (set(peers[triplet[0]]).intersection(peers[triplet[1]])).intersection(peers[triplet[2]])
        for box in common_peers:
            replacement = values[box].replace(digit1, "").replace(digit2, "").replace(digit3, "")
            values = assign_value(values, box, replacement)
    return values

def get_solved_values(values):
    '''
    Gets the number of boxes solved in the puzzle
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        an integer(int) representing the number of solved boxes 
    '''
    return len([box for box in values.keys() if len(values[box]) == 1])

def reduce_puzzle(values):
    '''
    Reduces the possibilities for each box in the puzzle using constraint propagation
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary after applying constraint propagation
    '''
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = get_solved_values(values)
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        values = naked_twins(values)
       # Check how many boxes have a determined value, to compare
        solved_values_after = get_solved_values(values)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        if(stalled):                        # if it got stuck it tries with reducing the puzzle with the naked 
            values = naked_triplets(values) # triplets and retries the other alorithms agian

        solved_values_after = get_solved_values(values)
        stalled = solved_values_before == solved_values_after   # it rechecks to see if the algorithm is still stuck
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    '''
    Uses depth-first search and constraint propagation, to all possible values.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary representing the solution if a solution exists.
        or False if not solution exists
    '''
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if solved(values): 
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

def solve(grid):
    """
    Finds the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    grids = ['2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3',        '4.......3..9.........1...7.....1.8.....5.9.....1.2.....3...5.........7..7.......8',        '......3.......12..71..9......36...................56......4..67..95.......8......',        '....3...1..6..........9...5.......6..1.7.8.2..8.......3...1..........7..9...2....',        '...47..........8.........5.9..2.1...4.......6...3.6..1.7.........4..........89...',        '...4.....37.5............89....9......2...7......3....43............2.45.....6...',        '..7........5.4...........18...3.6....1.....7....8.2...62...........9.6........4..',        '....29.......7......3...8..........735.....161..........6...4......6.......83....',        '7.......8.....14...4........7..1.......4.3.......6..2........3...35.....5.......4',        '5.......7......2.....3...1...8.4.......7.8.......2.9...8...5.....1......6.......9',        '..682...........69..7.......2..........9.4..........8.......5..58...........521..']
    #grids = ['.524.........7.1..............8.2...3.....6...9.5.....1.6.3...........897........']
    solutions_found = 0
    total_time = 0
    
    for grid in grids:
        start_time = time.time()
        solution = solve(grid)
        end_time = time.time()
        time_elapsed = end_time - start_time
        if(solution):
            total_time += time_elapsed
            solutions_found += 1
            display(solution)
            print("time elapsed: " + str(time_elapsed))

        else:
            print('Could not find solution')

    average_time_elapsed = total_time/solutions_found
    print("average time elapsed: " + str(average_time_elapsed))
        
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
