from lexer import Lexer, Token, TokenEnum


class Node:
    def __init__(
        self, name: TokenEnum, op1: str, op2: str | None = None, op3: str | None = None
    ) -> None:
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self) -> str:
        if self.op2 and self.op3:
            return f"Node('{self.name}', {self.op1}, {self.op2}, {self.op3})"
        elif self.op2:
            return f"Node('{self.name}', {self.op1}, {self.op2})"
        else:
            return f"Node('{self.name}', {self.op1})"


class Parser:
    def __init__(self) -> None:
        pass

    def parse_stmts(self, tokens: tuple[Token]) -> tuple:
        if tokens[-1] not in (TokenEnum.END_STMT, TokenEnum.RP_STMT):
            raise SyntaxError("Invalid stmts syntax: " + Lexer.detokenize(tokens))

        idx = 0
        stmts_idx = 0
        stmts = [[]]

        while idx < len(tokens):
            if tokens[idx] == TokenEnum.LP_STMT:
                lp_idx = idx
                idx += Lexer.rp_idx(tokens[idx:])
                rp_idx = idx

                if idx + 1 < len(tokens) and tokens[idx + 1] == TokenEnum.ELSE:
                    idx += 2
                    idx += Lexer.rp_idx(tokens[idx:])
                    rp_idx = idx

                stmts[stmts_idx].extend(tokens[lp_idx : rp_idx + 1])
                stmts_idx += 1
                stmts.append([])
            else:
                stmts[stmts_idx].append(tokens[idx])

            if tokens[idx] == TokenEnum.END_STMT:
                stmts_idx += 1
                stmts.append([])

            idx += 1

        del stmts[stmts_idx]
        return tuple(map(tuple, stmts))

    def parse_unary(self, tokens: tuple[Token]) -> Node:
        if not tokens:
            raise SyntaxError(
                "Invalid unary expression syntax: " + Lexer.detokenize(tokens)
            )

        if tokens[0] in (TokenEnum.U_ADD, TokenEnum.U_SUB):
            return Node(tokens[0].token, self.parse_expr(tokens[1:]))
        
        if tokens[0] in (TokenEnum.NUM, TokenEnum.VAR):
            return Node(tokens[0].token, tokens[0].name)

        raise SyntaxError(
            "Invalid unary expression syntax: " + Lexer.detokenize(tokens)
        )

    def parse_binary(self, tokens: tuple, ops: tuple[Token]) -> Node | None:
        if not tokens:
            raise SyntaxError(
                "Invalid binary expression syntax: " + Lexer.detokenize(tokens)
            )

        for idx, token in enumerate(tokens[::-1]):
            if token == TokenEnum.RP:
                idx = Lexer.lp_idx(tokens[:-idx])
                return self.parse_expr(tokens[1:idx])

        idx = 0
        while idx < len(tokens):
            if tokens[idx] == TokenEnum.LP:
                idx += Lexer.rp_idx(tokens[idx:])

            if tokens[idx] in ops:
                if idx == 0:
                    raise SyntaxError(
                        "Invalid binary expression syntax: " + Lexer.detokenize(tokens)
                    )
                return Node(
                    tokens[idx].token,
                    self.parse_expr(tokens[:idx]),
                    self.parse_expr(tokens[idx + 1 :]),
                )

            idx += 1

        return None

    def parse_expr(self, tokens: tuple[Token]) -> Node:
        if not tokens:
            raise SyntaxError("Invalid expression syntax: " + Lexer.detokenize(tokens))

        node = self.parse_binary(tokens, (TokenEnum.LT, TokenEnum.GT, TokenEnum.EQ, TokenEnum.NEQ))
        if node:
            return node

        node = self.parse_binary(tokens, (TokenEnum.ADD, TokenEnum.SUB))
        if node:
            return node

        node = self.parse_binary(tokens, (TokenEnum.MUL, TokenEnum.DIV))
        if node:
            return node

        if tokens[0] in (TokenEnum.U_ADD, TokenEnum.U_SUB):
            return self.parse_unary(tokens)

        if tokens[0] == TokenEnum.LP:
            idx = Lexer.rp_idx(tokens)
            return self.parse_expr(tokens[1:idx])

        node = self.parse_unary(tokens)
        if node:
            return node

        raise SyntaxError("Invalid expression syntax: " + Lexer.detokenize(tokens))


class OldParser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer

    def parse_term(self, term: tuple) -> Node:
        if len(term) != 2:
            raise SyntaxError("Invalid term")

        if term[0] == "id":
            return Node("ID", term[1])
        elif term[0] == "num":
            return Node("INT", term[1])

    def parse_unary(self, unary: tuple) -> Node:
        if len(unary) != 2:
            raise SyntaxError("Invalid unary expression")

        if unary[0] == "add":
            return Node("UNARY_ADD", self.parse_unary(unary[1]))

        if unary[0] == "sub":
            return Node("UNARY_SUB", self.parse_unary(unary[1]))

        return self.parse_term(unary)

    def parse_binary(self, binary: tuple) -> Node:
        if len(binary) == 2:
            return self.parse_unary(binary)

        if len(binary) < 3:
            raise SyntaxError("Invalid binary expression")

        if binary[0] == "add":
            return Node(
                "ADD", self.parse_binary(binary[1]), self.parse_binary(binary[2])
            )
        elif binary[0] == "sub":
            return Node(
                "SUB", self.parse_binary(binary[1]), self.parse_binary(binary[2])
            )

    def parse_expr(self, expr: tuple) -> Node:
        if len(expr) < 2:
            raise SyntaxError("Invalid expression")

        if len(expr) == 2:
            return self.parse_term(expr)

        if len(expr) != 3:
            raise SyntaxError("Invalid expression")

        op = expr[0]
        left_expr = expr[1]
        right_expr = expr[2]

        return Node(op, self.parse_expr(left_expr), self.parse_expr(right_expr))

    def parse_program(self, program: str) -> list:
        stmts = list(filter(None, program.split(";")))

        ast = []
        for i in range(len(stmts)):
            if not stmts[i]:
                continue

            tokens = self.lexer.lex_stmt(stmts[i])
            if tokens[0] == "assign":
                ast.append(
                    Node(
                        "ASSIGN",
                        tokens[1],
                        op2=self.parse_expr(self.lexer.lex_expr(tokens[2])),
                    )
                )
            elif tokens[0] == "if":
                parser = Parser(Lexer())
                ast.append(
                    Node(
                        "IF",
                        self.parse_expr(self.lexer.lex_expr(tokens[1])),
                        op2=parser.parse_program(tokens[2]),
                    )
                )
            elif tokens[0] == "ifelse":
                parser = Parser(Lexer())
                ast.append(
                    Node(
                        "IFELSE",
                        self.parse_expr(self.lexer.lex_expr(tokens[1])),
                        op2=parser.parse_program(tokens[2]),
                        op3=parser.parse_program(tokens[3]),
                    )
                )
            elif tokens[0] == "while":
                parser = Parser(Lexer())
                ast.append(
                    Node(
                        "WHILE",
                        self.parse_expr(self.lexer.lex_expr(tokens[1])),
                        op2=parser.parse_program(tokens[2]),
                    )
                )
            elif tokens[0] == "exit":
                ast.append(Node("EXIT", None))
            elif tokens[0] == "pass":
                ast.append(Node("PASS", None))

        return ast
