import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca


if __name__ == "__main__":

  cuca = Cuca()
  data = '''fun main() {
  
}'''


  #cuca.lexer.input(data)
  print cuca.yacc.parse(data)

 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
