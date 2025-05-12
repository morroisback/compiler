from lexer import Lexer
from parser import Parser
from compiler import Compiler
from virtual_machine import VirtualMachine


def test_program() -> tuple[str]:
    program = """
    a   = 3   + 2  ;
    while1=-3;
    if (2 >  2) {a   = 3   + 2  ; }
    if (2 >  2 ){a   = 3   + 2 ;}  else    { a   = 3;}

    while(while1 <   2 )  {
        if (a >  2  ){
            a = 5;
            while1=3   + a   ;
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

    return program, expr


def test_lexer() -> None:
    program, expr = test_program()

    lexer = Lexer()
    program_tokens = lexer.tokenize(program)
    expr_tokens = lexer.tokenize(expr)

    print(program_tokens)
    print(expr_tokens)

    print(lexer.detokenize(program_tokens))
    print(lexer.detokenize(expr_tokens))


def test_parser() -> None:
    program, expr = test_program()

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
        print(lexer.detokenize(stmt))
        print(stmt_tree)

    print(stmts)
    print(expr_tree)


def test_compiler() -> None:
    program, expr = test_program()

    lexer = Lexer()
    program_tokens = lexer.tokenize(program)
    expr_tokens = lexer.tokenize(expr)

    print(lexer.detokenize(program_tokens))
    print(lexer.detokenize(expr_tokens))

    parser = Parser()
    program_tree = parser.parse_program(program_tokens)
    expr_tree = parser.parse_expr(expr_tokens)

    print(program_tree)
    print(expr_tree)

    compiler = Compiler()
    program_code = compiler.compile_program(program_tree)
    for line, code in enumerate(program_code):
        print(f"{line:03d}: {code}")


def test_virtual_machine() -> None:
    program, expr = test_program()

    lexer = Lexer()
    program_tokens = lexer.tokenize(program)
    expr_tokens = lexer.tokenize(expr)

    print(lexer.detokenize(program_tokens))
    print(lexer.detokenize(expr_tokens))

    parser = Parser()
    program_tree = parser.parse_program(program_tokens)
    expr_tree = parser.parse_expr(expr_tokens)

    print(program_tree)
    print(expr_tree)

    compiler = Compiler()
    program_code = compiler.compile_program(program_tree)
    for line, code in enumerate(program_code):
        print(f"{line:03d}: {code}")

    vm = VirtualMachine()
    vm.run(program_code)


def run_program(program: str) -> None:
    lexer = Lexer()
    tokens = lexer.tokenize(program)

    parser = Parser()
    ast = parser.parse_program(tokens)

    compiler = Compiler()
    bytecode = compiler.compile_program(ast)

    vm = VirtualMachine()
    vm.run(bytecode)
    

def main() -> None:
    # test_lexer()
    # test_parser()
    # test_compiler()
    # test_virtual_machine()

    program, expr = test_program()
    run_program(program)


if __name__ == "__main__":
    main()
