def read_file(filename):
    results = set()
    guard = (0, 0)
    with open(filename, "r", encoding="utf-8") as file:
        m = file.readlines()
        y = len(m)
        x = len(m[0].strip())
        for i, line in enumerate(m):
            for j, c in enumerate(line):
                if c == "#":
                    results.add((i, j))
                elif c == "^":
                    guard = (i, j)

        m = [list(line.strip()) for line in m]
        return results, guard, y, x, m


blocks, gloc, h, w, m = read_file("./input.txt")


def check(blocks, pos, d):
    fpos = pos + d
    if (int(fpos.imag), int(fpos.real)) in blocks:
        fpos -= d
        d *= 1j
        fpos += d
    fd = d
    while -1 < int(fpos.imag) < h and -1 < int(fpos.real) < w:
        # ensure slow moves
        m[int(pos.imag)][int(pos.real)] = "S"
        m[int(fpos.imag)][int(fpos.real)] = "F"
        m[int(pos.imag)][int(pos.real)] = "."
        m[int(fpos.imag)][int(fpos.real)] = "."
        while True:
            pos += d
            if (int(pos.imag), int(pos.real)) in blocks:
                pos -= d
                d *= 1j
            else:
                break

        # fast moves twice
        n = 0
        while n < 2:
            fpos += fd
            if (int(fpos.imag), int(fpos.real)) in blocks:
                fpos -= fd
                fd *= 1j
            else:
                n += 1

        if pos == fpos and fd == d:
            return True

    return False


def part_one():
    pos = gloc[1] + gloc[0] * 1j
    d = -1j
    ans = 0
    been = set()
    for y in range(int(pos.imag), -1, -1):
        if m[y][gloc[1]] == "#":
            break
        been |= {gloc[1] + y * 1j}

    while -1 < int(pos.imag + d.imag) < h and -1 < int(pos.real + d.real) < w:
        while (
            (int(pos.imag), int(pos.real)) not in blocks
            and -1 < int(pos.imag + d.imag) < h
            and -1 < int(pos.real + d.real) < w
        ):
            m[int(pos.imag)][int(pos.real)] = "C"
            m[int(pos.imag)][int(pos.real)] = "."
            if (
                int(pos.imag + d.imag),
                int(pos.real + d.real),
            ) not in blocks and pos + d not in been:
                been.add(pos)
                m[int(pos.imag + d.imag)][int(pos.real + d.real)] = "#"
                curr = (int(pos.imag + d.imag), int(pos.real + d.real))
                ans += check(
                    blocks | {curr},
                    pos,
                    d * 1j,
                )
                m[int(pos.imag + d.imag)][int(pos.real + d.real)] = "."
            elif (
                int(pos.imag + d.imag),
                int(pos.real + d.real),
            ) in blocks:
                d *= 1j

            pos += d

    print(ans)


part_one()
