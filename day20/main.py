import sys

# Increase recursion depth
sys.setrecursionlimit(50000)


def read_file(filename):
    result = []
    start = ()
    end = ()
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            s = line.find("S")
            e = line.find("E")
            if s > -1:
                start = (i, s)
            if e > -1:
                end = (i, e)

            result.append(line.strip())
    return result, start, end


def dfs(m, visited, cheats, p, psec, time, cheat, prev):
    if p in visited:
        return 0

    if m[p[0]][p[1]] == "#":
        if cheat == 0:
            return 0
        cheat -= 1
    elif prev[1] == "#":
        cheats.add((prev[0], p))  # need to weed out similar cheats
        cheat = 0
    else:
        # legal to legal move
        prev = [p, m[p[0]][p[1]]]

    if m[p[0]][p[1]] == "E":
        return 1 if psec <= time else 0

    r1, r2, r3, r4 = 0, 0, 0, 0

    prev[1] = m[p[0]][p[1]]
    visited.add(p)
    if p[0] - 1 > -1 and (cheat != 0 or m[p[0] - 1][p[1]] != "#"):
        r1 = dfs(m, visited, cheats, (p[0] - 1, p[1]), psec + 1, time, cheat, prev)

    if p[1] + 1 < len(m[0]) and (cheat != 0 or m[p[0]][p[1] + 1] != "#"):
        r2 = dfs(m, visited, cheats, (p[0], p[1] + 1), psec + 1, time, cheat, prev)

    if p[0] + 1 < len(m) and (cheat != 0 or m[p[0] + 1][p[1]] != "#"):
        r3 = dfs(m, visited, cheats, (p[0] + 1, p[1]), psec + 1, time, cheat, prev)

    if p[1] - 1 > -1 and (cheat != 0 or m[p[0]][p[1] - 1] != "#"):
        r4 = dfs(m, visited, cheats, (p[0], p[1] - 1), psec + 1, time, cheat, prev)
    visited.remove(p)

    return r1 + r2 + r3 + r4


if __name__ == "__main__":
    layout, begin, finish = read_file("./test.txt")
    distance = 0
    for line in layout:
        print(line)
        for c in line:
            if c in (".", "E"):
                distance += 1
    print(begin, finish, distance)
    count = set()
    ans = dfs(layout, set(), count, begin, 0, distance, 2, ((), ""))
    print(ans, len(count))
