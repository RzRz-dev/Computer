import ply.yacc as yacc
from lexical_analyzer import LexicalAnalyzer

# Crea instancia del lexer
lex_analyzer = LexicalAnalyzer()
lexer = lex_analyzer.lexer

# Obtiene los tokens del lexer
tokens = lex_analyzer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
)
# -------------------------------------------------
# PROGRAMA
# -------------------------------------------------

def p_program(p):
    'program : declaration_list'
    p[0] = p[1]

# -------------------------------------------------
# DECLARATIONS
# -------------------------------------------------

def p_declaration_list_multi(p):
    'declaration_list : declaration_list declaration'
    p[0] = p[1] + [p[2]]

def p_declaration_list_single(p):
    'declaration_list : declaration'
    p[0] = [p[1]]

def p_declaration(p):
    '''declaration : func_decl
                   | struct_decl
                   | typedef_decl
                   | var_decl'''
    p[0] = p[1]

# -------------------------------------------------
# FUNCTION
# -------------------------------------------------

def p_func_decl(p):
    'func_decl : FUNC type ID LPAREN param_list_opt RPAREN block'
    p[0] = ("func", p[2], p[3], p[5], p[7])

def p_param_list_opt(p):
    '''param_list_opt : param_list
                      | empty'''
    p[0] = p[1]

def p_param_list_multi(p):
    'param_list : param_list COMMA param'
    p[0] = p[1] + [p[3]]

def p_param_list_single(p):
    'param_list : param'
    p[0] = [p[1]]

def p_param(p):
    'param : type ID array_opt'
    p[0] = ("param", p[1], p[2], p[3])

def p_array_opt(p):
    '''array_opt : LBRACKET RBRACKET
                 | empty'''
    p[0] = p[1:]

# -------------------------------------------------
# STRUCT
# -------------------------------------------------

def p_struct_decl(p):
    'struct_decl : STRUCT ID LBRACE field_list RBRACE'
    p[0] = ("struct", p[2], p[4])

def p_field_list_multi(p):
    'field_list : field_list field_decl'
    p[0] = p[1] + [p[2]]

def p_field_list_single(p):
    'field_list : field_decl'
    p[0] = [p[1]]

def p_field_decl(p):
    'field_decl : type ID array_size_opt SEMICOLON'
    p[0] = ("field", p[1], p[2], p[3])

def p_array_size_opt(p):
    '''array_size_opt : LBRACKET INT_LITERAL RBRACKET
                      | empty'''
    p[0] = p[1:]

def p_typedef_decl(p):
    'typedef_decl : TYPEDEF type ID SEMICOLON'
    p[0] = ("typedef", p[2], p[3])


# -------------------------------------------------
# TYPES
# -------------------------------------------------

def p_type_primitive(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOL
            | VOID'''
    p[0] = p[1]

def p_type_id(p):
    'type : ID'
    p[0] = p[1]

# -------------------------------------------------
# VARIABLES
# -------------------------------------------------

def p_var_decl(p):
    'var_decl : type ID var_suffix_opt init_opt SEMICOLON'
    p[0] = ("var", p[1], p[2], p[3], p[4])

def p_var_suffix_opt(p):
    '''var_suffix_opt : array_suffix
                      | matrix_suffix
                      | empty'''
    p[0] = p[1]

def p_array_suffix(p):
    'array_suffix : LBRACKET INT_LITERAL RBRACKET'
    p[0] = ("array", p[2])

def p_matrix_suffix(p):
    'matrix_suffix : LBRACKET INT_LITERAL RBRACKET LBRACKET INT_LITERAL RBRACKET'
    p[0] = ("matrix", p[2], p[5])

def p_init_opt(p):
    '''init_opt : ASSIGN expr
                | empty'''
    p[0] = p[2] if len(p) > 2 else None

# -------------------------------------------------
# BLOCK & STATEMENTS
# -------------------------------------------------

def p_block(p):
    'block : LBRACE stmt_list RBRACE'
    p[0] = p[2]

def p_stmt_list_multi(p):
    'stmt_list : stmt_list statement'
    p[0] = p[1] + [p[2]]

def p_stmt_list_single(p):
    'stmt_list : statement'
    p[0] = [p[1]]

def p_statement(p):
    '''statement : var_decl
                 | assign_stmt
                 | if_stmt
                 | while_stmt
                 | for_stmt
                 | do_while_stmt
                 | return_stmt
                 | break_stmt
                 | continue_stmt
                 | push_stmt
                 | pop_stmt
                 | func_call_stmt
                 | block'''
    p[0] = p[1]

# -------------------------------------------------
# ASSIGN
# -------------------------------------------------

def p_assign_stmt(p):
    'assign_stmt : lvalue assign_op expr SEMICOLON'
    p[0] = ("assign", p[1], p[2], p[3])

def p_assign_op(p):
    '''assign_op : ASSIGN
                 | PLUS_ASSIGN
                 | MINUS_ASSIGN
                 | TIMES_ASSIGN
                 | DIVIDE_ASSIGN'''
    p[0] = p[1]

# -------------------------------------------------
# LVALUE
# -------------------------------------------------

def p_lvalue(p):
    'lvalue : ID lvalue_tail'
    p[0] = ("lvalue", p[1], p[2])

def p_lvalue_tail_multi(p):
    'lvalue_tail : lvalue_tail lvalue_access'
    p[0] = p[1] + [p[2]]

def p_lvalue_tail_empty(p):
    'lvalue_tail : empty'
    p[0] = []

def p_lvalue_access(p):
    '''lvalue_access : DOT ID
                     | LBRACKET expr RBRACKET'''
    p[0] = p[1:]


# -------------------------------------------------
# FUNC CALL
# -------------------------------------------------

def p_func_call_stmt(p):
    'func_call_stmt : func_call SEMICOLON'
    p[0] = p[1]

def p_func_call(p):
    'func_call : ID LPAREN arg_list_opt RPAREN'
    p[0] = ("call", p[1], p[3])

def p_arg_list_opt(p):
    '''arg_list_opt : arg_list
                    | empty'''
    p[0] = p[1]

def p_arg_list_multi(p):
    'arg_list : arg_list COMMA expr'
    p[0] = p[1] + [p[3]]

def p_arg_list_single(p):
    'arg_list : expr'
    p[0] = [p[1]]


# -------------------------------------------------
# IF, ELSE IF, ELSE
# -------------------------------------------------

def p_if_stmt(p):
    'if_stmt : IF LPAREN expr RPAREN block else_if_opt'
    p[0] = ("if", p[3], p[5], p[6])

def p_else_if_opt(p):
    '''else_if_opt : else_if_list
                   | else_opt
                   | empty'''
    p[0] = p[1]

def p_else_if_list(p):
    'else_if_list : ELSE IF LPAREN expr RPAREN block else_if_list'
    p[0] = p[1] + [("elif", p[4], p[6])]

def p_else_if_single(p):
    'else_if_list : ELSE IF LPAREN expr RPAREN block else_if_opt'
    p[0] = [("elif", p[3], p[5])]

def p_else_opt(p):
    '''else_opt : ELSE block
                | empty'''
    p[0] = p[2] if len(p) > 2 else None

# -------------------------------------------------
# WHILE, FOR, DO-WHILE
# -------------------------------------------------

def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expr RPAREN block'
    p[0] = ("while", p[3], p[5])

def p_for_stmt(p):
    'for_stmt : FOR LPAREN for_init SEMICOLON expr_opt SEMICOLON for_update RPAREN block'
    p[0] = ("for", p[3], p[5], p[7], p[9])

def p_for_init(p):
    '''for_init : var_decl_inline
                | assign_stmt_inline
                | empty'''
    p[0] = p[1]

def p_for_update(p):
    '''for_update : assign_stmt_inline_list
                  | empty'''
    p[0] = p[1]

def p_assign_stmt_inline_list(p):
    'assign_stmt_inline_list : assign_stmt_inline_list COMMA assign_stmt_inline'
    p[0] = p[1] + [p[3]]

def p_assign_stmt_inline_single(p):
    'assign_stmt_inline_list : assign_stmt_inline'
    p[0] = [p[1]]

def p_assign_stmt_inline(p):
    'assign_stmt_inline : lvalue assign_op expr'
    p[0] = ("assign", p[1], p[2], p[3])

def p_var_decl_inline(p):
    'var_decl_inline : type ID init_opt'
    p[0] = ("var_decl", p[1], p[2], p[3])

def p_do_while_stmt(p):
    'do_while_stmt : DO block WHILE LPAREN expr RPAREN SEMICOLON'
    p[0] = ("do_while", p[2], p[5])


# -------------------------------------------------
# RETURN, BREAK, CONTINUE
# -------------------------------------------------

def p_return_stmt(p):
    'return_stmt : RETURN expr_opt SEMICOLON'
    p[0] = ("return", p[2])

def p_break_stmt(p):
    'break_stmt : BREAK SEMICOLON'
    p[0] = ("break",)

def p_continue_stmt(p):
    'continue_stmt : CONTINUE SEMICOLON'
    p[0] = ("continue",)

def p_expr_opt(p):
    '''expr_opt : expr
                | empty'''
    p[0] = p[1]


# -------------------------------------------------
# EXPRESSIONS
# -------------------------------------------------

def p_expr(p):
    'expr : logic_or'
    p[0] = p[1]

def p_logic_or(p):
    '''logic_or : logic_or OR logic_and
                | logic_and'''
    p[0] = p[1] if len(p) == 2 else ("or", p[1], p[3])

def p_logic_and(p):
    '''logic_and : logic_and AND equality
                 | equality'''
    p[0] = p[1] if len(p) == 2 else ("and", p[1], p[3])

def p_equality(p):
    '''equality : equality EQ relational
                | equality NEQ relational
                | relational'''
    p[0] = p[1] if len(p) == 2 else ("eq", p[1], p[3])

def p_relational(p):
    '''relational : relational LT additive
                  | relational GT additive
                  | relational LEQ additive
                  | relational GEQ additive
                  | additive'''
    p[0] = p[1] if len(p) == 2 else ("rel", p[1], p[3])

def p_additive(p):
    '''additive : additive PLUS term
                | additive MINUS term
                | term'''
    p[0] = p[1] if len(p) == 2 else ("add", p[1], p[3])

def p_term(p):
    '''term : term TIMES unary
            | term DIVIDE unary
            | term MODULO unary
            | unary'''
    p[0] = p[1] if len(p) == 2 else ("mul", p[1], p[3])

def p_unary(p):
    '''unary : NOT unary
             | MINUS unary
             | postfix'''
    p[0] = ("unary", p[1], p[2]) if len(p) == 3 else p[1]

def p_postfix(p):
    'postfix : primary postfix_tail'
    p[0] = ("postfix", p[1], p[2])

def p_postfix_tail_multi(p):
    'postfix_tail : postfix_tail postfix_access'
    p[0] = p[1] + [p[2]]

def p_postfix_tail_empty(p):
    'postfix_tail : empty'
    p[0] = []

def p_postfix_access(p):
    '''postfix_access : DOT ID
                      | LBRACKET expr RBRACKET'''
    p[0] = p[1:]

def p_primary(p):
    '''primary : literal
               | func_call
               | lvalue
               | LPAREN expr RPAREN'''
    p[0] = p[1] if len(p) == 2 else p[2]

# -------------------------------------------------
# PUSH, POP
# -------------------------------------------------
def p_push_stmt(p):
    'push_stmt : PUSH LPAREN expr RPAREN SEMICOLON'
    p[0] = ("push", p[3])

def p_pop_stmt(p):
    'pop_stmt : POP LPAREN RPAREN SEMICOLON'
    p[0] = ("pop",)

# -------------------------------------------------
# LITERALS
# -------------------------------------------------

def p_literal(p):
    '''literal : INT_LITERAL
               | FLOAT_LITERAL
               | CHAR_LITERAL
               | STRING_LITERAL
               | TRUE
               | FALSE'''
    p[0] = p[1]


# -------------------------------------------------
# EMPTY
# -------------------------------------------------

def p_empty(p):
    'empty :'
    pass

# -------------------------------------------------
# MANEJO DE ERRORES
# -------------------------------------------------

def p_error(p):
    if p:
        print(f"Error sintáctico en línea {p.lineno}: token inesperado '{p.value}' (tipo: {p.type})")
    else:
        print("Error sintáctico: fin de archivo inesperado")

# -------------------------------------------------
# CONSTRUCCIÓN DEL PARSER
# -------------------------------------------------

# Crea el parser (solo una vez)
parser = yacc.yacc(debug=False, write_tables=False, module=None)

# -------------------------------------------------
# FUNCIÓN PARA ANALIZAR
# -------------------------------------------------

def parse(code: str):
    """
    Analiza código fuente y retorna el AST.
    
    Args:
        code (str): Código fuente a analizar
        
    Returns:
        Árbol sintáctico o None si hay errores
    """
    # Tokeniza el código
    tokens, lex_errors = lex_analyzer.tokenize(code)
    
    # Si hay errores léxicos, imprime y retorna
    if lex_errors:
        print("Errores léxicos encontrados:")
        for error in lex_errors:
            print(f"  Línea {error['line']}: {error['message']}")
        return None
    
    # Parsea el código
    ast = parser.parse(code, lexer=lexer)
    return ast

if __name__ == "__main__":
    # Código de prueba
    code = """
    func int suma(int a, int b) {
        return a + b;
    }
    
    func void main() {
        int x = 5;
        int y = 10;
        int z = suma(x, y);
    }
    """
    
    result = parse(code)
    if result:
        print("\nÁrbol sintáctico generado exitosamente")
        print(result)