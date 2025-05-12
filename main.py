from lexer import Lexer
from parser import Parser
from compiler import Compiler


def test_lexer() -> None:
    program = """
    a   = 3   + 2  ;
    while1=-3;
    if (2 >  2) {a   = 3   + 2  ; }
    if (2 >  2 ){a   = 3   + 2 ;}  else    { a   = 3;}

    while(while1 <   2 )  {
        if (a >  2  ){
            a = 5;
            while1=3   + -a   ;
        }
        else     {
            while1   = 3;
        }

        if ( while1 == 3) {
            while ( a == 1) {
                a = a - 1;
            }
            while1 = -2;
        }else{
            pass;
        }
    }
    pass   ;
    exit;
    """

    expr = "-a  * - 2 - 2 > 2 / ( 5 + (56 - 2 )* 2) == 2  - - - + -(-2 - 4)*4"

    lexer = Lexer()
    program_tokens = lexer.tokenize(program)
    expr_tokens = lexer.tokenize(expr)

    print(program_tokens)
    print(expr_tokens)

    print(lexer.detokenize(program_tokens))
    print(lexer.detokenize(expr_tokens))


def test_parser() -> None:
    program = """
    a   = 3   + 2  ;
    while1=-3;
    if (2 >  2) {a   = 3   + 2  ; }
    if (2 >  2 ){a   = 3   + 2 ;}  else    { a   = 3;}

    while(while1 <   2 )  {
        if (a >  2  ){
            a = 5;
            while1=3   + -a   ;
        }
        else     {
            while1   = 3;
        }

        if ( while1 == 3) {
            while ( a == 1) {
                a = a - 1;
            }
            while1 = -2;
        }else{
            pass;
        }
    }
    pass   ;
    exit;
    """

    expr = "-a  * - 2 - 2 > 2 / ( 5 + (56 - 2 )* 2) == 2  - - - + -(-2 - 4)*4"
    lexer = Lexer()
    program_tokens = lexer.tokenize(program)
    expr_tokens = lexer.tokenize(expr)

    print(lexer.detokenize(program_tokens))
    print(lexer.detokenize(expr_tokens))

    parser = Parser()
    stmts = parser.parse_stmts(program_tokens)
    expr_tree = parser.parse_expr(expr_tokens)

    for stmt in stmts:
        stmt_tree = parser.parse_stmt(stmt)
        print(stmt_tree)

    print(stmts)
    print(expr_tree)

    # lexer = Lexer()
    # parser = Parser(lexer)

    # print(parser.parse_term(lexer.lex_term("a")))
    # print(parser.parse_expr(lexer.lex_expr("2")))
    # print(parser.parse_expr(lexer.lex_expr("2  +    a  ")))
    # print(parser.parse_binary(lexer.lex_expr("2  +  - - - + a  ")))

    # print(program)
    # print(parser.parse_program(program))


def test_compiler() -> None:
    program = "a = 1;while   a <   2   :  if i2 >  2  : a   = 3   + 2   else  :   a   = 3; pass   ;"
    # program = "while   a <   2   :   if 2 >  2  : a   = 3   + 2   else  :   a   = 3"
    # program = "if 2 >  2: a   = 3   + 2   else  :   a   = 3"
    # program = "if 2 >  2: a   = 3   + 2  "
    # program = "a   = 3   + 2  "

    lex = Lexer()
    parser = Parser(lex)
    compiler = Compiler()

    ast = parser.parse_program(program)
    print(ast)
    print(list(enumerate(compiler.compile_program(ast))))


def main() -> None:
    # test_lexer()
    test_parser()
    # test_compiler()


if __name__ == "__main__":
    main()
