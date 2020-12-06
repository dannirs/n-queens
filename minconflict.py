from math import trunc
import random
import time

# initially set # of queens/board size as 0
numQueens = 0  
# store board in a list
board = []  
# keep track of # of queens in each row, left diagonal, and right diagonal 
numRow = []  
numRightDiag = []  
numLeftDiag = []  
# determines if there's an infinite loop in the code that's preventing the program from finding a solution
infiniteLoop = False


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
    # ex. turns index 0 into index 1 to represent the 1st square from the top of the chess board in a given column
    for i in range(len(board)):
        board[i] += 1
        
    solution = str(board)
    with open('output.txt', 'a', 64) as file:
        # write the list containing the solution to output file
        file.write(solution + "\n\n")
    file.close()


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
def minConflict(col):
    # initially set minimum # of conflicts equal to total # of queens 
    minConflicts = numQueens
    # list to store the rows with minimum # of attacking queens 
    minRows = []
    
    # iterate through each row in the column
    for row in range(numQueens):
        # calculate the total number of attacking queens by adding the number of queens in that row, left diagonal, and right diagonal 
        conflicts = numRow[row] + numRightDiag[col + row] + numLeftDiag[col + (numQueens - row - 1)]
#         print(row, conflicts)

        # if the number of queens is less than minConflicts, update minConflicts and set the minRows list as containing only the index of the current row
        if conflicts < minConflicts:
            minRows = [row]
            minConflicts = conflicts
            
        # if the number of queens is equal to minConflicts, append the row index to the list instead
        elif conflicts == minConflicts:
            minRows.append(row)
            
    # randomly choose a row index from the list of rows with smallest # of queens
    minRow = random.choice(minRows)
#     print(minRow)
    return minRow


# heuristic that finds the column with the most # of attacking queens; will move queen in this column next
def maxCol():
    conflicts = 0
    maxConflicts = 0
    # create a list to store the index of the max column
    maxConflictCols = []

    # iterate through all the columns
    for col in range(0, numQueens):
            # get the row value for the current column (where the queen is currently placed)
            row = board[col]
            # find the # of attacking queens
            conflicts = numRow[row] + numRightDiag[col + row] + numLeftDiag[col + (numQueens - row - 1)]
            # if the # of attacking queens is greater than the current max, then set the column as maxConflictsCol and update maxConflicts
            if (conflicts > maxConflicts):
                    maxConflictCols = [col]
                    maxConflicts = conflicts
            # if the column ties with the current max column, then append the index value to the maxConflictCols list
            elif conflicts == maxConflicts:
                    maxConflictCols.append(col)
    # Randomly choose from the list of tied columns
    maxCol = random.choice(maxConflictCols)
    return maxCol, maxConflicts


# creates a random board (called if there's an infinite loop)
def createRandomBoard():
    # use global keyword so that we can modify each variable inside the function
    global board
    global numRow
    global numRightDiag
    global numLeftDiag

    # create a list to store the chess board
    board = []

    # initialize the lists for # of queens in each row, left diagonal, and right diagonal
    # the size of the lists are the # of rows and # of diagonals in the board 
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
        # append the row index to the board list to show the queen's positioning
        board.append(tryRow)
        # update row and diagonal lists, passing add = 1 to show that conflicts need to be added
        updateConflicts(col, tryRow, 1)
#         conflicts = numRow[tryRow] + numRightDiag[col + tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]
#         print("new conflicts: ", conflicts)
    
#     print(board)
#     for i in range(len(board)):
#         conflicts = numRow[board[i]] + numRightDiag[i + board[i]] + numLeftDiag[i + (numQueens - board[i] - 1)]
#         print(i, conflicts)
    

# creates an initial board 
def createInitialBoard():
    # use global keyword so that we can modify each variable inside the function
    global board
    global numRow
    global numRightDiag
    global numLeftDiag

    # create a list to store the chess board
    board = []

    # initialize the lists for # of queens in each row, left diagonal, and right diagonal
    # the size of the lists are the # of rows and # of diagonals in the board 
    # initially, there are 0 queens in each list
    numRow = [0] * numQueens
    numRightDiag = [0] * ((2 * numQueens) - 1)
    numLeftDiag = [0] * ((2 * numQueens) - 1)
#     for i in range(numQueens):
#         col = 0
#         conflicts = numRow[i] + numRightDiag[col + i] + numLeftDiag[col + (numQueens - i - 1)]
#         print(i, conflicts)

    # create an ordered set of all row index values
    rowsRemaining = set(range(0, numQueens))
    # create a list that keeps track of which columns have not been solved for 
    colsRemaining = []

    # iterate through each column
    for col in range(0, numQueens):
        # test a row in the column by popping the first row index out of the set of all rows
        tryRow = rowsRemaining.pop()
#         print("col: ", col)
#         print("tryRow: ", tryRow)

        # add the total # of queens that can attack the square using col and tryRow
        conflicts = numRow[tryRow] + numRightDiag[col + tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]
#         print("conflicts: ", conflicts)

        # if there are 0 attacking queens, then immediately place the queen at that position
        # this is to make as "good" an initial board as possible to make it easier to find a solution
        if conflicts == 0:
            # append the row index to the board list to show the queen's positioning
            board.append(tryRow)
            # update row and diagonal lists, passing add = 1 to show that conflicts need to be added
            updateConflicts(col, tryRow, 1)
#             conflicts = numRow[tryRow] + numRightDiag[col + tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]
#             print("new conflicts: ", conflicts)
        
        else:
            # if there are attacking queens, then add the row to the back of the set to test it again later
            rowsRemaining.add(tryRow)
            # pop the next row from the set to test
            tryRow = rowsRemaining.pop()
#             print("tryRow: ", tryRow)
            conflicts = numRow[tryRow] + numRightDiag[col + tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]
#             print("conflicts: ", conflicts)

            # if there are no attacking queens, place the queen at that location and append the row index to the board, update conflicts
            if conflicts == 0:
                board.append(tryRow)
                updateConflicts(col, tryRow, 1)
#                 conflicts = numRow[tryRow] + numRightDiag[col + tryRow] + numLeftDiag[col + (numQueens - tryRow - 1)]
#                 print("new conflicts: ", conflicts)
            else:
                # Otherwise, add this row at the back of the set as well to test it later
                rowsRemaining.add(tryRow)
                # add "none" to the board to show that the column has not yet been filled
                board.append(None)
                # append the column index to the colsRemaining list to come back to that column later
                colsRemaining.append(col)

    # after iterating through all columns in the board, iterate through the list of all columns that have not yet been placed
    for col in colsRemaining:
#         print("colsremaining")
        # place the queen at the first row in rowsRemaining, regardless of if there are conflicts or not to finish creating the initial board
        board[col] = rowsRemaining.pop()
#         print("tryrow: ", board[col])

        # update row and diagonal lists, passing add= 1 to show that conflicts need to be added
        updateConflicts(col, board[col], 1)
#         conflicts = numRow[board[col]] + numRightDiag[col + board[col]] + numLeftDiag[col + (numQueens - board[col] - 1)]
#         print("new conflicts: ", conflicts)
    
#     print(board)


# sets up an initial board by calling createInitialBoard() and then returns true if a solution is found
# returns false if a solution is not found under the given number of iterations
def solve():
    global infiniteLoop
    
    # if there was an infinite loop detected, create a random board
    if (infiniteLoop == True):
        createRandomBoard()
    else: 
        # else, call createInitialBoard() to create a board that's "close" to the solution
        createInitialBoard()
    # counts the number of iterations
    iteration = 0
    # keeps track of the movement of the queen between iterations
    positions = []

    # # of iterations that the program will run for during each new attempt to find a solution
    # keep it under numQueens to allow the program to run faster; stop an attempt if a solution is not found within the max # of iterations and start a new attempt
    # for smaller board sizes, totalIterations needs to be increased so that there are enough iterations to successfully reach a solution
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
#             print("position:", position)
            # append the position that the queen is moving to to the positions list
            positions.append(position)
            # if position is different from the queen's current position:
            if (position != board[col]):
                # call updateConflicts with add= -1 to remove 1 from the rows, left diagonal, and right diagonal lists
                updateConflicts(col, board[col], -1)
                # replace the row index in board[col] with the new row index to show the queen's new position
                board[col] = position
                # call updateConflicts with add = 1 to add 1 to the rows, left diagonal, and right diagonal lists of the queen's new position
                updateConflicts(col, board[col], 1)
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


# this function is called to initiate the program
def main():
    # use global keyword so that we can modify each variable inside the function
    global numQueens
    global board
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
        
        # writes the solution to the output file
        writeOutput()
        
        # calculates the time it took to find a solution and prints it in the console
        endTime = time.time()
        totalTime = endTime - startTime
        timeStr = str(trunc(totalTime * 100) / 100)
        print("Solution found in " + timeStr + " seconds\n")


main()
