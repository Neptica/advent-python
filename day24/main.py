def read_file(filename):
    activity = {}
    connections = {}
    end_wires = []
    with open(filename, "r", encoding="utf-8") as file:
        first = True
        for line in file:
            line = line.strip()
            if line == "":
                first = False
                continue
            if first:
                activity[line[: line.find(":")]] = int(line[-1:])
            else:
                line = line.split(" ")
                connections[line[-1]] = line[:3]
                end_wires.append(line[-1])
    return activity, connections, sorted(end_wires)


def part_one(inp):
    bits = ""
    activity = inp[0]
    connections = inp[1]
    end_wires = inp[2]
    while True:
        prev = bits
        bits = ""
        for wire in end_wires:
            makeup = connections[wire]
            b1 = activity.get(makeup[0], 0)
            op = makeup[1]
            b2 = activity.get(makeup[2], 0)

            bit = ""
            if op == "AND":
                bit = str(b1 & b2)
            elif op == "OR":
                bit = str(b1 | b2)
            elif op == "XOR":
                bit = str(b1 ^ b2)
            else:
                print("Error")
            activity[wire] = int(bit)
            bits += bit
        if prev == bits:
            break

    ans = ""
    for wire in end_wires[::-1]:  # Big endian
        if wire[0] != "z":
            break  # reverse alphabetical
        ans += str(activity[wire])
    print("Part One:", int(ans, 2), ans)


def part_two(inp):
    activity = inp[0]
    connections = inp[1]
    end_wires = inp[2]
    print(connections)
    for wire in end_wires[::-1]:  # Big endian
        if wire[0] != "z":
            break

    # ans = ""
    # for wire in end_wires[::-1]:  # Big endian
    #     if wire[0] != "z":
    #         continue
    #     ans += str(activity[wire])
    # x = ""
    # for wire in activity:  # Big endian
    #     if wire[0] != "x":
    #         continue
    #     x += str(activity[wire])
    # y = ""
    # for wire in activity:  # Big endian
    #     if wire[0] != "y":
    #         continue
    #     y += str(activity[wire])
    # a, b, c = 0, 0, 0
    # for con in connections:
    #     op = connections[con][1]
    #     if op == "AND":
    #         a += 1
    #     elif op == "OR":
    #         b += 1
    #     if op == "XOR":
    #         c += 1
    # print("AND", a, "OR", b, "XOR", c, len(x), len(y), len(ans))
    # # print("Part Two:", int(x, 2), "+", int(y, 2), "=", int(ans, 2), ans)


if __name__ == "__main__":
    data = read_file("./input.txt")
    # print(data[0], "\n\n\n", data[1], "\n\n\n", data[2])
    part_one(data)
    part_two(data)
