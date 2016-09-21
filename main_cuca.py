import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca
from SemanticAnalizer import *


if __name__ == "__main__":

  cuca = Cuca()
  data = '''
fun f( e : Bool, t : Int) : Int {
  a := not( True or False)
  return a + y
}

fun w(a : Int) : Int {
  return a
}

fun h(b : Int, c : Int) : Int {
  return b + c
}

fun i(d : Int, e : Int, f : Int) : Int {
  return d * e * f
}

fun betav(g:Bool, h:Bool) : Bool {
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
  #print program
  sa.analizeProgram(program)
 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
