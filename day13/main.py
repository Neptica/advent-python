"""Day 13 of advent of code"""


def process_data(elements):
    if not elements:
        return elements
    first = elements[0][0]
    index = 0
    if first in ("A", "B"):
        index += 1
    return [int(elements[index][2:]), int(elements[index + 1][2:])]


def read_input(filename):
    result = []
    with open(filename, "r", encoding="utf-8") as file:
        temp = []
        for i, line in enumerate(file):
            if i % 4 == 3:
                continue
            temp.extend(process_data(line.replace(",", "").split()[1:]))
            if i % 4 == 2:
                result.append(temp)
                temp = []

        # data_in = [list(process_data(line.split()[1:]) for line in file)]
    return result


def search(machine):
    unique = {(0, 0, 0, 0)}  # X, Y, A, B
    target = (machine[4], machine[5])

    # Awful code below
    # if (
    #     target[0] // max(machine[0], machine[2]) > 100
    #     or target[1] // max(machine[1], machine[3]) > 100
    # ):
    #     return 0

    n = 0  # how on earth does n bound fix this infinite loop
    while unique and n < 200:
        temp = set()
        for _ in range(len(unique)):
            dist = unique.pop()
            a_press = (dist[0] + machine[0], dist[1] + machine[1], dist[2] + 1, dist[3])
            b_press = (dist[0] + machine[2], dist[1] + machine[3], dist[2], dist[3] + 1)

            if a_press[0:2] == target:
                return a_press[2] * 3 + a_press[3]
            if b_press[0:2] == target:
                return b_press[2] * 3 + b_press[3]
            if a_press[2] <= 100:
                temp.add(a_press)
            if b_press[2] <= 100:
                temp.add(b_press)

        unique = temp
        n += 1
    return 0


def part_one(inp):
    total = 0
    for claw in inp:
        coins = search(claw)
        print(coins)
        total += coins
    return total


def s2(machine):
    target = (machine[4], machine[5])

    unique = {}  # X, Y, A, B
    start = 0
    biggest = max(machine[0:4])
    if biggest in (machine[0:2]):  # True means A is bigger
        if machine[0] > machine[1]:
            start = target[0] // machine[0]
            unique = {(machine[0] * start, machine[1] * start, start, 0)}
        else:
            start = target[1] // machine[1]
            unique = {(machine[0] * start, machine[1] * start, start, 0)}
    else:
        if machine[2] > machine[3]:
            start = target[0] // machine[2]
            unique = {(machine[0] * start, machine[1] * start, 0, start)}
        else:
            start = target[1] // machine[3]
            unique = {(machine[0] * start, machine[1] * start, 0, start)}

    while unique:
        temp = set()
        for _ in range(len(unique)):
            dist = unique.pop()
            a_redact = (
                dist[0] - machine[0],
                dist[1] - machine[1],
                dist[2] - 1,
                dist[3],
            )
            b_press = (dist[0] + machine[2], dist[1] + machine[3], dist[2], dist[3] + 1)

            if a_redact[0:2] == target:
                return a_redact[2] * 3 + a_redact[3]
            if b_press[0:2] == target:
                return b_press[2] * 3 + b_press[3]

            if a_redact[0] <= target[0] and a_redact[1] <= target[1]:
                temp.add(a_redact)
            if b_press[0] <= target[0] and b_press[1] <= target[1]:
                temp.add(b_press)

        unique = temp
    return 0


def part_two(inp):
    total = 0
    for claw in inp:
        coins = s2(claw[0:4] + [claw[4] + 10000000000000, claw[5] + 10000000000000])
        print(coins)
        total += coins
    return total


if __name__ == "__main__":
    data = read_input("./input.txt")
    # print(data)
    # ans = part_one(data)
    # print(ans)
    answer = part_two(data)
    print(answer)
