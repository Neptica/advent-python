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
        print(reg)
        opcode = program[ip]
        operand = program[ip + 1]

        match opcode:
            case 0:
                reg[0] //= (2**combo(operand, reg))
            case 1:
                reg[1] ^= operand
            case 2:
                reg[1] = combo(operand, reg) % 8
            case 3:
                if reg[0] != 0:
                    ip = operand
                    print("Jump")
                    continue
            case 4:
                reg[1] ^= reg[2]
            case 5:
                out += str(combo(operand, reg) % 8) + ","
            case 6:
                reg[1] = reg[0] // (2**combo(operand, reg))
            case 7:
                reg[2] = reg[0] // (2**combo(operand, reg))
            case _:
                print("ERROR: OPCODE DOES NOT EXIST")
        ip += 2

    return out


if __name__ == "__main__":
    data = read_file("./input.txt")
    ANS = part_one(data)
    print("".join(ANS.split(",")))
    # print(data)
    # data[0][0] = 27 
    # ANS = part_one(data)
    # print(ANS[:-1])
