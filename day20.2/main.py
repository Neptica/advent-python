import sys
from functools import cache
from typing import DefaultDict

# Increase recursion depth
sys.setrecursionlimit(50000)

board = open("./test.txt").read().splitlines()
s = (0, 0)
for i in range(len(board)):
    pos_start = board[i].find("S")
    if pos_start != -1:
        s = (i, pos_start)  # in i,j / y,x
track_length = sum([l in (".", "E") for line in board for l in line])

board = [list(line) for line in board]


def dfs(pos):
    path = [[float("inf") for _ in board] for _ in board]
    stack = [(pos, 0)]
    while stack:
        p, count = stack.pop()
        if not 0 <= p[0] < len(board) or not 0 <= p[1] < len(board[0]):
            continue
        elif board[p[0]][p[1]] == "#":
            continue
        if path[p[0]][p[1]] <= count:
            continue
        path[p[0]][p[1]] = count

        for p in [
            (p[0], p[1] + 1),
            (p[0] + 1, p[1]),
            (p[0], p[1] - 1),
            (p[0] - 1, p[1]),
        ]:
            stack.append((p, count + 1))

    # for line in path:
    #     print(line)
    return path


path = dfs(s)
cheats = set()


@cache
def twoi(p, psec, cheat_count, last, last_legal):
    shortcuts = DefaultDict(int)
    count = 0
    stack = [(p, psec, cheat_count, last, last_legal)]
    while stack:
        p, psec, cheat, last, last_legal = stack.pop()
        if (
            not 0 < p[0] < len(board) - 1
            or not 0 < p[1] < len(board[0]) - 1
            or path[p[0]][p[1]] < psec
        ):
            continue

        if board[p[0]][p[1]] == "#":
            cheat -= 1
            if cheat == 0:  # or last_legal in cheatsStart:
                continue
        else:
            # check if we just got out of a cheat
            if last != last_legal:
                # check if this cheat has been done before or has no advantage
                if psec < path[p[0]][p[1]] and (last_legal, p) not in cheats:
                    count += 1
                    cheats.add((last_legal, p))
                    shortcuts[path[p[0]][p[1]] - psec] += 1
                continue
            last_legal = p

        stack.append(((p[0] - 1, p[1]), psec + 1, cheat, p, last_legal))
        stack.append(((p[0], p[1] - 1), psec + 1, cheat, p, last_legal))
        stack.append(((p[0] + 1, p[1]), psec + 1, cheat, p, last_legal))
        stack.append(((p[0], p[1] + 1), psec + 1, cheat, p, last_legal))

    for [key, pair] in shortcuts.items():
        print(pair, ": ", key)
    return count


print(twoi(s, 0, 2, s, s))
# print(twoi(s, 0, 2, s, s))
