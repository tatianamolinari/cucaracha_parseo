import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca
from SemanticAnalizer import *


if __name__ == "__main__":

  cuca = Cuca()
  data = '''
fun f( e : Bool, t : Int) : Int {
  a := 1
  return a + t
}

fun main() {
f(True,8)
}

'''


  #cuca.lexer.input(data)
  sa = SemanticAnalizer()
  program = cuca.yacc.parse(data)
  #print program
  sa.analizeProgram(program)
 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
