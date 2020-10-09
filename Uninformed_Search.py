from collections import deque


class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None

    def addNode(self, i):
        if self.parent is not None:
            self.parent.addNode(i)
        else:
            self.parent = Node(i)

    def printTree(self):
        pass

    def printParent(self):
        print(self.parent)


expandedNodes = Node(0)
pathCost = Node(0)


def main():
    # List of the variables to be used
    fileName = "grid.txt"
    bfs = True
    goal = [4, 4]
    start = [1, 1]
    maze = readGrid(fileName)
    # print("\nGrid read from file: " + str(maze))
    path = uninformedSearch(maze, start, goal, bfs)
    print("The Number of expanded Nodes are: " + str(expandedNodes.value))
    print("The Path cost was: " + str(pathCost.value))
    print(path)
    outputGrid(maze, start, goal, path)


def uninformedSearch(grid, start, goal, bfs):
    current = Node([1, 1])
    closedList = [start]
    openList = deque()
    found = False
    path = []
    sort = []

    print("\nopen list: " + str(openList))
    print("closed list: " + str(closedList))
    print("Current Value:" + str(current.value))

    if bfs:
        for x in range(0, 30):
            movements = expandNode(closedList, current, grid)
            parent = current.value
            print("Temp: " + str(movements))

            if len(movements) > 1:
                sort.append(movements[1])
                print(sort)
                print(parent)
            for y in sort:
                print(y)
                if y == parent:
                    print("The imposter was: " + str(parent))
                    parent = [1, 1]
            current.value = movements[0]
            current.addNode(parent)
            for i in movements:

                if openList.count(i) < 1:
                    openList.append(i)
                    expandedN()
                    #current.printTree()
                elif i == goal:
                    current.value = i
                    print("Found It!")
                    path = setPath(current, path)
                    return path

            current.value = openList.popleft()
            closedList.append(current.value)

            print("\nopen list: " + str(openList))
            print("closed list: " + str(closedList))


    elif not bfs:
        for x in range(0, 30):
            temp = expandNode(closedList, current, grid)
            parent = current.value
            print("Temp: " + str(temp))
            for i in temp:
                if openList.count(i) < 1:
                    openList.append(i)
                    expandedN()
                    current.value = temp
                    current.parent = parent
                    #current.printTree()
                elif i == goal:
                    current.value = i
                    print("Found It!")
                    path = setPath(current, path)
                    return path

            current.value = openList.popl()
            closedList.append(current.value)

            print("\nopen list: " + str(openList))
            print("closed list: " + str(closedList))
            print("Current Value:" + str(current.value))


def expandedN():
    expandedNodes.value += 1


def getNeighbors(location, grid):
    neighbors = []
    a = 1
    b = 0
    for i in location:
        if grid[location[0] - a][location[1] - b] == 0:
            neighbors.append([location[0] - a, location[1] - b])
        if grid[location[0] + a][location[1] + b] == 0:
            neighbors.append([location[0] + a, location[1] + b])
        a, b = b, a
    return neighbors


def expandNode(closedList, location, grid):
    neighborsTemp = getNeighbors(location.value, grid)
    for i in closedList:
        for j in neighborsTemp:
            if i == j:
                neighborsTemp.remove(j)
                break
    return neighborsTemp


def setPath(position, path):
    path.append(position.value)
    print("the path is: " + str(path))
    if position.parent:
        setPath(position.parent, path)
    for i in path:
        if i == [1, 1]:
            path.remove([1, 1])
    path.sort()
    pathCost.value = len(path)
    return path


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
# 1 1 1 1 1
# 1 0 0 0 1
# 1 0 0 0 1
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


if __name__ == "__main__":
    main()
