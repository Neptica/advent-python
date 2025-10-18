def read_file(filename):
    result = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            result.append(line.strip())
    return result


arrows = [["", "^", "A"], ["<", "v", ">"]]
keys = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["", "0", "A"]]


def dfs(pad, p, visited, button, score):
    if pad[p[0]][p[1]] == button:
        return ""

    if p in visited and visited[p] < score:
        return "XXXXXXXXXXX"

    visited[p] = score
    s = []
    if p[0] - 1 > -1 and pad[p[0] - 1][p[1]] != "":
        s.append("^" + dfs(pad, (p[0] - 1, p[1]), visited, button, score + 1))
    if p[1] + 1 < len(pad[0]) and pad[p[0]][p[1] + 1] != "":
        s.append(">" + dfs(pad, (p[0], p[1] + 1), visited, button, score + 1))
    if p[0] + 1 < len(pad) and pad[p[0] + 1][p[1]] != "":
        s.append("v" + dfs(pad, (p[0] + 1, p[1]), visited, button, score + 1))
    if p[1] - 1 > -1 and pad[p[0]][p[1] - 1] != "":
        s.append("<" + dfs(pad, (p[0], p[1] - 1), visited, button, score + 1))

    return min(s, key=len)


class KeypadController:
    def __init__(self):
        self.keypad = keys
        self.start = (3, 2)
        self.pos = self.start
        self.priority = {"^": 0, "<": 1, "v": 2, ">": 3}

    def find_button(self, button):
        current_pos = self.pos

        # update the current pos
        for i, line in enumerate(self.keypad):
            for j, c in enumerate(line):
                if c == button:
                    self.pos = (i, j)

        return (
            "".join(
                sorted(
                    dfs(self.keypad, current_pos, {}, button, 0),
                    key=lambda x: self.priority.get(x, 100),
                )
            )
            + "A"
        )


class ArrowController:
    def __init__(self):
        self.arrowpad = arrows
        self.start = (0, 2)
        self.pos = self.start
        self.priority = {">": 1, "v": 2, "<": 3, "^": 4}

    def find_button(self, button):
        current_pos = self.pos

        # update the current pos
        for i, line in enumerate(self.arrowpad):
            for j, c in enumerate(line):
                if c == button:
                    self.pos = (i, j)

        return (
            "".join(
                sorted(
                    dfs(self.arrowpad, current_pos, {}, button, 0),
                    key=lambda x: self.priority.get(x, 100),
                )
            )
            + "A"
        )


# NOTE: 379A is returning too large of a value, rest are correct
def part_one(codes):
    controllers = [
        KeypadController(),
        ArrowController(),
        ArrowController(),
    ]
    ans = 0
    for code in codes:
        current = code

        for controller in controllers:
            expanded_code = ""
            for button in current:
                expanded_code += controller.find_button(button)
            current = expanded_code
            controller.pos = controller.start  # for the next code

        print(current, len(current), code)
        score = len(current) * int(code[:-1])
        print(score)
        ans += score
    return ans


# v<<A>>^AvA^Av< <A>>^AAv<A<A>>^AAvAA< ^A>Av<A>^AA<A>Av<A <A> >^AAAvA<^A>A (Mine)
# <v<A>>^AvA^A<v A<AA>>^AAvA<^A>AAvA ^A<v A>^AA<A>A<v<A >A >^AAAvA<^A>A (Correct)
if __name__ == "__main__":
    l = read_file("./test.txt")

    clicks = part_one(l)
    print(clicks)
    print(
        "".join(
            sorted(
                "<<vv>>^^", key=lambda x: {">": 1, "v": 2, "<": 3, "^": 4}.get(x, 100)
            )
        )
    )
