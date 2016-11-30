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

	data = ''' 

fun expres(i : Int) {
  i := 2 * 2 - 5
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

data = ''' 

fun expres(i : Int) {
  i := (2 + 1) * 2
  a := True and False
}


fun main() {
  expres(3)
}
 '''

data = ''' 

fun expres(i : Int) {
  if(i<1){
  	a:=True
  }else{
  	a:=False
  }

}


fun main() {
  expres(3)
}
 '''
sa = SemanticAnalizer()
program = cuca.yacc.parse(data)
print "------------------------------- AST from input program ------------------------------- "
#print program
  
sa.analizeProgram(program)

cucaracha_compiler = CucarachaCompiler()
cucaracha_compiler.cuca_compile(program)

