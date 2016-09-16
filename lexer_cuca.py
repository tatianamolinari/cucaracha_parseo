# coding: utf-8

import sys, os
sys.path.insert(0,"../..")

from parser import Parser
from node import Node

class Cuca(Parser):

  

  reserved = {
    'if'     : 'IF',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'def'    : 'DEF',
    'return' : 'RETURN',
    'fun'    : 'FUN',
    'and'    : 'AND',
    'or'     : 'OR',
    'not'    : 'NOT', 
    'Bool'   : 'BOOL',
    'Int'    : 'INT',
    'Vec'    : 'VEC',
    'True'   : 'TRUE',
    'False'  : 'FALSE'
   }

  

  tokens = list(reserved.values()) + [
      'ID',
      'NUM', 
      'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACK', 'RBRACK',
      'PLUS','MINUS', 'TIMES',
      'GT', 'GE', 'LE', 'LT', 'EQ', 'NE',  
      'ASSIGN',
      'COMMA', 'COLON', 'HASH'
      ]

  # Tokens
   
  t_LPAREN          = r'\('
  t_RPAREN          = r'\)'
  t_LBRACE          = r'\{'
  t_RBRACE          = r'\}'
  t_LBRACK          = r'\['
  t_RBRACK          = r'\]'
    
  t_PLUS            = r'\+'
  t_MINUS           = r'-'
  t_TIMES           = r'\*'
    
  t_GT              = r'>'
  t_GE              = r'>='
  t_LE              = r'<='
  t_LT              = r'<'
  t_EQ              = r'=='
  t_NE              = r'!='
    
  t_ASSIGN          = r':='
   
  t_COMMA           = r','
  t_COLON           = r':'
  t_HASH            = r'\#'


  def t_ID(self,t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = Cuca.reserved.get(t.value,'ID')    # Cheque de palabras reservadas
    return t
    
  def t_NUM(self, t):
    r'\d+'
    try:
      t.value = int(t.value)
    except ValueError:
      print "Integer value too large", t.value
      t.value = 0
      #print "parsed number %s" % repr(t.value)
    return t

  t_ignore_COMMENT = r'\/\/*'
  t_ignore = " \t"

  precedence = (
    ('nonassoc', 'GT', 'GE', 'LE', 'LT', 'EQ', 'NE'),  # operaciones no asociativas
    ('left', 'AND', 'OR'),
    ('left', 'NOT'),
    ('left', 'MINUS', 'PLUS'),
    ('right', 'TIMES'),            
   )

  def p_empty(self, p):
    ''' empty : '''
    pass

# ******************* ProgramT *******************
#                Program [FunctionT]

  def p_empty_program(self, p):
    ''' empty_program : empty'''
    p[0] = Program(children=[])

  def p_not_empty_program(self,p):
    ''' not_empty_program : function_declaration program '''
    p[0] = p[2].push(p[1])

  def p_program(self, p):
    ''' program : empty_program 
                | p_not_empty_program '''
    return p[1]


# ******************* FunctionT *******************
#         Function Id Type [ParameterT] BlockT
  def p_void_function_declaration(self,p):
     ''' void_function_declaration  : FUN ID params block'''
     p[0] = Function(children=[p[2],'Unit',p[3],p[4]])

  def p_function_declaration_with_type(self,p):
    ''' function_declaration_with_type  : FUN ID params COLON type block '''
    p[0] = Function(children=[p[2],p[4],p[3],p[5]])

  def p_function_declaration(self, p):
    ''' function_declaration  : void_function_declaration 
                              | function_declaration_with_type '''
     p[0] = p[1]
# ******************* ParameterT *******************
#                  Parameter Id Type

  def p_empty_params(self, p):
    ''' empty_params : empty'''
    p[0] = []

  def p_params(self, p):
    ''' params : LPARENT params_list RPARENT'''
    p[0] = p[1]

  def p_params_list(self, p):
    ''' params_list : empty 
                    | not_empty_params_list'''
    p[0] = p[1]

  def p_parameters_list(self,p):
    ''' parameters_list :  parameter COMMA not_empty_params_list '''
    p[0] = p[2].push(p[1])


  def p_not_empty_params_list(self, p):
    ''' not_empty_params_list : parameter 
                              | parameters_list '''
    p[0] = p[1]

  def p_parameter(self, p):
    ''' parameter : ID COLON type '''
    p[0] = Parameter(p[1],p[2])

# ******************* Type *******************
# Int | Bool | Vec

  def p_type(self, p):
    ''' type : INT
             | BOOL
             | VEC '''
    p[0] = p[1]
# ******************* BlockT *******************
#                  Block [StmtT]

  def p_block(self, p):
    ''' block : LBRACE instructions_list RBRACE '''
    p[0] = Block(children=p[2])

# ******************* StmtT ******************* 

  # StmtAssign Id ExprT
  def p_assing(self,p):
    '''assing : ID ASSIGN expression'''
    self.names[p[1]] = p[3]
    p[0] = StmtAssign(children=[p[1],p[3]])

  # StmtVecAssign Id ExprT ExprT 
  def p_vector_assing(self,p):
    '''vector_assing : ID LBRACK expression RBRACK ASSIGN expression'''
    p[0] = StmtVecAssign(children=[p[1],p[3],p[6]])

  # StmtIf ExprT BlockT
  def p_if_stmt(self,p):
    ''' if_stmt : IF expression block'''
    p[0] = StmtIf(children=[p[2],p[3]])

  # StmtIfElse ExprT BlockT BlockT
  def p_if_else_stmt(self,p):
    ''' if_else_stmt : IF expression block ELSE block'''
    p[0] = StmtIfElse(children=[p[2],p[3],p[5]])

  # StmtWhile ExprT BlockT
  def p_while_stmt(self,p):
    ''' while_stmt : WHILE expression block'''
    p[0] = StmtWhile(children=[p[2],p[3]])

  # StmtReturn ExprT
  def p_return_stmt(self,p):
    ''' return_stmt : RETURN expression'''
    p[0] = StmtReturn(children=[p[2]]) 

  # StmtCall Id [ExprT]
  def p_call_stmt(self,p):
    ''' call_stmt : ID LPAREN expressions_list RPAREN'''
    p[0] = StmtCall(children=[p[1],p[2]])

  def p_instruction(self,p):
    ''' instruction : assing
                    | vector_assing
                    | if_stmt
                    | if_else_stmt
                    | while_stmt
                    | return_stmt
                    | call_stmt '''
    p[0] = p[1]

  def p_empty_instructions_list(self, p):
    '''empty_instructions_list :  empty'''
    p[0]=[]
      
  def p_not_empty_instructions_list(self, p):
    '''not_empty_instructions_list :  instruction instructions_list'''
    p[0] = p[2].append(p[1])


  def p_instructions_list(self, p):
    '''instructions_list : p_empty_instructions_list
                         |  not_empty_instructions_list'''
    p[0] = p[1]


# ******************* ExprT *******************

# ExprVar Id Uso de una variable.
# ExprConstNum Integer Constante numerica.
# ExprConstBool Bool Constante booleana.
# ExprVecMake [ExprT] Construccion de un vector.
# ExprVecLength Id Longitud de un vector.
# ExprVecDeref Id ExprT Acceso al i-esimo de un vector.
# ExprCall Id [ExprT] Invocacion a una funcion. 

# ExprAdd ExprT ExprT Suma.
# ExprSub ExprT ExprT Resta.
# ExprMul ExprT ExprT Multiplicacion.

  def p_empty_expression_list(self,p):
    ''' empty_expression_list : empty'''
    p[0] = []
    
  def p_expressions_list(self,p):
    ''' expressions_list : empty_expression_list
                         | not_empty_expressions_list'''
    p[0] = p[1]


  def p_not_empty_expressions_list_head(self,p):
    ''' not_empty_expressions_list_head : expression COMMA not_empty_expressions_list'''
    p[0] = [p[1]]++p[3]
    
  def p_not_empty_expressions_list(self,p):
    ''' not_empty_expressions_list : expression
                                   | not_empty_expressions_list_head'''
    p[0] = p[1]

  def p_expression(self,p):
    ''' expression : logic_expression '''
    p[0] = p[1]

  def binary_expression_get_p(self,argument,expression1,expression2):
    switcher = {
        '<=':   ExprLe(children=[expression1,expression2]),  # ExprLe ExprT ExprT
        '>=':   ExprGe(children=[expression1,expression2]),  # ExprGe ExprT ExprT
        '<' :   ExprLt(children=[expression1,expression2]),  # ExprLt ExprT ExprT
        '>' :   ExprGt(children=[expression1,expression2]),  # ExprGt ExprT ExprT
        '==':   ExprEq(children=[expression1,expression2]),  # ExprEq ExprT ExprT
        '!=':   ExprNe(children=[expression1,expression2]),  # ExprNe ExprT ExprT
        '+' :   ExprAdd(children=[expression1,expression2]), # ExprAdd ExprT ExprT
        '-' :   ExprSub(children=[expression1,expression2]), # ExprSub ExprT ExprT
        '*' :   ExprMul(children=[expression1,expression2]), # ExprMul ExprT ExprT
        'and':  ExprAnd(children=[expression1,expression2]), # ExprAnd ExprT ExprT
        'or':   ExprOr(children=[expression1,expression2])   # ExprOr ExprT ExprT
        }
    return switcher.get(argument, "ERROR")

  def p_binary_logic_expression(self,p):
    ''' binary_logic_expression  : logic_expression AND atomic_logic_expression
                                 | logic_expression OR atomic_logic_expression'''
    p[0]=self.binary_expression_get_p(p[2],p[1],p[3])
    
  # ExprNot ExprT
  def p_atomic_logic_expression_not(self, p):
    ''' atomic_logic_expression_not : NOT atomic_logic_expression'''
    p[0] = ExprNot(p[2])

  def p_logic_expression(self, p): 
    ''' logic_expression  : binary_logic_expression
                          | atomic_logic_expression '''
    p[0] = p[1]

  def p_atomic_logic_expression(self, p):
    ''' atomic_logic_expression : atomic_logic_expression_not
                                | relational_expression '''
    p[0] = p[1]


  def p_binary_relational_expression(self, p): 
    ''' binary_relational_expression : additive_expression LE additive_expression
                                     | additive_expression GE additive_expression
                                     | additive_expression LT additive_expression
                                     | additive_expression GT additive_expression
                                     | additive_expression EQ additive_expression
                                     | additive_expression NE additive_expression'''
    p[0] = self.binary_expression_get_p(p[2],p[1],p[3])


  def p_relational_expression(self, p):
    ''' relational_expression : binary_relational_expression
                              | additive_expression '''
    return p[0] = p[1]

  def p_additive_binary_expression(self,p):
    ''' additive_binary_expression : additive_expression PLUS multiplicative_expression
                                   | additive_expression MINUS multiplicative_expression '''
  
    p[0] = self.binary_expression_get_p(p[2],p[1],p[3])  
  

  def p_additive_expression(self, p):
    ''' additive_expression : additive_binary_expression
                            | multiplicative_expression '''
    p[0] = p[1]

  def p_multiplicative_binary_expression(self,p):
    ''' multiplicative_binary_expression : multiplicative_expression TIMES atomic_expression'''
    p[0] = self.binary_expression_get_p(p[2],p[1],p[3]) 
    
  def p_multiplicative_expression(self, p):
    ''' multiplicative_expression : multiplicative_binary_expression
                                  | atomic_expression '''
    p[0] = p[1]


  def p_atomic_expression_three(self, p):
    ''' atomic_expression_three : LBRACK expressions_list RBRACK
                                | LPAREN expression RPAREN '''
    p[0]=p[2]


  def p_atomic_id_expression(self,p):
    ''' atomic_id_expression : ID LBRACK expression RBRACK'''
    p[0]=[p[1],p[3]]
      
  def p_atomic_expression_list(self,p):
    ''' atomic_expression_list : ID LPAREN expressions_list RPAREN'''
    p[0]=[p[1]]++p[3]

    
  def p_atomic_expression(self, p):
    ''' atomic_expression : ID
                          | NUM
                          | TRUE
                          | FALSE
                          | HASH ID
                          | atomic_id_expression
                          | atomic_expression_list
                          | atomic_expression_three '''
    p[0]= p[1] 

  def p_expression_group(self, p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

  def p_expression_number(self, p):
    'expression : NUM'
    p[0] = p[1]

  def p_expression_name(self, p):
    'expression : ID'
    try:
      p[0] = self.names[p[1]]
    except LookupError:
      print "Undefined name '%s'" % p[1]
      p[0] = 0

  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
  def t_error(self, t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

  # FUNCIÓN DE ERROR. ESTO HABRIA QUE MEJORARLO...
  def p_error(self,p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")

  #lexer = lex.lex(optimize=1)
