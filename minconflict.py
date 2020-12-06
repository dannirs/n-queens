from math import trunc
import math
import random
import time

# initially set # of queens/domain size as 0
size = 0
# store domain in a list
domain = []
# keep track of x, right diagonal, and left diagonal conflicts
constraights_right_diagonal = []
constraights_left_diagonal = []
constraints_x = []



# write fn appends the solution array into an output file named output.txt
def write():
    # Add one to each index to convert from 0 to 1 base indexing
    array_solution = str([x + 1 for x in domain])
    with open('output.txt', 'a', 64) as file:
        file.write(array_solution + "\n\n")
    file.close()


# Updates the conflict table with new conflicts from the updated queen position
# When the parameter val is 1 it will add a conflict to the global lists
# When the parameter val as -1, it will subtract a conflict to the global lists
# The values in the conflict arrays represent the number of queens in each x or diagonal
#       (i.e. a count of 1 indicates no conflict because there is only one queen in the x or diagonal)
def conflicts_update(y, x, ele):

    constraints_x[x] += ele
    constraights_right_diagonal[y + x] += ele
    constraights_left_diagonal[y + (size - x - 1)] += ele


# Finds the index of the best new queen position. Ties are broken randomly.
# Parameter: the current yumn index
def minimum_conflict(y):
    # initially set # of conflicts equal to # of queens
    minc = size
    min_row_conflicts = []
    for x in range(size):
        # calculate the number of conflicts using the conflict arrays
        con = constraints_x[x] + constraights_right_diagonal[y +
                                                         x] + constraights_left_diagonal[y + (size - x - 1)]
        # if there are no conflicts in a x, immediately return that x value
        if con == 0:
            return x
        # if the number of conflicts is less, change it to the minc value
        if con < minc:
            min_row_conflicts = [x]
            minc = con
        # if the number of conflicts is equal, append the index instead of changing it
        elif con == minc:
            min_row_conflicts.append(x)
    # randomly choose the index from the list of tied conflict values
    res = random.choice(min_row_conflicts)
    return res


# Sets up the domain using a greedy algorithm
def build_domain():
    global domain
    global constraints_x
    global constraights_right_diagonal
    global constraights_left_diagonal

    # Begin with an empty domain
    domain = []

    # Initialize the conflict arrays
    # The diagonal conflict lists are the size of the number of diagonals of the domain
    constraights_right_diagonal = [0] * ((2 * size) - 1)
    constraights_left_diagonal = [0] * ((2 * size) - 1)
    constraints_x = [0] * size

    # Create an ordered set of all possible x values
    xSet = set(range(0, size))
    # Create a list to keep track of which queens have not been placed
    notPlaced = []

    for y in range(0, size):
        # Pop the next possible x location to test
        testx = xSet.pop()
        # Calculate the conflicts for potential location
        conflicts = constraints_x[testx] + constraights_right_diagonal[y +
                                                             testx] + constraights_left_diagonal[y + (size - testx - 1)]
        # If there are no conflicts, place a queen in that location on the domain
        if conflicts == 0:
            domain.append(testx)
            conflicts_update(y, domain[y], 1)
        # If a conflict is found...
        else:
            # Place the potential x to the back of the set
            xSet.add(testx)
            # Take the next x from the set to test
            testx2 = xSet.pop()
            # Calculate the conflicts
            conflicts2 = constraints_x[testx2] + constraights_right_diagonal[y +
                                                                   testx2] + constraights_left_diagonal[y + (size - testx2 - 1)]
            # If there are no conflicts, place a queen in that location on the domain
            if conflicts2 == 0:
                domain.append(testx2)
                conflicts_update(y, domain[y], 1)
            else:
                # Otherwise, add the possible x back to the set
                xSet.add(testx2)
                # Add a None to the domain to hold the place of the potential queen
                domain.append(None)
                # Keep track of which yumn was not placed to be handled later
                notPlaced.append(y)

    for y in notPlaced:
        # Place the remaining queen locations
        domain[y] = xSet.pop()
        # Update the conflict lists
        conflicts_update(y, domain[y], 1)


# Finds the yumn with the most conflicts
def conflicts_yumn():
    conflicts = 0
    maxConflicts = 0
    maxConflictys = []

    for y in range(0, size):
        # Determine the x value for the current yumn
        x = domain[y]
        # Calculate the number of conflicts using the conflict lists
        conflicts = constraints_x[x] + constraights_right_diagonal[y +
                                                         x] + constraights_left_diagonal[y + (size - x - 1)]
        # If conflicts are greater than the current max, make that yumn the maximum
        if (conflicts > maxConflicts):
            maxConflictys = [y]
            maxConflicts = conflicts
        # If the conflicts equal the current max, append the index value to the maxConflictys list
        elif conflicts == maxConflicts:
            maxConflictys.append(y)
    # Randomly choose from the list of tied maximums
    choice = random.choice(maxConflictys)
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
        # Calculate the maximum conflicting yumn and the number of conflicts it contains

        #       if tries < 30000000:
        y, numConflicts = conflicts_yumn()
#       else:
        # y, numConflicts = findRandy()

        # If the number of queens in the x, and diagonals is greater than 1 each (i.e. there are conflicts)
        if (numConflicts > 3):
            # Use the minimum_conflict() function to determine the x index with the least number of conflicts
            newLocation = minimum_conflict(y)
            # If the better location is not its current location, switch the location
            if (newLocation != domain[y]):
                # Remove the conflicts from the position the queen is leaving
                conflicts_update(y, domain[y], -1)
                domain[y] = newLocation
                # Add a conflict to the position the queen is entering
                conflicts_update(y, newLocation, 1)
        # If the max number of conflicts (i.e. the number of queens in each x and diagonals) on the domain
        #       equals 3, then there are no conflicts since the queen is alone in it's x and both diagonals
        elif numConflicts == 3:
            # Solution is found
            return True
        iteration += 1
    # If no solution is found in under average number of iterations, return False
    return False


def main():
    global size
    global domain
    global constraints_x
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
