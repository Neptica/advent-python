import sys
import time

# Set a higher recursion limit

sys.setrecursionlimit(10000)


def read_file(filename):
    result = []
    pos = tuple()
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            j = line.find("S")
            if j > -1:
                pos = (i, j)
            result.append(list(line.strip()))

    return result, pos


# test, test2, input
# 7036, 11048, 85480
BEST = 7036


# S is always bottom left E is always top right, implement A* for speed
def dfs(m, visited, current_track, p, direction, score, best):
    weight = 1000
    if visited[p[0]][p[1]] + weight + 1 <= score:
        return float("infinity")

    if m[p[0]][p[1]] == "E":
        if score == best:
            for i, _ in enumerate(m):
                for j in range(len(m[0])):
                    if current_track[i][j] != float("infinity"):
                        m[i][j] = "O"
        return score

    prev = current_track[p[0]][p[1]]
    current_track[p[0]][p[1]] = min(current_track[p[0]][p[1]], score)
    visited[p[0]][p[1]] = min(visited[p[0]][p[1]], score)

    r1, r2, r3, r4 = (
        float("infinity"),
        float("infinity"),
        float("infinity"),
        float("infinity"),
    )

    if m[p[0] - 1][p[1]] != "#" and direction != 2:
        penalty = weight if direction != 0 else 0
        r1 = dfs(
            m, visited, current_track, (p[0] - 1, p[1]), 0, 1 + penalty + score, best
        )

    if m[p[0]][p[1] + 1] != "#" and direction != 3:
        penalty = weight if direction != 1 else 0
        r2 = dfs(
            m, visited, current_track, (p[0], p[1] + 1), 1, 1 + penalty + score, best
        )

    if m[p[0] + 1][p[1]] != "#" and direction != 0:
        penalty = weight if direction != 2 else 0
        r3 = dfs(
            m, visited, current_track, (p[0] + 1, p[1]), 2, 1 + penalty + score, best
        )

    if m[p[0]][p[1] - 1] != "#" and direction != 1:
        penalty = weight if direction != 3 else 0
        r4 = dfs(
            m, visited, current_track, (p[0], p[1] - 1), 3, 1 + penalty + score, best
        )

    current_track[p[0]][p[1]] = prev

    return min(r1, r2, r3, r4)


if __name__ == "__main__":
    layout, start = read_file("./input.txt")
    repeat = [
        [float("infinity") for _ in range(len(layout[0]))] for _ in range(len(layout))
    ]
    current = [
        [float("infinity") for _ in range(len(layout[0]))] for _ in range(len(layout))
    ]
    time_start = time.time()
    ans = dfs(layout, repeat, current, start, 1, 0, 0)
    print(ans)
    print(time.time() - time_start)

    # Part Two
    repeat = [
        [float("infinity") for _ in range(len(layout[0]))] for _ in range(len(layout))
    ]
    current = [
        [float("infinity") for _ in range(len(layout[0]))] for _ in range(len(layout))
    ]
    time_start = time.time()
    # 7036, 11048, 85480
    dfs(layout, repeat, current, start, 1, 0, ans)
    ans2 = 1  # end tile is not counted
    end = time.time() - time_start
    for line in layout:
        for c in line:
            print(c, end="")
            if c == "O":
                ans2 += 1
        print()

    print(ans2)
    print(end)
