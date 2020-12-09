from math import trunc
import random
import time
import matplotlib.pyplot as plt
from typing import Generator, List
# creates an initial domain


def createInitialdomain():
    # use global keyword so that we can modify each variable inside the function
    global domain
    global numRow
    global numRightDiag
    global numLeftDiag

    # create a list to store the chess domain
    domain = []

    # initialize the lists for # of queens in each row, left diagonal, and right diagonal
    # the size of the lists are the # of rows and # of diagonals in the domain
    # initially, there are 0 queens in each list
    numRow = [0] * numQueens
    numRightDiag = [0] * ((2 * numQueens) - 1)
    numLeftDiag = [0] * ((2 * numQueens) - 1)

    # create an ordered set of all row index values
    rowsRemaining = set(range(0, numQueens))
    # create a list that keeps track of which columns have not been solved for
    colsRemaining = []

    # iterate through each column
    for col in range(0, numQueens):
        # test a row in the column by popping the first row index out of the set of all rows
        tryRow = rowsRemaining.pop()

        # add the total # of queens that can attack the square using col and tryRow
        conflicts = numRow[tryRow] + numRightDiag[col +
                                                  tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]

        # if there are 0 attacking queens, then immediately place the queen at that position
        # this is to make as "good" an initial domain as possible to make it easier to find a solution
        if conflicts == 0:
            # append the row index to the domain list to show the queen's positioning
            domain.append(tryRow)
            # update row and diagonal lists, passing add = 1 to show that conflicts need to be added
            updateConflicts(col, tryRow, 1)

        else:
            # if there are attacking queens, then add the row to the back of the set to test it again later
            rowsRemaining.add(tryRow)
            # pop the next row from the set to test
            tryRow = rowsRemaining.pop()
            conflicts = numRow[tryRow] + numRightDiag[col +
                                                      tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]

            # if there are no attacking queens, place the queen at that location and append the row index to the domain, update conflicts
            if conflicts == 0:
                domain.append(tryRow)
                updateConflicts(col, tryRow, 1)

            else:
                # Otherwise, add this row at the back of the set as well to test it later
                rowsRemaining.add(tryRow)
                # add "none" to the domain to show that the column has not yet been filled
                domain.append(None)
                # append the column index to the colsRemaining list to come back to that column later
                colsRemaining.append(col)

    # after iterating through all columns in the domain, iterate through the list of all columns that have not yet been placed
    for col in colsRemaining:
        # place the queen at the first row in rowsRemaining, regardless of if there are conflicts or not to finish creating the initial domain
        domain[col] = rowsRemaining.pop()

        # update row and diagonal lists, passing add= 1 to show that conflicts need to be added
        updateConflicts(col, domain[col], 1)


# creates a random domain (called if there's an infinite loop)
def createRandomdomain():
    # use global keyword so that we can modify each variable inside the function
    global domain
    global numRow
    global numRightDiag
    global numLeftDiag

    # create a list to store the chess domain
    domain = []

    # initialize the lists for # of queens in each row, left diagonal, and right diagonal
    # the size of the lists are the # of rows and # of diagonals in the domain
    # initially, there are 0 queens in each list
    numRow = [0] * numQueens
    numRightDiag = [0] * ((2 * numQueens) - 1)
    numLeftDiag = [0] * ((2 * numQueens) - 1)

    # create an ordered set of all row index values
    rowsRemaining = list(range(0, numQueens))
    # randomly shuffle the list
    random.shuffle(rowsRemaining)

    # iterate through each column
    for col in range(0, numQueens):
        # pop the first row from the list
        tryRow = rowsRemaining.pop()
        # append the row index to the domain list to show the queen's positioning
        domain.append(tryRow)
        # update row and diagonal lists, passing add = 1 to show that conflicts need to be added
        updateConflicts(col, tryRow, 1)


# whenever a queen is moved to/from a position, there will be changes made to the row, left diagonal, and
# right diagonal lists that store the # of queens. this function updates the lists.
# parameters: col - column that queen is moved to/from
# row - row that the queen is moved to/from
# add - if 1 (queen is moved to a position), will add a queen to the list;
# if -1 (queen is moved from a position), will subtract a queen from the list
def updateConflicts(col, row, add):
    # update the row, right diagonal, and left diagonal lists that the queen is moved from/to by either adding or subtracting 1
    numRow[row] += add
    numRightDiag[col + row] += add
    numLeftDiag[col + (numQueens - row - 1)] += add


# finds the row in the column that has the fewest # of attacking queens (min-conflicts algorithm).
# this is where the queen will be moved to
# parameters: col - the index of the column that the queen is in
def minConflict(c):
    # initially set minimum # of conflicts equal to total # of queens
    minimum_conflict = numQueens
    # list to store the rows with minimum # of attacking queens
    minRows = []

    # iterate through each row in the column
    for r in range(numQueens):
        # calculate the total number of attacking queens by adding the number of queens in that row, left diagonal, and right diagonal
        conflicts = numRow[r] + numRightDiag[c + r] + \
            numLeftDiag[c + (numQueens - r - 1)]

        # if the number of queens is less than minimum_conflict, update minimum_conflict and set the minRows list as containing only the index of the current row
        if conflicts < minimum_conflict:
            minRows = [r]
            minimum_conflict = conflicts

        # if the number of queens is equal to minimum_conflict, append the row index to the list
        elif conflicts == minimum_conflict:
            minRows.append(r)

    # select randomly a row index from list of rows with smallest # of queens
    minRow = random.choice(minRows)
    return minRow


# heuristic that finds the column with the most # of attacking queens; will move queen in this column next
def maxCol():
    con = 0
    maximum_conflicts = 0
    # create a list to store the index of the max column
    conflictColsList = []

    # iterate through all the columns
    for c in range(0, numQueens):
        # get the row value for the current column (where the queen is currently placed)
        r = domain[c]
        # find the # of attacking queens
        con = numRow[r] + numRightDiag[c + r] + \
            numLeftDiag[c + (numQueens - r - 1)]
        # if the # of attacking queens is greater than the current max, then set the column as maximum_conflictsCol and update maximum_conflicts
        if (con > maximum_conflicts):
            conflictColsList = [c]
            maximum_conflicts = con
        # if the column ties with the current max column, then append the index value to the conflictColsList list
        elif con == maximum_conflicts:
            conflictColsList.append(c)
    # Randomly choose from the list of tied columns
    maxCol = random.choice(conflictColsList)
    return maxCol, maximum_conflicts


# sets up an initial domain by calling createInitialdomain() and then returns true if a solution is found
# returns false if a solution is not found under the given number of iterations
def solve():
    global infiniteLoop

    # if there was an infinite loop detected, create a random domain
    if (infiniteLoop == True):
        createRandomdomain()
    else:
        # else, call createInitialdomain() to create a domain that's "close" to the solution
        createInitialdomain()
    # counts the number of iterations
    iteration = 0
    # keeps track of the movement of the queen between iterations
    positions = []

    # # of iterations that the program will run for during each new attempt to find a solution
    # keep it under numQueens to allow the program to run faster; stop an attempt if a solution is not found within the max # of iterations and start a new attempt
    # for smaller domain sizes, totalIterations needs to be increased so that there are enough iterations to successfully reach a solution
    if numQueens < 100:
        totalIterations = numQueens
    else:
        totalIterations = 0.6 * numQueens

    # continue while current # of iterations doesn't exceed max iterations
    while (iteration < totalIterations):
        # find the column with the most attacking queens
        # return the column index and the # of attacking queens
        col, numConflicts = maxCol()
        # print("conflicts:", numConflicts)
        # print("col:", col)
        # if the total # of conflicts is greater than 3 (1 in row, 1 in left diagonal, and 1 in right diagonal), then there are more than 1 attacking queen
        if (numConflicts > 3):
            # call minConflict to find the row the move the queen to (returns the row with the smallest # of attacking queens)
            position = minConflict(col)
            # append the position that the queen is moving to to the positions list
            positions.append(position)
            # if position is different from the queen's current position:
            if (position != domain[col]):
                # call updateConflicts with add= -1 to remove 1 from the rows, left diagonal, and right diagonal lists
                updateConflicts(col, domain[col], -1)
                # replace the row index in domain[col] with the new row index to show the queen's new position
                domain[col] = position
                # call updateConflicts with add = 1 to add 1 to the rows, left diagonal, and right diagonal lists of the queen's new position
                updateConflicts(col, domain[col], 1)
        # if total # of conflicts is 3 (1 in row, 1 in left diagonal, and 1 in right diagonal), then there is only 1 attacking queen so the queen doesn't need to be moved
        elif numConflicts == 3:
            # solution is found
            return True
        iteration += 1

    # if there are only 2 distinct values in the positions list, then there is an infinite loop (queen keeps moving back and forth between 2 spots, never reaching a solution)
    if (len(set(positions)) == 2):
        infiniteLoop = True

    # no solution is found after max # of iterations is reached
    return False


# read from file containing # of queens (n)
def readInput():
    numQueensList = []
    with open('input.txt', 'r') as file:
        # create a list to store all of the values of n that we need to find a solution for
        for line in file:
            # store each value of n into the list
            numQueensList.append(int(line.rstrip('\n')))
    file.close()
    # clear the output file
    open('output.txt', 'w').close()
    # return the list
    return numQueensList


# create an output file to insert the solutions into
def writeOutput():
    # add 1 to each index value in the solution list to improve readability
    # ex. turns index 0 into index 1 to represent the 1st square from the top of the chess domain in a given column
    for i in range(len(domain)):
        domain[i] += 1

    solution = str(domain)
    with open('output.txt', 'a', 64) as file:
        # write the list containing the solution to output file
        file.write(solution + "\n\n")
    file.close()


def printDomain(domain, numQueens):
    # print(domain)
    row = [['-' for x in range(0, numQueens)] for y in range(0, numQueens)]
    for i in range(numQueens):
        num = domain[i] - 1
        row[i][num] = 'Q'

    for i in row:
        print(*i)

    return(row)

# this function is called to initiate the program


def main():
    # use global keyword so that we can modify each variable inside the function
    global numQueens
    global domain
    global numRow
    global numRightDiag
    global numLeftDiag
    global infiniteLoop

    # call the function that reads the input file and returns the list of #s of queens (n)
    numQueensList = readInput()
    # iterate through the list of #s of queens and return a solution for each
    for num in numQueensList:
        # set numQueens as equal to the # of queens read from input file
        numQueens = num
        # initially set infiniteLoop as false
        infiniteLoop = False
        # start the timer to count how long it takes to find a solution
        startTime = time.time()
        # whether or not a solution has been found
        solved = False
        print("# of Queens (n): " + str(num))

        # while not solved, will continue to call solve to try and find a solution
        while (solved == False):
            # returns solved if a solution is found, false otherwise
            solved = solve()
        new_array = list(range(0, numQueens))
        plt.plot(new_array, domain, 'ro')
        plt.axis([0, numQueens, 0, numQueens])
        plt.show()
        # writes the solution to the output file
        writeOutput()

        # figures out the time it took to find a solution and outputs it in the console
        endTime = time.time()
        totalTime = endTime - startTime
        timeStr = str(trunc(totalTime * 100) / 100)
        print("Solution found in " + timeStr + " seconds\n")
        printDomain(domain, numQueens)
           for i in range(len(domain)):
                domain[i] += 1
            print(domain)


if __name__ == '__main__':
    main()
