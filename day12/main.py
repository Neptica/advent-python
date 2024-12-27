m = [line.strip() for line in open("./input.txt")]
# print(m)


def dfs(pos, letter, seen):
    i, j = pos
    if (
        not (-1 < i < len(m))
        or not (-1 < j < len(m[0]))
        or m[i][j] != letter
        or pos in seen
    ):
        return set()

    seen.add(pos)
    seen |= dfs((i + 1, j), letter, seen)
    seen |= dfs((i, j + 1), letter, seen)
    seen |= dfs((i - 1, j), letter, seen)
    seen |= dfs((i, j - 1), letter, seen)
    return seen

def rightcheck(i, j, weights, m):
    # Either both right and up are both the same or none of them are for corners
    # Corners are counted for each Letter involved in making that corner
    # It is not possible to have three letters for a single corner, only 2 and 4
    # Account for same only in diagonal, equals 4 corners
    # AB
    # BC

    res = 0
    diagonal = (m[i][j] == m[i-1][j+1] and m[i][j] not in (m[i-1][j], m[i][j+1])) or ( m[i-1][j] == m[i][j+1] and m[i-1][j] not in (m[i][j], m[i-1][j+1]))

    letters = {}
    spot = j + i * 1j
    d = -1j

    for _ in range(4):
        if m[int(spot.imag)][int(spot.real)] in letters:
            letters[m[int(spot.imag)][int(spot.real)]].append((int(spot.imag), int(spot.real)))
        else:
            letters[m[int(spot.imag)][int(spot.real)]] = [(int(spot.imag), int(spot.real))]
        spot += d
        d *= 1j

    if diagonal: # Four Corners Automatically
        res += weights[i][j] + weights[i-1][j] + weights[i-1][j+1] + weights[i][j+1]
    else:
        for pos in letters.values():
            if len(pos) % 2 != 0:
                y, x = pos[0]
                res += weights[y][x]

    return res


def sol():
    calculated = set()
    weights = [[0 for _ in enumerate(m)] for _ in enumerate(m[0])]
    for i, line in enumerate(m):
        for j, c in enumerate(line):
            if (i, j) in calculated:
                continue
            new = dfs((i, j), c, set())
            for y, x in new:
                weights[y][x] = len(new)
            calculated |= new

    # for line in weights:
    #     print(line)

    ans = 0
    for i, line in enumerate(m):
        for j, c in enumerate(line):
            match (0 < i < len(m) - 1, 0 < j < len(line) - 1):
                case (False, False):
                    ans += weights[i][j] # All Corners
                    if j == 0 and line[j] != m[i][j+1]:
                        ans += weights[i][j] + weights[i][j+1] # Top and Bottom Edge check on left corners

                    if i == len(m) - 1 and m[i][j] != m[i-1][j]:
                        ans += weights[i][j] + weights[i-1][j] # Upwards edge check on bottom corner
                    if i == len(m) - 1 and j == 0:
                        ans += rightcheck(i, j, weights, m)

                case (True, False):
                    if line[j] != m[i-1][j]:
                        ans += weights[i][j] + weights[i-1][j] # Right and Left Edge
                    if j < len(line) - 1:
                        ans += rightcheck(i, j, weights, m)
                    # Need to check rightwards too
                case (False, True):
                    if line[j] != line[j+1]:
                        ans += weights[i][j] + weights[i][j+1] # Top and Bottom Edge
                    if i == len(m) - 1:
                        ans += rightcheck(i, j, weights, m)
                case (True, True):
                    # Either both right and up are both the same or none of them are for corners
                    # Corners are counted for each Letter involved in making that corner
                    # It is not possible to have three letters for a single corner, only 2 and 4
                    # Account for same only in diagonal, equals 4 corners
                    # AB
                    # BC
                    ans += rightcheck(i, j, weights, m)

    print(ans)



sol()
