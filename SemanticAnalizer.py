import sys, os
sys.path.insert(0,"../..")
from node import *

class SemanticAnalizer:


	#data FunctionT :: = Function Id Type [ParameterT] BlockT
	#data ParameterT :: = Parameter Id Type

	def __init__(self):
		
		self.program = None
		self.program_functions = None
		self.function_variables = {}
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
		self.checkMainFunction()
		self.checkFunctionVariables()
		print self.program_functions

	def completeProgramFunctions(self,node):
		if node.isFunction():
			name = node.getName()
			typee = node.getType()
			if not name in self.program_functions.keys():
				if typee=='Vec':
					print "Error: Function cannot return Vec type"
				else:
					self.program_functions[name] = node
			else:
				print "Error: Function already defined - " + name
		else: 
			for child in node.children:
				self.completeProgramFunctions(child)
	
	def checkMainFunction(self):
		if 'main' in self.program_functions.keys():
			if self.program_functions['main'].getType() != 'Unit':
				print "Error: main function. Only can have Unit return type."
		else:
			print "Error: Must exit a main function"

	def checkFunctionVariables(self):
		print "Prueba de identificacion de Blocks"
		for function in self.program_functions.values():
			self.function_variables = function.getParameters()
			print "......................."
			for child in function.children:
				if child.isBlock():
					for subchild in child.children:
						if subchild.isStmtAssign():
							self.function_variables[subchild.children[0].leaf] = subchild.children[1].getType()
							print self.function_variables
						else:
							print subchild
			print "......................."






