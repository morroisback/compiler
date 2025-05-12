from enum import Enum

from parser import Node


class Command(Enum):
    FETCH = 0
    STORE = 1
    PUSH = 2
    POP = 3
    ADD = 4
    SUB = 5
    MUL = 6
    DIV = 7
    LT = 8
    GT = 9
    EQ = 10
    NEQ = 11
    JZ = 12
    JNZ = 13
    JMP = 14
    PASS = 15
    HALT = 16


class Compiler:
    def __init__(self) -> None:
        self.program = []
        self.pc = 0

    def compile_command(self, command: Command | int | str) -> None:
        self.program.append(command)
        self.pc += 1

    def compile_node(self, node: Node) -> None:
        name = node.token
        if name == "INT":
            self.compile_command(Command.PUSH)
            self.compile_command(int(node.op1))
        elif name == "ID":
            self.compile_command(Command.FETCH)
            self.compile_command(node.op1)
        elif name == "+":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.ADD)
        elif name == "-":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.SUB)
        elif name == "*":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.MUL)
        elif name == "/":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.DIV)
        elif name == "<":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.LT)
        elif name == ">":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.GT)
        elif name == "==":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.EQ)
        elif name == "!=":
            self.compile_node(node.op1)
            self.compile_node(node.op2)
            self.compile_command(Command.NEQ)
        elif name == "ASSIGN":
            self.compile_node(node.op2)
            self.compile_command(Command.STORE)
            self.compile_command(node.op1)
        elif name == "IF":
            self.compile_node(node.op1)
            self.compile_command(Command.JZ)
            addr_end = self.pc
            self.compile_command(Command.PASS)
            self.compile_stmt(node.op2)
            self.program[addr_end] = self.pc
        elif name == "IFELSE":
            self.compile_node(node.op1)
            self.compile_command(Command.JZ)
            addr_else = self.pc
            self.compile_command(Command.PASS)
            self.compile_stmt(node.op2)
            self.compile_command(Command.JMP)
            addr_end = self.pc
            self.compile_command(Command.PASS)
            self.program[addr_else] = self.pc
            self.compile_stmt(node.op3)
            self.program[addr_end] = self.pc
        elif name == "WHILE":
            addr_while = self.pc
            self.compile_node(node.op1)
            self.compile_command(Command.JZ)
            addr_end = self.pc
            self.compile_command(Command.PASS)
            self.compile_stmt(node.op2)
            self.compile_command(Command.JMP)
            self.compile_command(addr_while)
            self.program[addr_end] = self.pc
        elif name == "EXIT":
            self.compile_command(Command.HALT)
        elif name == "PASS":
            self.compile_command(Command.PASS)

    def compile_stmt(self, ast: list) -> None:
        for stmt in ast:
            self.compile_node(stmt)

    def compile_program(self, ast: list) -> list:
        self.compile_stmt(ast)

        self.compile_command(Command.HALT)
        return self.program
