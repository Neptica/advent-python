def read_file(filename):
    data = [[], []]  # Locks, keys
    with open(filename, "r", encoding="utf-8") as file:
        new = True
        curr = 0
        obj = [-1 for _ in range(5)]
        for line in file:
            line = line.strip()
            if line == "":
                data[curr].append(obj)
                obj = [-1 for _ in range(5)]
                new = True
                continue
            if new:
                curr = 0 if line[0] == "#" else 1
                new = False
            for i, c in enumerate(line):
                obj[i] += 1 if c == "#" else 0
        data[curr].append(obj)
        obj = [0 for _ in range(5)]

    return data


def part_one(inp):
    locks = inp[0]
    keys = inp[1]

    ans = 0
    for key in keys:
        for lock in locks:
            valid = True
            for i in range(5):
                if key[i] + lock[i] > 5:
                    valid = False
            if valid:
                ans += 1

    print(ans)


if __name__ == "__main__":
    data = read_file("./input.txt")
    print(data[0])
    print("\n\n\n")
    print(data[1])

    part_one(data)
