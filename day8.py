import sys
import doctest

class Program:
    def __init__(self, instrs):
        self.instrs = instrs
        self.acc = 0
        self.pc = 0

    def copy(self):
        return self.__class__(self.instrs.copy())

    @classmethod
    def parse(cls, text):
        instrs = [parse_line(line.strip()) for line in text]
        return cls(instrs)

    def step(self):
        opcode, arg = self.instrs[self.pc]
        if opcode == "nop":
            self.pc += 1
        elif opcode == "acc":
            self.acc += arg
            self.pc += 1
        elif opcode == "jmp":
            self.pc += arg

    def terminate_or_find_loop(self):
        seen = set()
        while self.pc not in seen:
            seen.add(self.pc)
            self.step()
            if self.pc >= len(self.instrs):
                return True
        return False

def parse_line(line):
    """
    >>> parse_line('acc -99')
    ('acc', -99)
    """
    instr, arg = line.split()
    return (instr, int(arg))

doctest.testmod()

program = Program.parse(sys.stdin)

# Part 1
terminated = program.terminate_or_find_loop()
print(f"{program.acc = }, {terminated = }")

# Part 2
result = None
for i, (opcode, arg) in enumerate(program.instrs):
    if opcode == "acc":
        continue
    new_prog = program.copy()
    if opcode == "jmp":
        new_prog.instrs[i] = ("nop", arg)
    else:
        new_prog.instrs[i] = ("jmp", arg)
    terminated = new_prog.terminate_or_find_loop()
    if terminated:
        result = new_prog.acc
        break
print(result)
