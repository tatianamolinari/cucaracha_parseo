import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca


if __name__ == "__main__":

  cuca = Cuca()
  data = '''fun producto(v : Vec) : Int {
  i := 0
  p := 1
  while i < #v {
    p := p * v[i]
    i := i + 1
  }
  return p
}
'''


  #cuca.lexer.input(data)
  print cuca.yacc.parse(data)

 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
