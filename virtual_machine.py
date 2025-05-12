from compiler import Command


class VirtualMachine:
    def run(self, program: tuple[Command | int | str]) -> None:
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
            elif op == Command.STORE:
                env[arg] = stack.pop()
                pc += 2
            elif op == Command.PUSH:
                stack.append(arg)
                pc += 2
            elif op == Command.ADD:
                stack.append(stack.pop() + stack.pop())
                pc += 1
            elif op == Command.SUB:
                stack.append(-stack.pop() + stack.pop())
                pc += 1
            elif op == Command.MUL:
                stack.append(stack.pop() * stack.pop())
                pc += 1
            elif op == Command.DIV:
                stack.append(1 / stack.pop() * stack.pop())
                pc += 1
            elif op == Command.LT:
                stack.append(int(stack.pop() > stack.pop()))
                pc += 1
            elif op == Command.GT:
                stack.append(int(stack.pop() < stack.pop()))
                pc += 1
            elif op == Command.EQ:
                stack.append(int(stack.pop() == stack.pop()))
                pc += 1
            elif op == Command.NEQ:
                stack.append(int(stack.pop() != stack.pop()))
                pc += 1
            elif op == Command.JZ:
                if stack.pop() == 0:
                    pc = arg
                else:
                    pc += 2
            elif op == Command.JMP:
                pc = arg
            elif op == Command.PASS:
                pc += 1
            elif op == Command.HALT:
                break

        print("Program finished.")
        length = len(max(env.keys()))
        for i in env:
            print(f"{i:>{length}}:\t{env[i]}")
