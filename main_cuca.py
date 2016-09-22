import sys, os
sys.path.insert(0,"../..")

from lexer_cuca import Cuca
from SemanticAnalizer import *
from optparse import OptionParser

if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
	                  help="Input file to parse", metavar="FILE")


	(options, args) = parser.parse_args()


	if options.filename is None:
		print "Please give an input file for parsing with the option --file or -f"
	else:

	 	cuca = Cuca()
	 	f = open(options.filename, 'r')
	 	data = f.read()
	 	f.close()

		sa = SemanticAnalizer()
		program = cuca.yacc.parse(data)
	 	print "------------------------------- AST from input program ------------------------------- "
		print program
	  
	 	sa.analizeProgram(program)

