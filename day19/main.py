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


@cache
class Trie:
    def __init__(self):
        self.data = {}
        self.blank_char = "BLANK"
        self.nodes = 0
        self.data[self.blank_char] = False

    def addWord(self, word):
        prev = self.data
        for letter in word:
            if letter not in prev:
                prev[letter] = {self.blank_char: False}
                self.nodes += 1
            prev = prev[letter]
        prev[self.blank_char] = True

    @cache
    def pieceWise(self, linen):
        count = 0

        @cache
        def helper(linen, trie, previous_terminates):
            nonlocal count
            if len(linen) == 0:
                if previous_terminates:
                    count += 1
                return

            i = 0
            while i < len(linen) and linen[i] in trie:
                trie = trie[linen[i]]
                pattern = linen[: i + 1]
                if trie[self.blank_char]:
                    helper(linen[i + 1 :], self.data, trie[self.blank_char])
                i += 1

        helper(linen, self.data, False)
        return count


def twoi(s, w):
    trie = Trie()
    count = 0
    for pattern in s:
        count += len(pattern)
        trie.addWord(pattern)
    print(count, trie.nodes)

    ans = 0
    # print(trie.pieceWise(w[3]))
    for i, linen in enumerate(w):
        print(i)
        ans += trie.pieceWise(linen)

    return ans


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
