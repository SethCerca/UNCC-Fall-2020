#!/usr/bin/env python3.6

# import queue
# Access to queue.Queue and Queue.LifoQueue
# myList = queue.Queue()
# or myList = Queue.LifoQueue()
# myList.put(), myList.get()

import heapq
import random
import math


# Node class to hold the location and parent node (needed for getting final path)
class Node:

    def __init__(self, value, par, h=0.0, g=0.0):
        self.value = value
        self.parent = par
        self.h = h
        self.g = g
        self.f = g + h

    def setF(self):
        self.f = self.h + self.g

    def __lt__(self, other):
        self_mag = self.f
        other_mag = other.f
        return self_mag < other_mag

    def __gt__(self, other):
        self_mag = self.f
        other_mag = other.f
        return self_mag > other_mag

    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.value, self.parent, self.h, self.f)


# The grid values must be separated by spaces, e.g.
# 1 1 1 1 1
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
# Returns a 2D list of 1s and 0s
def readGrid(filename):
    # print('In readGrid')
    grid = []
    with open(filename) as f:
        for l in f.readlines():
            grid.append([int(x) for x in l.split()])

    f.close()
    # print 'Exiting readGrid'
    return grid


# Writes a 2D list of 1s and 0s with spaces in between each character
# It will change the start location to 'S', goal to 'G', and path points to '*'
# 1 1 1 1 1
# 1 S * * 1
# 1 0 0 G 1
# 1 1 1 1 1
def outputGrid(grid, start, goal, path):
    # print('In outputGrid')
    filenameStr = 'path.txt'

    # Open filename
    f = open(filenameStr, 'w')

    # Mark the start and goal points
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'

    # Mark intermediate points with *
    for i, p in enumerate(path):
        if i > 0 and i < len(path) - 1:
            grid[p[0]][p[1]] = '*'

    # Write the grid to a file
    for r, row in enumerate(grid):
        for c, col in enumerate(row):

            # Don't add a ' ' at the end of a line
            if c < len(row) - 1:
                f.write(str(col) + ' ')
            else:
                f.write(str(col))

        # Don't add a '\n' after the last line
        if r < len(grid) - 1:
            f.write("\n")

    # Close file
    f.close()


# print('Exiting outputGrid')


# Generates a random grid
def genGrid():
    print('In genGrid')
    f = open('grid.txt', 'w')

    num_rows = 10
    num_cols = 10

    grid = [[0] * num_cols for i in range(0, num_rows)]

    max_cost = 9
    ob_cost = 0

    for i_r in range(0, num_rows):
        for i_c in range(0, num_cols):

            # Default to obstacle cost
            cost = ob_cost

            # Chance to be an obstacle
            chance = random.random()
            if chance > 0.2:
                # Generate a random cost for the location
                cost = random.randint(1, max_cost)

                # Don't add a ' ' to the end of the grid
                if i_c == num_cols - 1:
                    f.write(str(cost))
                else:
                    f.write(str(cost) + ' ')
            else:
                if i_c == num_cols - 1:
                    f.write(str(0))
                else:
                    f.write(str(0) + ' ')

            grid[i_r][i_c] = cost

        # New line in the grid
        f.write("\n")

    f.close()
    return grid


def printGrid(grid):
    for i in range(len(grid)):
        print(grid[i])


def InList(node, theList):
    for n in theList:
        if n.value == node.value:
            return True
    return False


def printNodeList(l):
    for node in l:
        print(node.value)


# Returns all adjacent locations for node that are free space
def getNeighbors(location, grid):
    # print('In getNeighbors')

    result = []

    # Use location[:] to get a copy of the list
    # For each direction (u,r,d,l), check the bounds and value on the grid
    # Clockwise order -> u, r, d, l

    up = location[:]
    up[0] -= 1
    if up[0] > -1 and grid[up[0]][up[1]] != 0:
        result.append(up)

    right = location[:]
    right[1] += 1
    if right[1] < len(grid[right[0]]) and grid[right[0]][right[1]] != 0:
        result.append(right)

    down = location[:]
    down[0] += 1
    if down[0] < len(grid) and grid[down[0]][down[1]] != 0:
        result.append(down)

    left = location[:]
    left[1] -= 1
    if left[1] > -1 and grid[left[0]][left[1]] != 0:
        result.append(left)

    # print('Exiting getNeighbors')
    return result


# Gets all children for node and adds them to the openList if possible
def expandNode(node, openList, openListCopy, closedList, grid, algo, goal):
    # print('In expandNode')

    neighbors = getNeighbors(node.value, grid)
    # for n in neighbors:
    #    nd = Node(n, node)

    #    if not InList(nd, closedList) and not InList(nd, openListCopy):
    #        openList.put(nd)
    #        openListCopy.append(nd)

    if algo == 'astar':
        for n in neighbors:
            nd = Node(n, node)
            nd.h = (math.pow(goal[0] - n[0], 2) + math.pow(goal[1] - n[1], 2))
            nd.g = grid[n[0]][n[1]]
            nd.setF()

            if not InList(nd, closedList) and not InList(nd, openListCopy):
                heapq.heappush(openList, nd)
                openListCopy.append(nd)

        openList.sort()

    else:
        for n in neighbors:
            nd = Node(n, node)
            nd.h = (math.pow(goal[0] - n[0], 2) + math.pow(goal[1] - n[1], 2))
            nd.setF()

            if not InList(nd, closedList) and not InList(nd, openListCopy):
                heapq.heappush(openList, nd)
                openListCopy.append(nd)

        openList.sort()

    # print('Exiting expandNode')


# Sets the path variable by inserting each node on the current node's path
def setPath(current, path, grid):
    # print('In setPath')

    # While not at the root, append each node's parent
    while current.parent != '':
        path.insert(0, current.parent.value)
        current = current.parent

    # print('Exiting setPath')


def uninformedSearch(type, grid, start, goal):
    # print('\nIn uninformedSearch')
    print('\nStarting search, type: %s start: %s goal: %s' % (type, start, goal))

    # Set initial variables
    current = Node(start, '', 0.0, 0.0)
    path = []

    # The open list is a heap
    openList = []
    heapq.heapify(openList)

    # List of nodes in the open list
    # This is needed because you cannot iterate over a Queue object
    openListCopy = []

    # Initially, push the root node onto the open list
    openList.append(current)
    openListCopy.append(current)

    # List of expanded nodes
    closedList = []

    # Track the number of expanded nodes
    numExpanded = 0

    ###############################
    ###        Main Loop        ###
    ###############################

    # While we are not at the goal and we haven't expanded all nodes
    while len(openList) != 0:

        # Pop off open list
        current = heapq.heappop(openList)

        # Add to closed list
        closedList.append(current)

        # Check for goal
        if current.value == goal:
            break

        else:

            # Expand this node
            expandNode(current, openList, openListCopy, closedList, grid, type, goal)

            # Data
            numExpanded += 1

    # If we found the goal, then build the final path
    if len(openList) != 0 or current == goal:
        # Set the path variable
        setPath(current, path, grid)

        # Append the goal because setPath doesn't add that
        path.append(goal)

    return [path, numExpanded]


def main():
    print('\nStarting main function for Informed_Search program\n')
    # genGrid()
    grid = readGrid('grid.txt')

    # the path cost, removes the cost of the starting space
    pCost = -4
    print('Grid read from file: %s' % grid)

    # Ask for input
    algo = input('\nInput \"astar\" or \"greedy\"\n')
    # algo = 'A*'

    if algo != "astar" and algo != "greedy":
        print('Invalid input')

    else:
        start = [0, 0]
        goal = [3, 2]
        [p, numExpanded] = uninformedSearch(algo, grid, start, goal)
        for j in p:
            pCost += grid[j[0]][j[1]]

        if len(p) > 0:
            print('\nFinal path: %s' % p)
            print('\nNumber of nodes expanded: %d' % numExpanded)
            print('Path cost: %d' % pCost)
            outputGrid(grid, start, goal, p)
            print('\nUsing Manhattan distance')
            print('\n\nPath written to file path.txt')
        else:
            print('No path could be found')


if __name__ == '__main__':
    main()
    print('\nExiting normally')
