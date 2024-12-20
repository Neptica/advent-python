import curses
from collections import deque


def read_file(filename):
    layout_m = []
    path_r = []
    processing_map = True
    i = 0
    pos = (0, 0)
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if line.strip() == "":
                processing_map = False
                continue
            if processing_map:
                temp = []
                for j, c in enumerate(line.strip()):
                    if c == "@":
                        temp.extend(["@", "."])
                        pos = [i, j * 2]
                        print(pos)
                    elif c == "O":
                        temp.extend(["[", "]"])
                    else:
                        temp.extend([c, c])

                layout_m.append(temp)
            else:
                path_r.extend(list(line.strip()))
            i += 1
    return layout_m, path_r, pos


def print_map(stdscr, pages, direction):
    current_page = 0
    n = 1  # starting position is not kept in pages
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Page {current_page + 1}/{len(pages)}")
        stdscr.addstr(2, 0, pages[current_page])
        stdscr.addstr(6, 20, f"Next Move: {direction[n]}")
        stdscr.addstr(14, 0, "Press 'n' for next, 'p' for previous, 'q' to quit.")
        stdscr.refresh()

        n += 1

        if current_page >= len(pages) or n >= len(direction):
            break
        key = stdscr.getkey()
        if key == "n" and current_page < len(pages) - 1:
            current_page += 1
        elif key == "p" and current_page > 0:
            current_page -= 1
        elif key == "q":
            break


def get_score(layout):
    answer = 0
    for i, line in enumerate(layout):
        for j, c in enumerate(line):
            if c == "O":
                answer += 100 * i + j
    return answer


def legalmove(layout, start, d):
    p = (start[0] + d[0], start[1] + d[1])

    while layout[p[0]][p[1]] == "O":
        p = (p[0] + d[0], p[1] + d[1])

        if layout[p[0]][p[1]] == ".":
            layout[start[0] + d[0]][start[1] + d[1]], layout[p[0]][p[1]] = (
                layout[p[0]][p[1]],
                layout[start[0] + d[0]][start[1] + d[1]],
            )
            return True, layout
    return False, layout


def part_one(layout, path, curr):
    pages = []
    pos = curr

    for line in layout:
        for c in line:
            print(c, end="")
        print()

    for d in path:
        if d == ">":
            check, layout = legalmove(layout, pos, (0, 1))
            if check:
                pos[1] += 1
                layout[pos[0]][pos[1] - 1] = "."
                layout[pos[0]][pos[1]] = "@"
        elif d == "v":
            check, layout = legalmove(layout, pos, (1, 0))
            if check:
                pos[0] += 1
                layout[pos[0] - 1][pos[1]] = "."
                layout[pos[0]][pos[1]] = "@"
        elif d == "<":
            check, layout = legalmove(layout, pos, (0, -1))
            if check:
                pos[1] -= 1
                layout[pos[0]][pos[1] + 1] = "."
                layout[pos[0]][pos[1]] = "@"
        elif d == "^":
            check, layout = legalmove(layout, pos, (-1, 0))
            if check:
                pos[0] -= 1
                layout[pos[0] + 1][pos[1]] = "."
                layout[pos[0]][pos[1]] = "@"
        # temp = ""
        # for line in layout:
        #     for c in line:
        #         temp += c
        #     temp += "\n"
        # pages.append(temp)

    # curses.wrapper(print_map, pages, path)

    # for line in layout:
    #     for c in line:
    #         print(c, end="")
    #     print()

    return get_score(layout)


def legal(m, start, direction, visited):
    """dfs to check if a wall blocks the box, if it does return False for illegal move"""
    obs = m[start[0] + direction[0]][start[1] + direction[1]]
    if obs == ".":
        return True
    if obs == "#":
        return False

    if direction[0] != 0:
        # moving up and down require special checks
        if tuple(start) in visited:
            return True
        visited.add((start[0], start[1]))
        if obs == "]":
            return legal(
                m,
                (start[0] + direction[0], start[1]),
                direction,
                visited,  # only Y moves
            ) and legal(m, (start[0], start[1] - 1), direction, visited)
        if obs == "[":
            return legal(
                m,
                (start[0] + direction[0], start[1]),
                direction,
                visited,  # only Y moves
            ) and legal(m, (start[0], start[1] + 1), direction, visited)
    else:
        return legal(m, (start[0], start[1] + direction[1]), direction, set())


def moveboxes(m, start, direction):
    if direction[0] != 0:
        new = m.copy()
        # parameter is passed as the first obstacle, needs to be person
        y = start[0] - direction[0]
        x = start[1]

        queue = set()
        queue.add((y, x))

        ####################
        ##....[]....[]..[]##
        ##............[]..##
        ##..[][]....[]..[]##
        ##...[].......[]..##
        ##[]##....[]......##
        ##[]......[]..[]..##
        ##..[][]..@[].[][]##
        ##........[]......##
        ####################

        go = list(queue)
        while queue:
            q2 = set()
            for _ in range(len(queue)):
                (i, j) = queue.pop()
                obs = m[i + direction[0]][j]
                if obs in ("[", "]", "@"):
                    q2.add((i + direction[0], j))
                    if obs == "[":
                        q2.add((i + direction[0], j + 1))
                    else:
                        q2.add((i + direction[0], j - 1))
            queue = q2
            go += q2

        for i, j in go[::-1]:
            new[i + direction[0]][j] = m[i][j]
            if (i - direction[0], j) not in go:
                new[i][j] = "."

        return new

    coords = [start[0], start[1]]
    prev = "."
    obs = m[coords[0]][coords[1]]
    while obs in ("[", "]"):
        m[coords[0]][coords[1]] = prev
        prev = obs
        coords[1] += direction[1]
        tmp = m[coords[0]][coords[1]]
        m[coords[0]][coords[1]] = obs
        obs = tmp

    return m


def get_score2(layout):
    answer = 0
    for i, line in enumerate(layout):
        for j, c in enumerate(line):
            if c == "[":
                answer += 100 * i + j
    return answer


def part_two(layout, path, curr):
    pages = []
    pos = curr

    # for line in layout:
    #     for c in line:
    #         print(c, end="")
    #     print()

    for i, d in enumerate(path):
        if d == ">":
            check = legal(layout, pos, (0, 1), set())
            if check:
                pos[1] += 1
                if layout[pos[0]][pos[1]] in ("[", "]"):
                    layout = moveboxes(layout, pos, (0, 1))
                layout[pos[0]][pos[1]], layout[pos[0]][pos[1] - 1] = (
                    layout[pos[0]][pos[1] - 1],
                    layout[pos[0]][pos[1]],
                )
        elif d == "v":
            check = legal(layout, pos, (1, 0), set())
            if check:
                pos[0] += 1
                if layout[pos[0]][pos[1]] in ("[", "]"):
                    layout = moveboxes(layout, pos, (1, 0))
                else:
                    layout[pos[0]][pos[1]], layout[pos[0] - 1][pos[1]] = (
                        layout[pos[0] - 1][pos[1]],
                        layout[pos[0]][pos[1]],
                    )
        elif d == "<":
            check = legal(layout, pos, (0, -1), set())
            if check:
                pos[1] -= 1
                if layout[pos[0]][pos[1]] in ("[", "]"):
                    layout = moveboxes(layout, pos, (0, -1))
                layout[pos[0]][pos[1]], layout[pos[0]][pos[1] + 1] = (
                    layout[pos[0]][pos[1] + 1],
                    layout[pos[0]][pos[1]],
                )
        elif d == "^":
            check = legal(layout, pos, (-1, 0), set())
            if check:
                pos[0] -= 1
                if layout[pos[0]][pos[1]] in ("[", "]"):
                    layout = moveboxes(layout, pos, (-1, 0))
                else:
                    layout[pos[0]][pos[1]], layout[pos[0] + 1][pos[1]] = (
                        layout[pos[0] + 1][pos[1]],
                        layout[pos[0]][pos[1]],
                    )

    #     temp = ""
    #     for line in layout:
    #         for c in line:
    #             temp += c
    #         temp += "\n"
    #     pages.append(temp)
    #
    # curses.wrapper(print_map, pages, path)

    return get_score2(layout)


if __name__ == "__main__":
    lay, way, curr = read_file("./input.txt")
    # ans = part_one(lay, way, curr)
    # print("Score of Boxes", ans)
    answer = part_two(lay, way, curr)
    print("Score of Boxes Doubled", answer)
