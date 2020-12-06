from math import trunc
import math
import random
import time

# initially set # of queens/domain size as 0
size = 0
# store domain in a list
domain = []
# keep track of row, right diagonal, and left diagonal conflicts
constraints_row = []
constraights_right_diagonal = []
constraights_left_diagonal = []


# Append the solution array to the output file
def write():
    # Add one to each index to convert from 0 to 1 base indexing
    solutionArrayStr = str([x + 1 for x in domain])
    with open('output.txt', 'a', 64) as file:
        file.write(solutionArrayStr + "\n\n")
    file.close()


# Updates the conflict table with new conflicts from the updated queen position
# When the parameter val is 1 it will add a conflict to the global lists
# When the parameter val as -1, it will subtract a conflict to the global lists
# The values in the conflict arrays represent the number of queens in each row or diagonal
#       (i.e. a count of 1 indicates no conflict because there is only one queen in the row or diagonal)
def conflicts_update(col, row, val):
    constraints_row[row] += val
    constraights_right_diagonal[col + row] += val
    constraights_left_diagonal[col + (size - row - 1)] += val


# Finds the index of the best new queen position. Ties are broken randomly.
# Parameter: the current column index
def minimum_conflict(col):
    # initially set # of conflicts equal to # of queens
    minConflicts = size
    minConflictRows = []
    for row in range(size):
        # calculate the number of conflicts using the conflict arrays
        conflicts = constraints_row[row] + constraights_right_diagonal[col +
                                                         row] + constraights_left_diagonal[col + (size - row - 1)]
        # if there are no conflicts in a row, immediately return that row value
        if conflicts == 0:
            return row
        # if the number of conflicts is less, change it to the minConflicts value
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        # if the number of conflicts is equal, append the index instead of changing it
        elif conflicts == minConflicts:
            minConflictRows.append(row)
    # randomly choose the index from the list of tied conflict values
    choice = random.choice(minConflictRows)
    return choice


# Sets up the domain using a greedy algorithm
def build_domain():
    global domain
    global constraints_row
    global constraights_right_diagonal
    global constraights_left_diagonal

    # Begin with an empty domain
    domain = []

    # Initialize the conflict arrays
    # The diagonal conflict lists are the size of the number of diagonals of the domain
    constraights_right_diagonal = [0] * ((2 * size) - 1)
    constraights_left_diagonal = [0] * ((2 * size) - 1)
    constraints_row = [0] * size

    # Create an ordered set of all possible row values
    rowSet = set(range(0, size))
    # Create a list to keep track of which queens have not been placed
    notPlaced = []

    for col in range(0, size):
        # Pop the next possible row location to test
        testRow = rowSet.pop()
        # Calculate the conflicts for potential location
        conflicts = constraints_row[testRow] + constraights_right_diagonal[col +
                                                             testRow] + constraights_left_diagonal[col + (size - testRow - 1)]
        # If there are no conflicts, place a queen in that location on the domain
        if conflicts == 0:
            domain.append(testRow)
            conflicts_update(col, domain[col], 1)
        # If a conflict is found...
        else:
            # Place the potential row to the back of the set
            rowSet.add(testRow)
            # Take the next row from the set to test
            testRow2 = rowSet.pop()
            # Calculate the conflicts
            conflicts2 = constraints_row[testRow2] + constraights_right_diagonal[col +
                                                                   testRow2] + constraights_left_diagonal[col + (size - testRow2 - 1)]
            # If there are no conflicts, place a queen in that location on the domain
            if conflicts2 == 0:
                domain.append(testRow2)
                conflicts_update(col, domain[col], 1)
            else:
                # Otherwise, add the possible row back to the set
                rowSet.add(testRow2)
                # Add a None to the domain to hold the place of the potential queen
                domain.append(None)
                # Keep track of which column was not placed to be handled later
                notPlaced.append(col)

    for col in notPlaced:
        # Place the remaining queen locations
        domain[col] = rowSet.pop()
        # Update the conflict lists
        conflicts_update(col, domain[col], 1)


# Finds the column with the most conflicts
def conflicts_column():
    conflicts = 0
    maxConflicts = 0
    maxConflictCols = []

    for col in range(0, size):
        # Determine the row value for the current column
        row = domain[col]
        # Calculate the number of conflicts using the conflict lists
        conflicts = constraints_row[row] + constraights_right_diagonal[col +
                                                         row] + constraights_left_diagonal[col + (size - row - 1)]
        # If conflicts are greater than the current max, make that column the maximum
        if (conflicts > maxConflicts):
            maxConflictCols = [col]
            maxConflicts = conflicts
        # If the conflicts equal the current max, append the index value to the maxConflictCols list
        elif conflicts == maxConflicts:
            maxConflictCols.append(col)
    # Randomly choose from the list of tied maximums
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts


# Sets up the domain using build_domain() and then solves it with a min-conflict algorithm
def solve():
    build_domain()
    iteration = 0
    # maxIteration = 0.6 * size  # Define the maximum iterations as 0.6 * size of domain
    if size < 100:
        maxIteration = size
    else:
        maxIteration = 0.6 * size
    while (iteration < maxIteration):
        # Calculate the maximum conflicting column and the number of conflicts it contains

        #       if tries < 30000000:
        col, numConflicts = conflicts_column()
#       else:
        # col, numConflicts = findRandCol()

        # If the number of queens in the row, and diagonals is greater than 1 each (i.e. there are conflicts)
        if (numConflicts > 3):
            # Use the minimum_conflict() function to determine the row index with the least number of conflicts
            newLocation = minimum_conflict(col)
            # If the better location is not its current location, switch the location
            if (newLocation != domain[col]):
                # Remove the conflicts from the position the queen is leaving
                conflicts_update(col, domain[col], -1)
                domain[col] = newLocation
                # Add a conflict to the position the queen is entering
                conflicts_update(col, newLocation, 1)
        # If the max number of conflicts (i.e. the number of queens in each row and diagonals) on the domain
        #       equals 3, then there are no conflicts since the queen is alone in it's row and both diagonals
        elif numConflicts == 3:
            # Solution is found
            return True
        iteration += 1
    # If no solution is found in under average number of iterations, return False
    return False


def main():
    global size
    global domain
    global constraints_row
    global constraights_right_diagonal
    global constraights_left_diagonal

    # Read in the file containing the size values
    filepath = 'input.txt'
    sizeensionArray = []
    fp = open(filepath, "r", encoding="utf-8")
    for line in fp:
        sizeensionArray.append(int(line.rstrip('\n')))
    for sizeension in sizeensionArray:
        # If the sizeension is outside the constraints
        if sizeension <= 3 or sizeension > 10000000:
            # Print error and write empty array to file
            print("Cannot build domain of size: " + str(sizeension))
            write()
        else:
            # Set size equal to the current test sizeension
            size = sizeension
            # Start timer and set/reset boolen
            time0 = time.time()
            solved = False
            print("Searching for domain configuration of size " +
                  str(sizeension) + "...")
            # 6 is a special case, return hard-coded solution and skip while loop
            if (size == 6):
                domain = [1, 3, 5, 0, 2, 4]
            # Continues restarting solve() until a solution is found
            while (not solved):
                # Solved will be True when a solution is returned
                solved = solve()

            print("domain configuration found for size " + str(sizeension))

            write()

            # Calculate and print time taken to find solution
            time1 = time.time()
            tot_time = time1 - time0
            time_string = str(trunc(tot_time * 100) / 100)
            print("   Took " + time_string + " seconds\n")
    fp.close()


main()
