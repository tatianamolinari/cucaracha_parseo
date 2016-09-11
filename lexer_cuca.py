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

  def p_program(self, p):
    ''' program : empty 
                | function_declaration program '''
    return ??

  def p_function_declaration(self, p):
    ''' function_declaration  : FUN ID params block 
                              | FUN ID params COLON type block '''
    return ??

  def p_params(self, p):
    ''' params : LPARENT params_list RPARENT'''
    return ??

  def p_params_list(self, p):
    ''' params_list : empty 
                    | not_empty_params_list'''
    return ??

  def p_not_empty_params_list(self, p):
    ''' not_empty_params_list : parameter 
                              | not_empty_params_list '''
    return ???

  def p_parameter(self, p):
    ''' parameter : ID COLON type '''
    return ??

  def p_type(self, p):
    ''' type : INT
             | BOOL
             | VEC '''
    return ??

  def p_block(self, p):
    ''' block : LBRACE instructions_list RBRACE '''
    return ??

  def p_instructions_list(self, p):
    '''instructions_list : empty
                         |  instruction instructions_list'''
    return ??

  def p_instruction(self,p):
    ''' instruction : ID ASSIGN expression
                    | ID LBRACK expression RBRACK ASSIGN expression
                    | IF expression block
                    | IF expression block ELSE block
                    | WHILE expression block
                    | RETURN expression
                    | ID LPAREN expressions_list RPAREN '''
    return ??

  def p_expressions_list(self,p):
    ''' expressions_list : empty
                         | not_empty_expressions_list'''
    return ??

  def p_not_empty_expressions_list(self,p):
    ''' not_empty_expressions_list : expression
                                   | expression COMMA not_empty_expressions_list'''
    return ??

  def p_expression(self,p):
    ''' expression : logic_expression '''
    return ??

  def p_logic_expression(self, p): 
    ''' logic_expression  : logic_expression AND atomic_logic_expression
                          | logic_expression OR atomic_logic_expression
                          | atomic_logic_expression '''
    return ??

  def p_atomic_logic_expression(self, p):
    ''' atomic_logic_expression : NOT atomic_logic_expression
                                | relational_expression '''
    return ??

  def p_relational_expression(self, p):
    ''' relational_expression : additive_expression LE additive_expression
                              | additive_expression GE additive_expression
                              | additive_expression LT additive_expression
                              | additive_expression GT additive_expression
                              | additive_expression EQ additive_expression
                              | additive_expression NE additive_expression
                              | additive_expression '''
    return ??

  def p_additive_expression(self, p):
    ''' additive_expression : additive_expression PLUS multiplicative_expression
                            | additive_expression MINUS multiplicative_expression
                            | multiplicative_expression '''
    return ??

  def p_multiplicative_expression(self, p):
    ''' multiplicative_expression : multiplicative_expression TIMES atomic_expression
                                  | atomic_expression '''
    return ??

  def atomic_expression(self, p):
    ''' atomic_expression : ID
                          | NUM
                          | TRUE
                          | FALSE
                          | LBRACK expressions_list RBRACK
                          | HASH ID
                          | ID LBRACK expression RBRACK
                          | ID LPAREN expressions_list RPAREN
                          | LPAREN expression RPAREN '''
    return ??






  # Hay que chequear estás funciones

  def p_statement_assign(self, p):
    '''statement :   ID ASSIGN NUM
           |  ID ASSIGN expression'''
    self.names[p[1]] = p[3]

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

  def p_expression_binop(self,p):
    '''expression : expression PLUS expression
         | expression MINUS expression
         | expression TIMES expression
         | expression AND expression
         | expression OR expression
         | expression GT expression
         | expression GE expression
         | expression LE expression
         | expression LT expression
         | expression EQ expression
         | expression NE expression'''

                #type     children    leaf
    p[0] = Node("binop", [p[1],p[3]], p[2])
    #p[0] = ('binary-expression',p[2],p[1],p[3])

  def p_expression_simpleop(self, p):
    '''statement :   NOT expression'''
    p[0] = ('simple-expression',p[1],p[2])

  def p_expression_if(self, p):
    'expression : IF expression'
    p[0] = ('if-expression',p[1],p[2])

  def p_expression_ifelse(self, p):
    'expression : IF expression ELSE expression'
    p[0] = ('if-else-expression',p[1],p[2], p[3], p[4])

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
