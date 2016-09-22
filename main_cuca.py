import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca
from SemanticAnalizer import *


if __name__ == "__main__":

  cuca = Cuca()
  data = '''
fun g(i : Bool){
	
}

fun main() {
  
  x := g(#ha)
  
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
