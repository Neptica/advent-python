import math


def read_file(filename):
    registers = []
    program = []
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i < 3:
                registers.append(int(line.strip().split(" ")[2]))
            elif i == 4:
                prog = line.strip().split(" ")[1]
                program.extend([int(op) for op in prog.split(",")])
    return registers, program


def combo(num, registers):
    if num > 3:
        num = registers[num % 4]
    return num


def part_one(inp):
    # the number proceeding it in the program is the operand
    reg, program = inp
    ip = 0
    out = ""

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        match opcode:
            case 0:
                reg[0] //= 2 ** combo(operand, reg)
            case 1:
                reg[1] ^= operand
            case 2:
                reg[1] = combo(operand, reg) % 8
            case 3:
                if reg[0] != 0:
                    ip = operand
                    continue
            case 4:
                reg[1] ^= reg[2]
            case 5:
                out += str(combo(operand, reg) % 8) + ","
            case 6:
                reg[1] = reg[0] // (2 ** combo(operand, reg))
            case 7:
                reg[2] = reg[0] // (2 ** combo(operand, reg))
            case _:
                print("ERROR: OPCODE DOES NOT EXIST")
        ip += 2

    return out


def find(program, a):
    if not program:
        return a

    for n in range(1, 8):
        a = a << 3
        a += n
        b = a % 8
        b = b ^ 3
        c = a >> b
        a = a >> 3
        b = b ^ c
        b = b ^ 5
        if b % 8 == program[-1]:
            ans = find(program[:-1], (a << 3) + n)
            if ans:
                return ans


if __name__ == "__main__":
    data = read_file("./input.txt")
    # ANS = part_one(data)
    # print("".join(ANS.split(",")))
    ans = find(data[1], 0)
    print(ans)
    # datatwo = [[236581108670061, 0, 0], data[1]]
    # twoi = part_one(datatwo)
    # print(twoi)
