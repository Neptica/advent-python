from typing import DefaultDict

board = [line for line in open("./input.txt").read().splitlines()]
path = [[-1 for _ in board[0]] for _ in board]

s = (0, 0)
for i, line in enumerate(board):
    j = line.find("S")
    if j != -1:
        s = (i, j)
        break

stack = [(s, 0)]
while stack:
    (i, j), count = stack.pop()
    if board[i][j] == "#":
        continue
    if not 0 < j < len(board) - 1 or not 0 < i < len(board) - 1:
        continue
    if path[i][j] != -1:
        continue

    path[i][j] = count
    for nc, nr in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        stack.append(((nc, nr), count + 1))

# for line in path:
#     print(line, sep="\t")


shortcuts = DefaultDict(int)

ans = 0
visited = set()
cheats = set()
CHEAT = 20 + 1
stacks = [(s, 0)]
while stacks:
    (i, j), count = stacks.pop()
    if board[i][j] == "#":
        continue
    if not 0 < j < len(board) - 1 or not 0 < i < len(board) - 1:
        continue
    if (i, j) in visited:
        continue

    visited.add((i, j))
    for sc in range(CHEAT):
        for sr in range(CHEAT - sc):
            for nr, nc in [(sc, sr), (-sc, sr), (sc, -sr), (-sc, -sr)]:
                if not 0 < nc + i < len(path) - 1 or not 0 < nr + j < len(path[0]) - 1:
                    continue
                if path[nc + i][nr + j] == -1:
                    continue

                time_saved = path[nc + i][nr + j] - path[i][j] - sc - sr
                if time_saved >= 100 and ((nc + i, nr + j), (i, j)) not in cheats:
                    cheats.add(((nc + i, nr + j), (i, j)))
                    shortcuts[time_saved] += 1
                    ans += 1

    for nc, nr in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        stacks.append(((nc, nr), count + 1))

for [length, count] in shortcuts.items():
    print(count, ": ", length)
print(ans)
