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
                    guard = j + i * 1j

        m = [list(line.strip()) for line in m]
        return results, guard, y, x, m


blocks, gloc, h, w, m = read_file("./input.txt")


def walk(blocks, pos, d):
    ans = set()
    while -1 < int(pos.imag) < h and -1 < int(pos.real) < w and (pos, d) not in ans:
        ans.add((pos, d))
        pos += d
        if (int(pos.imag), int(pos.real)) in blocks:
            pos -= d
            d *= 1j
    return {p for p, _ in ans}, (pos, d) in ans


walked = walk(blocks, gloc, -1j)[0]
print(
    len(walked),
    sum(walk(blocks | {(int(p.imag), int(p.real))}, gloc, -1j)[1] for p in walked),
)
