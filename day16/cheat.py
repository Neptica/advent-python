import copy
import sys
import time

start_time = 0
minDist = sys.maxsize
routes = [[]]


def combineRouties(draw):
    global routes

    for i in range(len(draw)):
        for j in range(len(draw[0])):
            if draw[i][j] == "+" and routes[i][j] != "+":
                routes[i][j] = "+"


def isSafe(input, visited, y, x):
    return (
        x >= 0
        and x < len(input[0])
        and y >= 0
        and y < len(input)
        and input[y][x] != "#"
        and (not visited[y][x])
    )


def findShortestPath(
    input, dir, visited, posY, posX, goalY, goalX, currDist, weigths, part, draw
):
    global minDist
    global routes

    if currDist > weigths[posY][posX] + 1000:
        return
    if minDist <= currDist and part == 1:
        return
    if posY == goalY and posX == goalX:
        if currDist < minDist:
            routes = copy.deepcopy(input)
            minDist = currDist
            combineRouties(draw)
        if currDist == minDist:
            minDist = currDist
            combineRouties(draw)
        return

    visited[posY][posX] = True
    weigths[posY][posX] = currDist
    draw[posY][posX] = "+"

    # check right cell
    if isSafe(input, visited, posY, posX + 1):
        distInc = 1001 if dir[1] == False else 1
        findShortestPath(
            input,
            [False, True, False, False],
            visited,
            posY,
            posX + 1,
            goalY,
            goalX,
            currDist + distInc,
            weigths,
            part,
            draw,
        )
    # check above cell
    if isSafe(input, visited, posY + 1, posX):
        distInc = 1001 if dir[0] == False else 1
        findShortestPath(
            input,
            [True, False, False, False],
            visited,
            posY + 1,
            posX,
            goalY,
            goalX,
            currDist + distInc,
            weigths,
            part,
            draw,
        )
    # check bottom cell
    if isSafe(input, visited, posY - 1, posX):
        distInc = 1001 if dir[2] == False else 1
        findShortestPath(
            input,
            [False, False, True, False],
            visited,
            posY - 1,
            posX,
            goalY,
            goalX,
            currDist + distInc,
            weigths,
            part,
            draw,
        )
    # check left cell
    if isSafe(input, visited, posY, posX - 1):
        distInc = 1001 if dir[3] == False else 1
        findShortestPath(
            input,
            [False, False, False, True],
            visited,
            posY,
            posX - 1,
            goalY,
            goalX,
            currDist + distInc,
            weigths,
            part,
            draw,
        )

    visited[posY][posX] = False
    draw[posY][posX] = "."


def solve(part):
    input = []
    visited = []
    weights = []
    # directions: up, right, down, left
    dir = [False, True, False, False]
    posX = 0
    posY = 0
    goalX = 0
    goalY = 0

    # read the input
    with open("input.txt", "r") as file:
        for line in file:
            line = line.strip()  # 47217
            row = []
            for char in line:
                row.append(char)
            input.append(row)

    # find the start/end positions and create visited and weigths matrix
    for y in range(len(input)):
        row = []
        weigh_row = []
        for x in range(len(input[0])):
            row.append(False)
            weigh_row.append(sys.maxsize)
            if input[y][x] == "S":
                posY = y
                posX = x
            elif input[y][x] == "E":
                goalY = y
                goalX = x
        visited.append(row)
        weights.append(weigh_row)

    # find shortest path
    sys.setrecursionlimit(3500)
    draw = copy.deepcopy(input)
    findShortestPath(
        input, dir, visited, posY, posX, goalY, goalX, 0, weights, part, draw
    )

    if part == 1:
        print("final: ", minDist)
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        part_two_count = 1  # I never account for the exit cell thats why 1
        for i in routes:
            part_two_count += i.count("+")
        print("final_part_two: ", part_two_count)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    start_time = time.time()
    solve(1)
    start_time = time.time()
    solve(2)
