from functools import cache


def read_lines(filename):
    with open(filename, "r", encoding="utf-8") as file:
        file = file.read().strip()
        stripes = file.splitlines()[0].split(", ")
        patterns = stripes
        # stripes = {pattern: None for pattern in stripes}
        wanted = file.splitlines()[2:]
        # print(sorted(patterns), sorted(wanted))
        # return stripes, wanted
        return patterns, wanted


def possible(objective, patterns):
    # this is for backtracking and finding larger patterns if overlap exists in the patterns collection
    stack = [(0, len(objective))]
    l, r = 0, 0
    visited = set()  # without this it don't work
    count = 0

    while stack:
        l, r = stack.pop()
        while l < r:
            substr = objective[l:r]
            if substr in patterns:
                # if (l, r) not in visited:
                stack.append((l, r - 1))  # check smaller window
                #     visited.add((l, r))
                if r == len(objective) and objective[l:r] in patterns:
                    count += 1
                l = r
                r = len(objective)
            else:
                r -= 1

    return count


def twoi(s, w):
    maxlen = len(max(s, key=len))
    patterns = set(s)

    @cache
    def dfs(linen):
        if linen == "":
            return 1
        count = 0
        for i in range(1, min(maxlen, len(linen)) + 1):
            check = linen[:i]
            if linen[:i] in patterns:
                count += dfs(linen[i:])
        return count

    return sum(dfs(linen) for linen in w)


if __name__ == "__main__":
    s, w = read_lines("./input.txt")
    # s, w = read_lines("./test.txt")

    # ans = 0
    # count = 0
    # for i, towel in enumerate(w):
    #     print(i)
    #     TEMP = possible(towel, s)
    #     count += TEMP
    #     if TEMP:
    #         ans += 1
    # print(ans)
    # print(count)

    ans = twoi(s, w)
    print(ans)
