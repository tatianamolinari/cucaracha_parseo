import sys
sys.path.insert(0,"../..")

import readline
import ply.lex as lex
import ply.yacc as yacc
import os

class Node:
  def __init__(self,type,children=None,leaf=None):
    self.type = type
    if children:
      self.children = children
    else:
      self.children = [ ]
      self.leaf = leaf

class Parser:
  

  tokens = ()
  precedence = ()

  def __init__(self, **kw):
      self.debug = kw.get('debug', 0)
      self.names = { }
      try:
         modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
      except:
         modname = "parser"+"_"+self.__class__.__name__
      self.debugfile = modname + ".dbg"
      self.tabmodule = modname + "_" + "parsetab"
      #print self.debugfile, self.tabmodule

      # Build the lexer and parser
      self.lexer = lex.lex(module=self, debug=self.debug)
      #yacc.yacc(module=self, debug=self.debug, debugfile=self.debugfile, tabmodule=self.tabmodule)

  def run(self):
    while 1:
      try:
        s = raw_input('cuca > ')
      except EOFError:
        break
      if not s: continue
      yacc.parse(s)

class Cuca(Parser):

  reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    "def": "DEF",
    "return": "RETURN",
    "fun": "FUN"

   }

  

  tokens = list(reserved.values()) + [
      'ID', 'VECTORID', 
      'NUMBER', 
      'TRUE', 'FALSE', 
      'AND', 'OR', 'NOT', 
      'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
      'PLUS','MINUS', 'TIMES',
      'GREATHER', 'GREATHEREQUAL', 'LESSEQUAL', 'LESS', 'EQUAL', 'NOTEQUAL',  
      'ASSIGN',
      'COMMA', 'COLON'
      ]

    # Tokens

  #t_ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'
  t_VECTORID       = r'\#[a-zA-Z_][a-zA-Z0-9_]*'

  t_TRUE            = r'True'
  t_FALSE           = r'False'
    
  t_AND             = r'and'
  t_OR              = r'or'   
  t_NOT             = r'not'
   
  t_LPAREN          = r'\('
  t_RPAREN          = r'\)'
  t_LBRACE          = r'\{'
  t_RBRACE          = r'\}'
  t_LBRACKET        = r'\['
  t_RBRACKET        = r'\]'
    
  t_PLUS            = r'\+'
  t_MINUS           = r'-'
  t_TIMES           = r'\*'
    
  t_GREATHER        = r'>'
  t_GREATHEREQUAL   = r'>='
  t_LESSEQUAL       = r'<='
  t_LESS            = r'<'
  t_EQUAL           = r'=='
  t_NOTEQUAL        = r'!='
    
  t_ASSIGN          = r'='
   
  t_COMMA           = r','
  t_COLON           = r':'


  def t_ID(self,t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = Cuca.reserved.get(t.value,'ID')    # Check for reserved words
    return t
    
  def t_NUMBER(self, t):
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
    ('nonassoc', 'GREATHER', 'GREATHEREQUAL', 'LESSEQUAL', 'LESS', 'EQUAL', 'NOTEQUAL'),  # Nonassociative operators
    ('left', 'AND', 'OR'),
    ('left', 'NOT'),
    #('left', 'GREATHER', 'GREATHEREQUAL', 'LESSEQUAL', 'LESS', 'EQUAL', 'NOTEQUAL')
    ('left', 'MINUS', 'PLUS'),
    ('right', 'TIMES'),            
   )

  def p_statement_assign(self, p):
    '''statement :   ID ASSIGN NUMBER
           |  ID ASSIGN expression'''
    self.names[p[1]] = p[3]

  def p_expression_group(self, p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

  def p_expression_number(self, p):
    'expression : NUMBER'
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
         | expression GREATHER expression
         | expression GREATHEREQUAL expression
         | expression LESSEQUAL expression
         | expression LESS expression
         | expression EQUAL expression
         | expression NOTEQUAL expression'''

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
    p[0] = ('if-expression',p[1],p[2], p[3], p[4])

  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
  def t_error(self, t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

  # FUNCION DE ERROR. ESTO HABRIA QUE MEJORARLO...
  def p_error(self,p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")

  lexer = lex.lex(optimize=1)

if __name__ == "__main__":

  cuca = Cuca()
  data = '''
  fun f() : Int {
  return 1
}

fun g(x : Int) : Int {
  return x
}

fun h(x : Int, y : Int) : Int {
  return x + y
}

fun i(x : Int, y : Int, z : Int) : Int {
  return x * y * z
}

fun beta(x:Bool, y:Bool) : Int {
  if x and y {
    z := 1
  } else {
    z := 0
  }
  return z
}

fun main() {
  v := [1,2,3]
  x := f()
  x := g(100)
  x := g(100 + 100)
  x := g(v[0])
  x := g(#v)
  x := g(#v + 100)
  x := g(f())
  x := h(11,12)
  x := h(v[0],v[1])
  x := h(f(),f())
  x := h(f(),g(f()))
  x := h(f(),g(#v))
  x := h(f(),v[f()])
  x := h(g(f()),f())
  x := h(g(#v),f())
  x := h(v[f()],f())
  x := h(g(f()),g(f()))
  x := h(g(v[f()]),v[f()])
  x := h(v[f()],v[f()])
  x := v[h(v[f()],v[f()])]
  x := i(1,2,3)
  x := v[i(1,2,3)]
  x := v[i(#v,#v + 1,#v+2)]
  x := i(h(1,11),h(2,22),h(3,33))
  x := v[i(h(1,11),h(2,22),h(3,33))]
  x := v[i(h(1,11),h(2,22),h(3,33))]
  x := v[i(h(1,11),h(2,22),h(3,33))]*#v
  x := beta(1 != 2 or 2 != 1, 1 < 2 or 1 > 2)
}

  '''

  # Give the lexer some input
  cuca.lexer.input(data)

  # Tokenize
  while True:
      tok = cuca.lexer.token()
      if not tok: 
          break      # No more input
      print(tok)

