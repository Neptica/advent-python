import math


def read_file(filename):
    result = []
    with open(filename, "r", encoding="utf-8") as file:

        for line in file:
            temp = []
            parts = line.strip().replace("p=", "").replace("v=", "").split(" ")
            for part in parts:
                temp.extend(part.split(","))
            result.append([int(x) for x in temp])
    return result


def part_one(inp):
    # 101 wide 103 tall for input and 11, 7 for test
    wide = 101
    tall = 103
    mid_y = math.floor(tall / 2)
    mid_x = math.floor(wide / 2)
    print(mid_x, mid_y)

    result = [[0, 0], [0, 0]]
    for parts in inp:
        p = parts[:2]
        v = parts[2:]
        p_x = (p[0] + v[0] * 100) % wide
        p_y = (p[1] + v[1] * 100) % tall
        if p_x != mid_x and p_y != mid_y:
            x = 0 if p_x < mid_x else 1
            y = 0 if p_y < mid_y else 1
            result[x][y] += 1

    result = result[0] + result[1]
    print(result)
    answer = 1
    for num in result:
        answer *= num
    return answer


def part_two(inp):
    # 101 wide 103 tall for input and 11, 7 for test
    wide = 101
    tall = 103
    layout = []
    print(layout)
    seconds = 0

    user_in = ""
    while user_in != "exit":
        user_in = input("Type anything to continue and 'exit' to quit: ")
        temp = [[1 for _ in range(wide)] for _ in range(tall)]
        for parts in inp:
            x = (parts[0] + parts[2]) % wide
            y = (parts[1] + parts[3]) % tall
            parts[0] = x
            parts[1] = y
            temp[y][x] = 0
        layout = temp
        seconds += 1
        print(layout)
        print(seconds)

    return 0


if __name__ == "__main__":
    data = read_file("./input.txt")
    # print(data)
    ans = part_one(data)
    print("Answer is", ans)
    answer = part_two(data)
