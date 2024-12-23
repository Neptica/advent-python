from collections import deque


def read_file(filename):
    results = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            results.append(list(int(x) for x in line.strip().split(",")))
    return results


def part_one(m, l, w, fallen_bytes):
    for index in range(fallen_bytes):
        i = l[index][1]  # Y
        j = l[index][0]  # X
        print(i, j)
        m[i][j] = "#"

    # print(m)
    visited = set()
    queue = deque()
    queue.append((0, 0))
    count = 0
    while queue:
        new = deque()

        for _ in range(len(queue)):
            i, j = queue.popleft()
            visited.add((i, j))
            m[i][j] = "X"
            if (i, j) == (w - 1, w - 1):
                return count

            if i + 1 < len(m) and m[i + 1][j] != "#":
                if (i + 1, j) not in visited:
                    visited.add((i + 1, j))
                    new.append((i + 1, j))

            if j + 1 < len(m[0]) and m[i][j + 1] != "#":
                if (i, j + 1) not in visited:
                    visited.add((i, j + 1))
                    new.append((i, j + 1))

            if i - 1 >= 0 and m[i - 1][j] != "#":
                if (i - 1, j) not in visited:
                    visited.add((i - 1, j))
                    new.append((i - 1, j))

            if j - 1 >= 0 and m[i][j - 1] != "#":
                if (i, j - 1) not in visited:
                    visited.add((i, j - 1))
                    new.append((i, j - 1))

            m[i][j] = "."

        queue = new
        count += 1
    return -1


if __name__ == "__main__":
    byte_list = read_file("./input.txt")
    WIDTH = 71  # 0 to 70 inclusive
    FALLEN = 12

    # part one
    # layout = [["." for _ in range(WIDTH)] for _ in range(WIDTH)]
    # ans = part_one(layout, byte_list, WIDTH, FALLEN)
    # print(ans)

    # part two
    ans2 = 0
    for i, byte in enumerate(byte_list):
        layout = [["." for _ in range(WIDTH)] for _ in range(WIDTH)]
        res2 = part_one(layout, byte_list, WIDTH, i + 1)
        if res2 == -1:
            print(byte, i)
            ans2 = i
            break

    # print(byte_list[ans2 + 1])
