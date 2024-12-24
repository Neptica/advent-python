def read_file(filename):
    results = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            results.append(line.strip())

    return results


def part_one(links):
    connections = {}
    for link in links:
        c1, c2 = link[:2], link[3:]
        if c1 not in connections:
            connections[c1] = {c2}
        else:
            connections[c1].add(c2)
        if c2 not in connections:
            connections[c2] = {c1}
        else:
            connections[c2].add(c1)

    # see if they have any overlapping connections?
    # a single key can be present in multiple interconnected networks
    networks = set()
    for key, group in connections.items():
        for c1 in group:
            for c2 in group:
                if c1 == c2:
                    continue
                if c1 in connections[c2]:
                    m = [key, c1, c2]
                    m.sort()
                    networks.add(tuple(m))

    ans = 0
    for net in networks:
        for computer in net:
            if computer.find("t") == 0:
                ans += 1
                # print(net)
                break
    print(len(networks))
    print(ans)


def part_two(links):
    connections = {}
    for link in links:
        c1, c2 = link[:2], link[3:]
        if c1 not in connections:
            connections[c1] = {c2}
        else:
            connections[c1].add(c2)

        if c2 not in connections:
            connections[c2] = {c1}
        else:
            connections[c2].add(c1)

    def bron_kerbosch(r, p, x):
        if not p and not x:
            return r
        largest = {}
        for v in list(p):
            possible = bron_kerbosch(
                r | {v}, p & connections[v], x & connections[v]
            )  # & is intersection | is union
            largest = max(largest, possible, key=len)
            p -= {v}
            x |= {v}
        return largest

    largest_clique = ""
    for key, neighbors in connections.items():
        clique = bron_kerbosch(set(), neighbors | {key}, set())
        largest_clique = max(largest_clique, clique, key=len)
    largest = list(largest_clique)
    largest.sort()
    print(",".join(largest), len(largest_clique))


if __name__ == "__main__":
    data = read_file("./input.txt")
    part_one(data)
    part_two(data)
