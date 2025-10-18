"""Day 13 of advent of code"""

import math

import numpy as np


def read_input(filename):
    result = []
    with open(filename, "r", encoding="utf-8") as file:
        temp = []
        for i, line in enumerate(file):
            if i % 4 == 3:
                continue
            if i % 4 == 2:
                line = line.replace(",", "").split()[1:]
                temp.extend(list(map(lambda s: int(s[2:]) + 10000000000000, line)))
                # temp.extend(list(map(lambda s: int(s[2:]), line)))
                result.append(temp)
                temp = []
            else:
                line = line.replace(",", "").split()[2:]
                temp.extend(list(map(lambda s: int(s[2:]), line)))

        # data_in = [list(process_data(line.split()[1:]) for line in file)]
    return result


def pt2(inp):
    tokens = 0
    for buttons in inp:
        a = buttons[:2]
        b = buttons[2:4]
        goals = buttons[4:]

        # c = int(l[1][2:-1]) + add
        # d = int(l[2][2:]) + add
        # a = (c*y2 - d*x2) / (x1*y2 - y1*x2)
        # b = (d*x1 - c*y1) / (x1*y2 - y1*x2)

        aPress = (goals[0] * b[1] - goals[1] * b[0]) / (a[0] * b[1] - a[1] * b[0])
        bPress = (goals[1] * a[0] - goals[0] * a[1]) / (a[0] * b[1] - a[1] * b[0])

        if aPress == int(aPress) and bPress == int(bPress):
            print(aPress, bPress, buttons)
            tokens += int(aPress * 3 + bPress)
        # else:
        # print(z)

    print(tokens)


if __name__ == "__main__":
    data = read_input("./input.txt")
    # print(data)
    pt2(data)
