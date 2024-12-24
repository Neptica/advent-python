from collections import deque


def read_file(filename):
    results = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            results.append(int(line.strip()))

    return results


# Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number.
#       Finally, prune the secret number.
# Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
#       Then, mix this result into the secret number. Finally, prune the secret number.
# Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number.
#       Finally, prune the secret number.


def part_one(prices):
    ans = 0
    totals = [
        [[[0 for _ in range(19)] for _ in range(19)] for _ in range(19)]
        for _ in range(19)
    ]
    # current gets reset while adding to totals
    current = [
        [[[0 for _ in range(19)] for _ in range(19)] for _ in range(19)]
        for _ in range(19)
    ]

    current_changes = deque()
    for debug, initial in enumerate(prices):

        visited = set()
        curr = initial
        prev = initial % 10
        for _ in range(2000):
            curr = ((curr * 64) ^ curr) % 16777216
            curr = ((curr // 32) ^ curr) % 16777216
            curr = ((curr * 2048) ^ curr) % 16777216

            current_changes.append(curr % 10 - prev)
            if len(current_changes) > 4:
                current_changes.popleft()
            if len(current_changes) == 4:
                (
                    i,
                    j,
                    k,
                    l,
                ) = (
                    current_changes[0] + 9,
                    current_changes[1] + 9,
                    current_changes[2] + 9,
                    current_changes[3] + 9,
                )
                if (i, j, k, l) not in visited:
                    # not max because the second number of the same sequence could never be bought
                    # indices have been left adjusted because changes are within [-9, 9]
                    current[i][j][k][l] += curr % 10
                visited.add((i, j, k, l))
                # if (i - 9, j - 9, k - 9, l - 9) == (-2, 1, -1, 3):
                #     print(debug, curr % 10)

            prev = curr % 10

        # add current to totals and zero out current
        for i, a in enumerate(totals):
            for j, b in enumerate(a):
                for k, c in enumerate(b):
                    for l, _ in enumerate(c):
                        totals[i][j][k][l] += current[i][j][k][l]
                        current[i][j][k][l] = 0

        ans += curr

    answer2 = 0
    # indices = []
    for i, a in enumerate(totals):
        for j, b in enumerate(a):
            for k, c in enumerate(b):
                for l, value in enumerate(c):
                    answer2 = max(answer2, value)
                    # indices.append((i - 9, j - 9, k - 9, l - 9))
                    # if (i - 9, j - 9, k - 9, l - 9) == (-2, 1, -1, 3):
                    #     correct = value

    return ans, answer2


if __name__ == "__main__":
    inp = read_file("./input.txt")
    print(inp)
    answer, ans2 = part_one(inp)
    print(answer)
    print(ans2)
