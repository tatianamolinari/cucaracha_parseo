import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca
from SemanticAnalizer import *


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

fun betav(x:Bool, y:Bool) : Vec {
  if x and y {
    z := 1
  } else {
    z := 0
  }
  return z
}

fun main() {
}

'''


  #cuca.lexer.input(data)
  sa = SemanticAnalizer()
  program = cuca.yacc.parse(data)
  sa.analizeProgram(program)
 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
