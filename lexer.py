import re

from enum import Enum


class TokenEnum(str, Enum):
    END_STMT = ";"
    LP_STMT = "{"
    RP_STMT = "}"
    WHILE = "while"
    IF = "if"
    ELSE = "else"
    PASS = "pass"
    EXIT = "exit"
    VAR = "var"
    NUM = "num"
    LP = "("
    RP = ")"
    U_ADD = "+u"
    U_SUB = "-u"
    MUL = "*"
    DIV = "/"
    ADD = "+"
    SUB = "-"
    LT = "<"
    GT = ">"
    EQ = "=="
    NEQ = "!="
    ASSIGN = "="


class Token:
    def __init__(self, token: TokenEnum, name: str | None = None) -> None:
        self.token = token
        self.name = name

    def __str__(self) -> str:
        if self.token in (TokenEnum.VAR, TokenEnum.NUM):
            return self.name

        if self.token in (TokenEnum.U_ADD, TokenEnum.U_SUB):
            return self.token[0]

        return self.token

    def __repr__(self) -> str:
        return f"Token({str(self)})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Token):
            return self.token == other.token
        elif isinstance(other, TokenEnum):
            return self.token == other
        
        return False


class Lexer:
    @staticmethod
    def tokenize(program: str) -> tuple:
        pos = 0
        tokens = []

        while pos < len(program):
            if program[pos] in " \t\n":
                pos += 1
            elif re.search(r"^(while|if)[ \t\n]*\(", program[pos:]):
                token = re.findall(r"^(while|if)[ \t\n]*\(", program[pos:])[0]
                pos += len(token)
                tokens.append(Token(token))
            elif re.search(r"^(else)[ \t\n]*{", program[pos:]):
                token = re.findall(r"^(else)[ \t\n]*{", program[pos:])[0]
                pos += len(token)
                tokens.append(Token(token))
            elif re.search(r"^(pass|exit)[ \t\n]*;", program[pos:]):
                token = re.findall(r"^(pass|exit)[ \t\n]*;", program[pos:])[0]
                pos += len(token)
                tokens.append(Token(token))
            elif re.search(r"^[a-zA-Z][a-zA-Z0-9_]*", program[pos:]):
                token = re.findall(r"^[a-zA-Z][a-zA-Z0-9_]*", program[pos:])[0]
                pos += len(token)
                tokens.append(Token("var", token))
            elif re.search(r"^[0-9]+", program[pos:]):
                token = re.findall(r"^[0-9]+", program[pos:])[0]
                pos += len(token)
                tokens.append(Token("num", token))
            elif re.search(r"^(<|>|==|!=|\+|\-|\*|\/|\(|\)|=|;|{|})", program[pos:]):
                token = re.findall(
                    r"^(<|>|==|!=|\+|\-|\*|\/|\(|\)|=|;|{|})", program[pos:]
                )[0]
                pos += len(token)

                if token in "+-":
                    if len(tokens) == 0 or tokens[-1] not in (
                        TokenEnum.VAR,
                        TokenEnum.NUM,
                    ):
                        token += "u"

                tokens.append(Token(token))
            else:
                raise SyntaxError("Invalid program syntax: " + program)

        return tuple(tokens)

    @staticmethod
    def detokenize(tokens: tuple) -> str:
        return " ".join(map(lambda token: str(token), tokens))

    @staticmethod
    def rp_idx(tokens: tuple) -> int:
        if tokens[0] not in (TokenEnum.LP, TokenEnum.LP_STMT):
            raise SyntaxError("Invalid parenthesis syntax: " + Lexer.detokenize(tokens))

        level = 0
        lp = tokens[0]
        if tokens[0] == TokenEnum.LP:
            rp = TokenEnum.RP
        elif tokens[0] == TokenEnum.LP_STMT:
            rp = TokenEnum.RP_STMT

        for idx, token in enumerate(tokens):
            if token == lp:
                level += 1
            elif token == rp:
                level -= 1

            if level == 0:
                return idx

        raise SyntaxError("Invalid parenthesis syntax: " + Lexer.detokenize(tokens))

    @staticmethod
    def lp_idx(tokens: tuple) -> int:
        if tokens[-1] not in (TokenEnum.RP, TokenEnum.RP_STMT):
            raise SyntaxError("Invalid parenthesis syntax: " + Lexer.detokenize(tokens))

        level = 0
        rp = tokens[-1]
        if tokens[-1] == TokenEnum.RP:
            lp = TokenEnum.LP
        elif tokens[-1] == TokenEnum.RP_STMT:
            lp = TokenEnum.LP_STMT

        for idx, token in enumerate(tokens[::-1]):
            if token == rp:
                level += 1
            elif token == lp:
                level -= 1

            if level == 0:
                return -idx - 1

        raise SyntaxError("Invalid parenthesis syntax: " + Lexer.detokenize(tokens))


class OldLexer:
    def __init__(self) -> None:
        pass

    def lex_term(self, term: tuple) -> tuple:
        if len(term) != 1:
            raise SyntaxError("Invalid term syntax: " + str(term))

        if re.match(r"[a-zA-Z][a-zA-Z0-9_]*", term[0]):
            return ("id", term[0])
        elif re.match(r"[0-9]+", term[0]):
            return ("num", term[0])

        raise SyntaxError("Invalid term syntax: " + str(term))

    def lex_unary(self, tokens: tuple, op: str) -> tuple:
        if op not in tokens:
            raise SyntaxError("Invalid unary syntax: " + " ".join(tokens))

        sub_expr = tokens[tokens.index(op) + 1 :]
        return (op, sub_expr)

    def lex_binary(self, tokens: tuple, op: str) -> tuple:
        pattern = re.compile(rf"([a-zA-Z0-9_]+ )(\{op})")
        tokens = pattern.sub(r"\1:", " ".join(tokens)).split(" ")
        if ":" not in tokens:
            raise SyntaxError("Invalid binary syntax: " + " ".join(tokens))

        left_expr = tuple(tokens[: tokens.index(":")])
        right_expr = tuple(tokens[tokens.index(":") + 1 :])
        return (op, left_expr, right_expr)

    def pos_brackets(self, tokens: tuple, close_bracket: str) -> int:
        open_bracket = tokens[0]
        level = 0
        for pos, token in enumerate(tokens):
            if token == open_bracket:
                level += 1
            elif token == close_bracket:
                level -= 1

            if level == 0:
                return pos

        raise SyntaxError("Invalid bracket syntax: " + " ".join(tokens))

    def lex_expr(self, tokens: tuple) -> tuple:
        if len(tokens) < 1:
            raise SyntaxError("Invalid expr syntax: " + " ".join(tokens))

        if len(tokens) == 1:
            return self.lex_term(tokens[0])

        while True:
            if "(" in tokens:
                open_bracket = tokens.index("(")
                close_bracket = open_bracket + self.pos_brackets(
                    tokens[open_bracket:], ")"
                )

                bracket_expr = [
                    ("brackets", tuple(tokens[open_bracket + 1 : close_bracket]))
                ]
                tokens = (
                    tokens[:open_bracket]
                    + tuple(bracket_expr)
                    + tokens[close_bracket + 1 :]
                )
            else:
                break

        tokens_str = " ".join(map(lambda e: e if isinstance(e, str) else e[0], tokens))

        if re.search(r"[a-zA-Z0-9_]+ (<|>|==|!=)", tokens_str):
            token = re.findall(r"[a-zA-Z0-9_]+ (<|>|==|!=)", tokens_str)[0]
            return self.lex_binary(tokens, token)
        elif re.search(r"[a-zA-Z0-9_]+ (\+|\-)", tokens_str):
            token = re.findall(r"[a-zA-Z0-9_]+ (\+|\-)", tokens_str)[0]
            return self.lex_binary(tokens, token)
        elif re.search(r"[a-zA-Z0-9_]+ (\*|\/).*", tokens_str):
            token = re.findall(r"[a-zA-Z0-9_]+ (\*|\/)", tokens_str)[0]
            return self.lex_binary(tokens, token)
        elif re.search(r"(\+|\-)", tokens_str):
            token = re.findall(r"(\+|\-)", tokens_str)[0]
            return self.lex_unary(tokens, token)

        raise SyntaxError("Invalid binary syntax: " + " ".join(tokens))

    def lex_stmt(self, tokens: tuple) -> tuple:
        if tokens[0] == "pass" and tokens[1] == ";":
            return ("pass", None)
        elif tokens[0] == "exit" and tokens[1] == ";":
            return ("exit", None)

        if len(tokens) < 3:
            raise SyntaxError("Invalid stmt syntax: " + " ".join(tokens))

        if tokens[1] == "=" and tokens[-1] == ";":
            name = tokens[:1]
            value = tokens[2:-1]
            return ("assign", name, value)
        elif tokens[0] == "while" and tokens[1] == "(" and tokens[-1] == "}":
            cond_open = 1
            cond_close = cond_open + self.pos_brackets(tokens[cond_open:], ")")
            cond = tokens[cond_open + 1 : cond_close]

            while_open = tokens.index("{")
            while_close = while_open + self.pos_brackets(tokens[while_open:], "}")
            while_stmt = tokens[while_open + 1 : while_close]

            return ("while", cond, while_stmt)
        elif tokens[0] == "if" and tokens[1] == "(" and tokens[-1] == "}":
            cond_open = 1
            cond_close = cond_open + self.pos_brackets(tokens[cond_open:], ")")
            cond = tokens[cond_open + 1 : cond_close]

            if_open = tokens.index("{")
            if_close = if_open + self.pos_brackets(tokens[if_open:], "}")
            if_stmt = tokens[if_open + 1 : if_close]

            tokens = tokens[if_close + 1 :]
            if "else" in tokens and tokens[1] == "{" and tokens[-1] == "}":
                else_open = tokens.index("{")
                else_close = else_open + self.pos_brackets(tokens[else_open:], "}")
                else_stmt = tokens[else_open + 1 : else_close]

                return ("ifelse", cond, if_stmt, else_stmt)

            return ("if", cond, if_stmt)

        raise SyntaxError("Invalid stmt syntax: " + " ".join(tokens))

    def lex_stmts(self, tokens: tuple) -> tuple:
        if tokens[-1] not in ";}":
            raise SyntaxError("Invalid stmts syntax: " + " ".join(tokens))

        pos = 0
        stmts_pos = 0
        stmts = [[]]

        while pos < len(tokens):
            if tokens[pos] == "{":
                open_pos = pos
                pos += self.pos_brackets(tokens[pos:], "}")
                if pos + 1 < len(tokens) and tokens[pos + 1] == "else":
                    pos += 2
                    pos += self.pos_brackets(tokens[pos:], "}")

                stmts[stmts_pos].extend(tokens[open_pos : pos + 1])
                stmts_pos += 1
                stmts.append([])
            else:
                stmts[stmts_pos].append(tokens[pos])

            if tokens[pos] == ";":
                stmts_pos += 1
                stmts.append([])

            pos += 1

        del stmts[stmts_pos]
        return tuple([tuple(stmt) for stmt in stmts])

    def lex_program(self, program: str) -> tuple:
        keywords = "|".join({"while", "if", "else", "pass", "exit"})

        pos = 0
        tokens = []

        while pos < len(program):
            if program[pos] in " \t\n":
                pos += 1
            elif re.search(rf"^({keywords})[ \t\n]*\(", program[pos:]):
                token = re.findall(rf"^({keywords})[ \t\n]*\(", program[pos:])[0]
                tokens.append(token)
                pos += len(token)
            elif re.search(r"^[a-zA-Z][a-zA-Z0-9_]*", program[pos:]):
                token = re.findall(r"^[a-zA-Z][a-zA-Z0-9_]*", program[pos:])[0]
                tokens.append(token)
                pos += len(token)
            elif re.search(r"^[0-9]+", program[pos:]):
                token = re.findall(r"^[0-9]+", program[pos:])[0]
                tokens.append(token)
                pos += len(token)
            elif re.search(r"^(<|>|==|!=|\+|\-|\*|\/|\(|\)|=|;|{|})", program[pos:]):
                token = re.findall(
                    r"^(<|>|==|!=|\+|\-|\*|\/|\(|\)|=|;|{|})", program[pos:]
                )[0]
                tokens.append(token)
                pos += len(token)
            else:
                raise SyntaxError("Invalid program syntax: " + program)

        return tuple(tokens)
