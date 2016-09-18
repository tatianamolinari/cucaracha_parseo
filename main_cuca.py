import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca


if __name__ == "__main__":

  cuca = Cuca()
  data = '''fun main() {
  putChar(72)
  putChar(79)
  putChar(76)
  putChar(65)
}'''


  #cuca.lexer.input(data)
  print cuca.yacc.parse(data)

 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
