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

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_


class Token:
    def __init__(self, token: TokenEnum, value: str | None = None) -> None:
        if not TokenEnum.has_value(token):
            raise TypeError("token must be a TokenEnum instance")

        self.token = token
        self.value = value

    def __str__(self) -> str:
        if self.token in (TokenEnum.VAR, TokenEnum.NUM):
            return self.value

        if self.token in (TokenEnum.U_ADD, TokenEnum.U_SUB):
            return self.token[0]

        return self.token

    def __repr__(self) -> str:
        if self.token in (TokenEnum.VAR, TokenEnum.NUM):
            return f"Token({self.token}, {self.value})"

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
                token = re.findall(r"^(<|>|==|!=|\+|\-|\*|\/|\(|\)|=|;|{|})", program[pos:])[0]
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
                return idx

        raise SyntaxError("Invalid parenthesis syntax: " + Lexer.detokenize(tokens))
