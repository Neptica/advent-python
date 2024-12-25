import sys

sys.setrecursionlimit(50000)


def read_file(filename):
    results = []
    guard = (0, 0)
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            results.append(list(line.strip()))
            pos = line.find("^")
            if pos > -1:
                guard = (i, pos)
    return results, guard


def dfs(m, p, d, visited, turns, checking):
    if (p[0], p[1], d) in turns and len(turns) > 1:
        return 1

    if not checking:
        visited.add((p[0], p[1]))

    directions = ["^", ">", "v", "<"]
    prev = m[p[0]][p[1]]
    m[p[0]][p[1]] = directions[d]
    m[p[0]][p[1]] = prev

    match d:
        case 0:
            if p[0] > 0:
                check = 0

                if m[p[0] - 1][p[1]] == "#":
                    turns.add((p[0], p[1], d))
                    return dfs(m, (p[0], p[1]), 1, visited, turns, checking)

                if (p[0] - 1, p[1]) not in visited and not checking:
                    check = dfs(m, (p[0], p[1]), 1, visited, { (p[0], p[1], 0) }, True)
                    turns = set()
                return dfs(m, (p[0] - 1, p[1]), d, visited, turns, checking) + check

            return 0
        case 1:
            if p[1] + 1 < len(m[0]):
                check = 0

                if m[p[0]][p[1] + 1] == "#":
                    turns.add((p[0], p[1], d))
                    return dfs(m, (p[0], p[1]), 2, visited, turns, checking)

                if (p[0], p[1] + 1) not in visited and not checking:
                    check = dfs(m, (p[0], p[1]), 2, visited, { (p[0], p[1], 1) }, True)
                    turns = set()

                return dfs(m, (p[0], p[1] + 1), d, visited, turns, checking) + check
            return 0
        case 2:
            if p[0] + 1 < len(m):
                check = 0

                if m[p[0] + 1][p[1]] == "#":
                    turns.add((p[0], p[1], d))
                    return dfs(m, (p[0], p[1]), 3, visited, turns, checking)

                if (p[0] + 1, p[1]) not in visited and not checking:
                    check = dfs(m, (p[0], p[1]), 3, visited, { (p[0], p[1], 2) }, True)
                    turns = set()

                return dfs(m, (p[0] + 1, p[1]), d, visited, turns, checking) + check
            return 0

        case 3:
            if p[1] > 0:
                check = 0

                if m[p[0]][p[1] - 1] == "#":
                    turns.add((p[0], p[1], d))
                    return dfs(m, (p[0], p[1]), 0, visited, turns, checking)

                if (p[0], p[1] - 1) not in visited and not checking:
                    check = dfs(m, (p[0], p[1]), 0, visited, { (p[0], p[1], 3) }, True)
                    turns = set()

                return dfs(m, (p[0], p[1] - 1), d, visited, turns, checking) + check
            return 0
    return 0


if __name__ == "__main__":
    data = read_file("./input.txt")

    for l in data[0]:
        for c in l:
            print(c, end="")
        print()
    print(data[1])

    visited = { (y, data[1][1]) for y in range(data[1][0] + 1) }
    ans = dfs(data[0], data[1], 0, set(), set(), False)
    print(ans)
