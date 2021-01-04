import random
import math


class Board():

    def __init__(self, numRowsCols):
        self.cells = [[0] * numRowsCols for i in range(numRowsCols)]
        self.numRows = numRowsCols
        self.numCols = numRowsCols

        # negative value for initial h...easy to check if it's been set or not
        self.h = -1

    # Print board
    def printBoard(self):
        for row in self.cells:
            print(row)

    # Randomize the board
    def rand(self):
        self.cells = [[0] * self.numRows for i in range(self.numRows)]
        for row in self.cells:
            i = random.randint(0, self.numCols - 1)
            row[i] = 1

    # Swap two locations on the board
    def swapLocs(self, a, b):
        temp = self.cells[a[0]][a[1]]
        self.cells[a[0]][a[1]] = self.cells[b[0]][b[1]]
        self.cells[b[0]][b[1]] = temp


# Cost function for a board
def numAttackingQueens(board):
    # Collect locations of all queens
    locs = []
    for r in range(len(board.cells)):
        for c in range(len(board.cells[r])):
            if board.cells[r][c] == 1:
                locs.append([r, c])
    # print 'Queen locations: %s' % locs

    result = 0

    # For each queen (use the location for ease)
    for q in locs:

        # Get the list of the other queen locations
        others = [x for x in locs if x != q]
        # print 'q: %s others: %s' % (q, others)

        count = 0
        # For each other queen
        for o in others:
            # print 'o: %s' % o
            diff = [o[0] - q[0], o[1] - q[1]]

            # Check if queens are attacking
            if o[0] == q[0] or o[1] == q[1] or abs(diff[0]) == abs(diff[1]):
                count = count + 1

        # Add the amount for this queen
        result = result + count

    return result


# Move any queen to another square in the same column
# successors all the same
def getSuccessorStates(board):
    result = []

    for i_row, row in enumerate(board.cells):
        # Get the column the queen is on in this row
        # [0] because list comprehension returns a list, even if only one element
        # This line will crash if the board has not been initialized with rand() or some other method
        i_queen = [i for i, x in enumerate(row) if x == 1][0]

        # For each column in the row
        for i_col in range(board.numCols):

            # If the queen is not there
            if row[i_col] != 1:
                # Make a copy of the board
                bTemp = Board(board.numRows)
                bTemp.cells[:] = [r[:] for r in board.cells]

                # Now swap queen to i_col from i_queen
                bTemp.swapLocs([i_row, i_col], [i_row, i_queen])
                # bTemp.printBoard()
                result.append(bTemp)

    return result


# Returns the new T value
def linearScheduling(T, decayRate):
    return T * decayRate


# Prints the size of the board
def printHeader(boardSize):
    print("\n     ==================")
    print("       Board Size: " + str(boardSize))
    print("     ==================")


# prints the decay rate and the T threshold
def printValues(tThreshold, decayRate):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Decay Rate: " + str(decayRate) + ", T Threshold: " + str(tThreshold))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# Executes Simulated Annealing to get the next board
def simAnnealing(boards, board, T, decayRate, tThreshold):
    prob = 0

    # Finds the next board in the sequence
    while T > tThreshold:
        T = linearScheduling(T, decayRate)
        rand = random.randint(0, 11)
        newBoard = boards[rand]
        deltaE = numAttackingQueens(board) - numAttackingQueens(newBoard)
        if deltaE > 0:
            board = newBoard
        else:
            prob = math.exp(deltaE / T)
            r = random.random()
            if prob > r:
                board = newBoard
    return board


# Calculates and prints the average h-cost
def getAverage(hAverage):
    h = 0
    # print("hAverage = " + str(hAverage))
    for x in hAverage:
        h += x
    print("H = " + str(h))
    h = h / len(hAverage)
    print('Average h-cost of final solutions: ' + str(h))


def main():

    decayRates = [0.9, 0.75, 0.5]
    tThresholds = [0.000001, 0.0000001, 0.00000001]
    boardSize = [4, 8, 16]

    # Iterates through all of the board sizes
    for i in boardSize:
        board = Board(i)
        printHeader(i)

        # iterates through all of the value states
        for j in range(len(decayRates)):
            printValues(tThresholds[j], decayRates[j])
            T = 100
            hAverage = []
            # Generates the next 10 boards in the sequence
            for x in range(0, 10):
                print("\nRun: " + str(x))
                print("Initial board: ")
                board.rand()
                board.printBoard()
                print("h-value: " + str(numAttackingQueens(board)))
                board = simAnnealing(getSuccessorStates(board), board, T, decayRates[j], tThresholds[j])
                h = numAttackingQueens(board)
                hAverage.append(h)
                print("Final board h-value: " + str(h))
                board.printBoard()

            getAverage(hAverage)


if __name__ == '__main__':
    main()
    print('\nExiting normally')
