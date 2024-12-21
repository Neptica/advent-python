import sys

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


# S is always bottom left E is always top right, implement A* for speed
def dfs(m, p, direction, visited, score):
    # Direction, NESW -> 0123
    if p in visited and visited[p] + 1000 <= score:
        # 1000 incase orientation is different
        return float("infinity")

    if m[p[0]][p[1]] == "E":
        return score

    visited[p] = score  # overwrite any high scores and find new paths
    weight = 1000

    scores = []
    if m[p[0] - 1][p[1]] != "#":
        p1 = dfs(
            m,
            (p[0] - 1, p[1]),
            0,
            visited,
            1 + abs((direction - 0) % 3) * weight + score,
        )
        scores.append(p1)
    if m[p[0]][p[1] + 1] != "#":
        p2 = dfs(
            m, (p[0], p[1] + 1), 1, visited, 1 + abs(direction - 1) * weight + score
        )
        scores.append(p2)
    if m[p[0] + 1][p[1]] != "#":
        p3 = dfs(
            m, (p[0] + 1, p[1]), 2, visited, 1 + abs(direction - 2) * weight + score
        )
        scores.append(p3)
    if m[p[0]][p[1] - 1] != "#":
        p4 = dfs(
            m,
            (p[0], p[1] - 1),
            3,
            visited,
            1 + abs((direction - 3) % 3) * weight + score,
        )
        scores.append(p4)

    return min(scores)


if __name__ == "__main__":
    layout, start = read_file("./input.txt")
    # print(layout, start)
    ans = dfs(layout, start, 1, {}, 0)
    print(ans)
