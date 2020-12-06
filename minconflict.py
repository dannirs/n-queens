from math import trunc
import math
import random
import time

# initially set # of queens/board size as 0
DIM = 0  
# store board in a list
board = []  
# keep track of # of queens in each row, left diagonal, and right diagonal 
row_conflicts = []  
diagr_conflicts = []  
diagl_conflicts = []  


# read from file containing # of queens (n)
def readInFile():
    with open('input.txt', 'r') as file:
        # create a list to store all of the values of n that we need to find a solution for
        dimensionArray = []
        for line in file:
            # store each value of n into the list
            dimensionArray.append(int(line.rstrip('\n')))
    file.close()
    # clear the output file
    open('output.txt', 'w').close()
    # return the list
    return dimensionArray


# create an output file to insert the solutions into
def writeToFile():
    # add 1 to each index value in the solution list to improve readability
    # ex. turns index 0 into index 1 to represent the 1st square from the top on the chess board in a given column
    solutionArrayStr = str([x + 1 for x in board])
    with open('output.txt', 'a', 64) as file:
        # write the list containing the solution to output file
        file.write(solutionArrayStr + "\n\n")
    file.close()


# whenever a queen is moved to/from a position, there will be changes made to the row, left diagonal, and
# right diagonal lists that store the # of queens. this function updates the lists.
# parameters: col - column that queen is moved to/from
# row - row that the queen is moved to/from
# val - if 1 (queen is moved to a position), will add a queen to the list; 
# if -1 (queen is moved from a position), will subtract a queen from the list 
def changeConflicts(col, row, val):
    # update the row, right diagonal, and left diagonal that the queen is moved from/to by either adding
    # or subtracting 1 
    row_conflicts[row] += val
    diagr_conflicts[col + row] += val
    diagl_conflicts[col + (DIM - row - 1)] += val

# Finds the index of the best new queen position. Ties are broken randomly.
# Parameter: the current column index


# finds the row in the column that has the fewest # of attacking queens (min conflict heuristic).
# this is where the queen will be moved to
# parameters: col - the index of the column that the queen is in 
def minConflictPos(col):
    # initially set minimum # of conflicts equal to total # of queens 
    minConflicts = DIM
    # list to store the rows with minimum # of attacking queens 
    minConflictRows = []
    
    # iterate through each row in the column
    for row in range(DIM):
        # calculate the total number of attacking queens by adding the number of queens in that row, left diagonal, and right diagonal 
        conflicts = row_conflicts[row] + diagr_conflicts[col + row] + diagl_conflicts[col + (DIM - row - 1)]
        # if there are no queens that can currently attack that row, immediately return the row index because it has the smallest # of conflicts 
        if conflicts == 0:
            return row
        # if the number of queens is less than minConflicts, update minConflicts and set the minConflictRows list as containing only the index of the current row
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        # if the number of queens is equal to minConflicts, append the row index to the list instead
        elif conflicts == minConflicts:
            minConflictRows.append(row)
    # randomly choose a row index from the list of rows with smallest # of queens
    choice = random.choice(minConflictRows)
    return choice


# creates an initial board 
def createBoard():
    # create global variables so that we can modify each variable outside of the current function
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts

    # create a list to store the chess board
    board = []

    # initialize the lists for # of queens in each row, left diagonal, and right diagonal
    # the size of the lists are the # of rows and # of diagonals in the board 
    # initially, there are 0 queens in each list
    row_conflicts = [0] * DIM
    diagr_conflicts = [0] * ((2 * DIM) - 1)
    diagl_conflicts = [0] * ((2 * DIM) - 1)

    # create an ordered set of all row index values
    rowSet = set(range(0, DIM))
    # create a list that keeps track of which queens have not been placed in the board
    notPlaced = []

    # iterate through each column
    for col in range(0, DIM):
        # test a row in the column by popping the first row index out of the set of all rows
        testRow = rowSet.pop()
        # add the total # of queens that can attack the square using col and testRow
        conflicts = row_conflicts[testRow] + diagr_conflicts[col + testRow] + diagl_conflicts[col + (DIM - testRow - 1)]
        # if there are 0 attacking queens, then immediately place the queen at that position
        # this is to make as "good" an initial board as possible to make it easier to find a solution
        if conflicts == 0:
            # append the row index to the board list to show the queen's positioning
            board.append(testRow)
            # update row and diagonal lists, passing val = 1 to show that conflicts need to be added
            changeConflicts(col, board[col], 1)
        
        else:
            # if there are attacking queens, then add the row to the back of the set to test it again later
            rowSet.add(testRow)
            # pop the next row from the set to test
            testRow2 = rowSet.pop()
            conflicts2 = row_conflicts[testRow2] + diagr_conflicts[col + testRow2] + diagl_conflicts[col + (DIM - testRow2 - 1)]
            # if there are no attacking queens, place the queen at that location and append the row index to the board, update conflicts
            if conflicts2 == 0:
                board.append(testRow2)
                changeConflicts(col, board[col], 1)
            else:
                # Otherwise, add this row at the back of the set as well to test it later
                rowSet.add(testRow2)
                # add "none" to the board to show that the column has not yet been filled
                board.append(None)
                # append the column index to the notPlaced list to come back to that column later
                notPlaced.append(col)

    # after iterating through all columns in the board, iterate through the list of all columns that have not yet been placed
    for col in notPlaced:
        # place the queen at the first row in rowSet, regardless of if there are conflicts or not to finish creating the initial board
        board[col] = rowSet.pop()
        # update row and diagonal lists, passing val = 1 to show that conflicts need to be added
        changeConflicts(col, board[col], 1)
 

# heuristic that finds the column with the most # of attacking queens
def findMaxConflictCol():
    conflicts = 0
    maxConflicts = 0
    # create a list to store the index of the max column in
    maxConflictCols = []

    # iterate through all the columns
    for col in range(0, DIM):
            # get the row value for the current column (where the queen is currently placed)
            row = board[col]
            # find the # of attacking queens
            conflicts = row_conflicts[row] + diagr_conflicts[col + row] + diagl_conflicts[col + (DIM - row - 1)]
            # if the # of attacking queens is greater than the current max, then set the column as maxConflictsCol and update maxConflicts
            if (conflicts > maxConflicts):
                    maxConflictCols = [col]
                    maxConflicts = conflicts
            # if the column ties with the current max column, then append the index value to the maxConflictCols list
            elif conflicts == maxConflicts:
                    maxConflictCols.append(col)
    # Randomly choose from the list of tied columns
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts


# sets up an initial board by calling createBoard() and then returns true if a solution is found
# returns false if a solution is not found under the given number of iterations
def solveNQueens():
    createBoard()
    # counts the number of iterations
    iteration = 0

    # # of iterations that the program will run for during each new attempt to find a solution
    # keep it under DIM to allow the program to run faster; stop an attempt if a solution is not found within the max # of iterations and start a new attempt
    # for smaller board sizes, maxIteration needs to be increased so that there are enough iterations to successfully reach a solution
    if DIM < 100:
        maxIteration = DIM
    else:
        maxIteration = 0.6 * DIM
        
    # continue while current # of iterations doesn't exceed max iterations 
    while (iteration < maxIteration):
        # find the column with the most attacking queens 
        # return the column index and the # of attacking queens
        col, numConflicts = findMaxConflictCol()

        # if the total # of conflicts is greater than 3 (1 in row, 1 in left diagonal, and 1 in right diagonal), then there are more than 1 attacking queen
        if (numConflicts > 3):
            # call minConflictPos to find the row the move the queen to (returns the row with the smallest # of attacking queens) 
            newLocation = minConflictPos(col)
            # if newLocation is different from the queen's current position:
            if (newLocation != board[col]):
                # call changeConflicts with val = -1 to remove 1 from the rows, left diagonal, and right diagonal lists
                changeConflicts(col, board[col], -1)
                # replace the row index in board[col] with the new row index to show the queen's new position
                board[col] = newLocation
                # call changeConflicts with val = 1 to add 1 to the rows, left diagonal, and right diagonal lists of the queen's new position
                changeConflicts(col, newLocation, 1)
        # if total # of conflicts is 3 (1 in row, 1 in left diagonal, and 1 in right diagonal), then there is only 1 attacking queen so the queen doesn't need to be moved
        elif numConflicts == 3:
            # solution is found
            return True
        iteration += 1
    # no solution is found after max # of iterations is reached 
    return False


# this function is called to initiate the program
def main():
    # create global variables so that we can modify each variable outside of the current function
    global DIM
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts

    # call the function that reads the input file and returns the list of #s of queens (n)
    dimensionArray = readInFile()

    # iterate through the list of #s of queens and return a solution for each 
    for dimension in dimensionArray:
        # If the dimension is outside the constraints
        if dimension <= 3 or dimension > 10000000:
            # Print error and write empty array to file
            print("Cannot build board of size: " + str(dimension))
            writeToFile()
        else:
            # set DIM as equal to the # of queens 
            DIM = dimension
            # start the timer to count how long it takes to find a solution
            time0 = time.time()
            # whether or not a solution has been found
            solved = False
            print("Searching for board configuration of size " + str(dimension) + "...")
            # print a hard-coded solution for 6 
            if (DIM == 6):
                board = [1, 3, 5, 0, 2, 4]
                
            # while not solved, will continue to call solveNQueens to try and find a solution 
            while (not solved):
                # returns solved if a solution is found, false otherwise
                solved = solveNQueens()

            print("Board configuration found for size " + str(dimension))
            
            # writes the solution to the output file
            writeToFile()
            
            # calculates the time it took to find a solution and prints it in the console
            time1 = time.time()
            tot_time = time1 - time0
            time_string = str(trunc(tot_time * 100) / 100)
            print("   Took " + time_string + " seconds\n")


main()
