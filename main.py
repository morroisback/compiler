from lexer import Lexer
from parser import Parser
from compiler import Compiler


def test_lexer() -> None:
    # program = "a   = 3   + 2  ;"
    # program = "while1 = 5;"
    # program = "if (2 >  2) {a   = 3   + 2  ; }"
    # program = "if (2 >  2 ){a   = 3   + 2 ;}  else    { a   = 3;}"
    # program = "while   (a <   2)   {   if (2 >  2){   a   = 3   + 2  } else {   a   = 3 }}"
    # program = "a = 1;while   a <   2   :  if i2 >  2  : a   = 3   + 2   else  :   a   = 3; pass   ;"

    program = """
    a = 1;
    while1=-3;
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
    program1 = lexer.tokenize(program)
    expr1 = lexer.tokenize(expr)

    print(program1)
    print(expr1)

    # lexer = OldLexer()
    # program2 = lexer.lex_program(program)
    # stmts = lexer.lex_stmts(program)
    # print(program)
    # print(stmts)
    # for stmt in stmts: 
    #     print(lexer.lex_stmt(stmt))
        
    # while_stmt = lexer.lex_stmt(stmts[2])
    # inner_stmts = lexer.lex_stmts(while_stmt[2])
    # print(inner_stmts)
    # for stmt in inner_stmts: 
    #     print(lexer.lex_stmt(stmt))

    # expr = lexer.lex_program(expr)
    # expr = lexer.lex_expr(expr)
    # print(expr)
    # expr = lexer.lex_expr(expr[1])
    # print(expr)
    # expr = lexer.lex_expr(expr[1])
    # print(expr)
    # expr = lexer.lex_expr(expr[1])
    # print(expr)
    # expr = lexer.lex_expr(expr[1])
    # print(expr)


def test_parser() -> None:
    # program = "a   = 3   + 2  ;"
    # program = "while1 = 5;"
    # program = "if (2 >  2) {a   = 3   + 2  ; }"
    # program = "if (2 >  2 ){a   = 3   + 2 ;}  else    { a   = 3;}"
    # program = "while   (a <   2)   {   if (2 >  2){   a   = 3   + 2  } else {   a   = 3 }}"
    # program = "a = 1;while   a <   2   :  if i2 >  2  : a   = 3   + 2   else  :   a   = 3; pass   ;"

    program = """
    a = 1;
    while1=-3;
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
    program1 = lexer.tokenize(program)
    expr1 = lexer.tokenize(expr)
    
    parser = Parser()
    stmts1 = parser.parse_stmts(program1)
    expr2 = parser.parse_expr(expr1)
    
    print(stmts1)
    print(expr2)

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
