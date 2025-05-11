from compiler import Command


class VirtualMachine:
    def __init__(self) -> None:
        pass

    def run(self, program):
        env = {}
        stack = []
        pc = 0
        while True:
            op = program[pc]
            if pc < len(program) - 1:
                arg = program[pc + 1]

            if op == Command.FETCH:
                if arg in env:
                    stack.append(env[arg])
                else:
                    stack.append(0)
                pc += 2
