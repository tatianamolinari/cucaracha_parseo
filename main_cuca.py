import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca
from SemanticAnalizer import *
from optparse import OptionParser
from CucarachaCompiler import CucarachaCompiler

if __name__ == "__main__":

	#parser = OptionParser()
	#parser.add_option("-f", "--file", dest="filename",
	#                  help="Input file to parse", metavar="FILE")


	#(options, args) = parser.parse_args()


	#if options.filename is None:
	#	print "Please give an input file for parsing with the option --file or -f"
	#else:

	cuca = Cuca()
	# 	f = open(options.filename, 'r')
	# 	data = f.read()
	# 	f.close()

	data1 = ''' 

fun expres(i : Int) {
  j := 2 * 2 - 5
  j := 0
}

fun stat(i : Int): Int {
  i := 2
  j := True
  if(True){
  	t := True
  }else{
  	j := False
  	z := 7 
  }

  return i
}

fun main() {
  expres(3)
  x:= 2
  y:= stat(2) 
}
 '''

data2 = ''' 

fun expres(i : Int) {
  i := (2 + 1) * 2
  a := True and False
}


fun main() {
  expres(3)
}
 '''

data3 = ''' 

fun expres(i : Int, y : Int) {
  if(4<1){
  	a:=True
  }

}


fun main() {
  expres(3,2 -1)
}
 '''

data4 = ''' 

fun main() {
	i := (2 + 1) * 2
	j := 4
	putNum(i)
}
 '''

data5 = ''' 

fun main() {
	i:=2
	while(i>0)
	{
	 i:=5
	}

}
 '''

data7 = '''
fun main() {
    if 1 == 1 { putChar(65) }
    if 1 == 2 { putChar(66) }
    if 2 == 2 { putChar(67) }
    if 3 == 2 { putChar(68) }
    if 3 == 3 { putChar(69) }

    x := 1
    if x == 1 { putChar(70) }
    if x == 2 { putChar(71) }
    if 1 == x { putChar(72) }
    if 2 == x { putChar(73) }
    if x == x { putChar(74) }

    x := 2
    if x == 1 { putChar(75) }
    if x == 2 { putChar(76) }
    if 1 == x { putChar(77) }
    if 2 == x { putChar(78) }
    if x == x { putChar(79) }
    putChar(10)

}

''' 

sa = SemanticAnalizer()
program = cuca.yacc.parse(data7)
print "------------------------------- AST from input program ------------------------------- "
print program
  
sa.analizeProgram(program)

cucaracha_compiler = CucarachaCompiler()
cucaracha_compiler.cuca_compile(program)

