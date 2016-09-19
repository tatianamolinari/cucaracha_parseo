import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca


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


  #cuca.lexer.input(data)
  print cuca.yacc.parse(data)

 # Tokenize
 # while True:
 #     tok = cuca.lexer.token()
 #     if not tok: 
 #         break      # No more input
 #     print(tok)
