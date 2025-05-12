from lexer import Lexer, Token, TokenEnum


class Node:
    def __init__(
        self, token: TokenEnum, op1: str, op2: str | None = None, op3: str | None = None
    ) -> None:
        self.token = token
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self) -> str:
        if self.op2 and self.op3:
            return f"Node('{self.token}', {self.op1}, {self.op2}, {self.op3})"
        elif self.op2:
            return f"Node('{self.token}', {self.op1}, {self.op2})"
        else:
            return f"Node('{self.token}', {self.op1})"


class Parser:
    def parse_unary(self, tokens: tuple[Token]) -> Node:
        if not tokens:
            raise SyntaxError(
                "Invalid unary expression syntax: " + Lexer.detokenize(tokens)
            )

        if tokens[0] in (TokenEnum.U_ADD, TokenEnum.U_SUB):
            return Node(tokens[0].token, self.parse_expr(tokens[1:]))

        if tokens[0] in (TokenEnum.NUM, TokenEnum.VAR):
            return Node(tokens[0].token, tokens[0].value)

        raise SyntaxError(
            "Invalid unary expression syntax: " + Lexer.detokenize(tokens)
        )

    def parse_binary(self, tokens: tuple[Token], ops: tuple[TokenEnum]) -> Node | None:
        if len(tokens) < 3:
            return None

        idx = len(tokens) - 1
        while idx >= 0:
            if tokens[idx] == TokenEnum.RP:
                idx -= Lexer.lp_idx(tokens[: idx + 1])

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

            idx -= 1

        return None

    def parse_expr(self, tokens: tuple[Token]) -> Node:
        if not tokens:
            raise SyntaxError("Invalid expression syntax: " + Lexer.detokenize(tokens))

        if node := self.parse_binary(
            tokens, (TokenEnum.LT, TokenEnum.GT, TokenEnum.EQ, TokenEnum.NEQ)
        ):
            return node
        elif node := self.parse_binary(tokens, (TokenEnum.ADD, TokenEnum.SUB)):
            return node
        elif node := self.parse_binary(tokens, (TokenEnum.MUL, TokenEnum.DIV)):
            return node

        if tokens[0] in (TokenEnum.U_ADD, TokenEnum.U_SUB):
            return self.parse_unary(tokens)

        if tokens[0] == TokenEnum.LP:
            idx = Lexer.rp_idx(tokens)
            return self.parse_expr(tokens[1:idx])

        return self.parse_unary(tokens)

    def parse_stmt(self, tokens: tuple[Token]) -> Node:
        if len(tokens) < 2:
            raise SyntaxError("Invalid stmt syntax: " + Lexer.detokenize(tokens))

        if (
            tokens[0] in (TokenEnum.PASS, TokenEnum.EXIT)
            and tokens[1] == TokenEnum.END_STMT
        ):
            return Node(tokens[0].token, None)

        if len(tokens) < 3:
            raise SyntaxError("Invalid stmt syntax: " + Lexer.detokenize(tokens))

        if (
            tokens[1] == TokenEnum.ASSIGN
            and tokens[0] == TokenEnum.VAR
            and tokens[-1] == TokenEnum.END_STMT
        ):
            return Node(
                tokens[1].token,
                Node(tokens[0].token, tokens[0].value),
                self.parse_expr(tokens[2:-1]),
            )
        elif (
            tokens[0] == TokenEnum.WHILE
            and tokens[1] == TokenEnum.LP
            and tokens[-1] == TokenEnum.RP_STMT
        ):
            expr_open_idx = 1
            expr_close_idx = expr_open_idx + Lexer.rp_idx(tokens[expr_open_idx:])
            expr_tree = self.parse_expr(tokens[expr_open_idx + 1 : expr_close_idx])

            stmts_open_idx = tokens.index(TokenEnum.LP_STMT, expr_close_idx)
            stmts_close_idx = stmts_open_idx + Lexer.rp_idx(tokens[stmts_open_idx:])
            stmts = self.parse_stmts(tokens[stmts_open_idx + 1 : stmts_close_idx])
            stmts_tree = []
            for stmt in stmts:
                stmts_tree.append(self.parse_stmt(stmt))

            if len(stmts_tree) != len(stmts):
                raise SyntaxError("Invalid stmts syntax: " + Lexer.detokenize(stmt))

            return Node(tokens[0].token, expr_tree, tuple(stmts_tree))
        elif (
            tokens[0] == TokenEnum.IF
            and tokens[1] == TokenEnum.LP
            and tokens[-1] == TokenEnum.RP_STMT
        ):
            expr_open_idx = 1
            expr_close_idx = expr_open_idx + Lexer.rp_idx(tokens[expr_open_idx:])
            expr_tree = self.parse_expr(tokens[expr_open_idx + 1 : expr_close_idx])

            if_stmts_open_idx = tokens.index(TokenEnum.LP_STMT, expr_close_idx)
            if_stmts_close_idx = if_stmts_open_idx + Lexer.rp_idx(
                tokens[if_stmts_open_idx:]
            )
            if_stmts = self.parse_stmts(
                tokens[if_stmts_open_idx + 1 : if_stmts_close_idx]
            )
            if_stmts_tree = []
            for stmt in if_stmts:
                if_stmts_tree.append(self.parse_stmt(stmt))

            if len(if_stmts_tree) != len(stmts):
                raise SyntaxError("Invalid stmts syntax: " + Lexer.detokenize(stmt))

            if (
                len(tokens) == if_stmts_close_idx
                or tokens[if_stmts_close_idx + 1] != TokenEnum.ELSE
            ):
                return Node(tokens[0].token, expr_tree, tuple(if_stmts_tree))

            # return Node(tokens[0].token, expr_tree, tuple(if_stmts_tree))

        raise SyntaxError("Invalid stmt syntax: " + Lexer.detokenize(tokens))

    def parse_stmts(self, tokens: tuple[Token]) -> tuple[tuple[Token]]:
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
