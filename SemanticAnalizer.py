import sys, os
sys.path.insert(0,"../..")
from node import *

class SemanticAnalizer:


	#data FunctionT :: = Function Id Type [ParameterT] BlockT
	#data ParameterT :: = Parameter Id Type

	def __init__(self):
		
		self.program = None
		self.program_functions = None
		parameter = Parameter(children=[Id(leaf='x'),Type(leaf='Int')])
		empty_block=Block(children=[])
		type_unit = Type(leaf='Unit')
     		putChar = Function(children=[Id(leaf='putChar'),type_unit,parameter,empty_block])
     		putNum = Function(children=[Id(leaf='putNum'),type_unit,parameter,empty_block])
     		self.static_program_functions = {
	  	'putChar':putChar,
	  	'putNum':putNum
	  	}


	def analizeProgram(self,program):
		self.program = program	
		self.program_functions = self.static_program_functions
		self.completeProgramFunctions(program)
		print self.program_functions

	def completeProgramFunctions(self,node):
		if node.isFunction():
			name = node.getName()
			typee = node.getType()
			if not name in self.program_functions.keys():
				if typee=='Vec':
					print "error el tipo de retorno es Vec y eso no esta permitido "
				else:
					self.program_functions[name] = node
			else:
				print "error dos veces la funcion " + name
		else: 
			for child in node.children:
				self.completeProgramFunctions(child)	






