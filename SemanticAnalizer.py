import sys, os
sys.path.insert(0,"../..")
from node import *
from semantic_exceptions import *

class SemanticAnalizer:

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
		print "------------------------------- Semantic Analize check ------------------------------- "
		self.program = program	
		self.program_functions = self.static_program_functions.copy()
		try:
			self.completeProgramFunctions(program)
			self.checkMainFunction()
			self.checkFunctionVariables()
		except Error as e:
			print e
			return None

		print  "Success Semantic Analize done"	

		print "-------------------------------------------------------------------------------------- " 

	def completeProgramFunctions(self,node):
		if node.isFunction():
			name = node.getName()
			typee = node.getType()
			if not name in self.program_functions.keys():
				if typee=='Vec':
					raise TypeError("Error: Function cannot return Vec type")
				else:
					self.program_functions[name] = node
			else:
				raise AlreadyDefinedError("Error: Function already defined - " + name)
		else: 
			for child in node.children:
				self.completeProgramFunctions(child)
	
	def checkMainFunction(self):
		if 'main' in self.program_functions.keys():
			mainFunction = self.program_functions['main']
			if mainFunction.getType() != 'Unit':
				raise TypeError("Error: main function. Only can have Unit return type.")
			if len(mainFunction.getParameters()) != 0: 
				raise Error("Error: main function must not have any params.")
		else:
			raise Error("Error: Must exist a main function")

	def checkFunctionVariables(self):

		for function in self.program_functions.values():
			dic_function = self.program_functions.copy()
			dic_function.pop('main')
			dic_function.update(function.getParameters())
			typeFun = function.getType()
			name = function.getName()
			self.checkBlockFunction(function.getBlock(),typeFun,dic_function)


	def updateValuesDic(self,dic1,dic2):
		keys_dic1 = dic1.keys()
		for key in dic2:
			if key in keys_dic1:
				dic1[key] = dic2[key]
		return dic1

	def checkBlockFunction(self,block,type_fun='Unit',vars_table={}):
		copy_of_vars_table = vars_table.copy()
		for instruction in block.children:

			if instruction.isStmtAssign():
				self.checkAssignStmt(instruction,copy_of_vars_table)
				continue

			if instruction.isCondtionStmt():
				self.checkConditionStatment(instruction,copy_of_vars_table,type_fun)
				continue

			if instruction.isVecAssing():
				self.checkVecAssing(instruction,copy_of_vars_table)
				continue

			if instruction.isCallStmt():
				self.checkCallStmt(instruction,copy_of_vars_table)
				continue

			if instruction.isReturnStmt():
				self.checkReturnStmt(instruction,copy_of_vars_table,type_fun)
				continue

			print instruction

	def checkCallStmt(self,instruction,vars_table):
		instruction.getType(vars_table)

	def checkReturnStmt(self,instruction,vars_table,type_fun):
		return_type = instruction.getType(vars_table)
		if return_type != type_fun:
			raise TypeError("ERROR return type not match function type " + return_type +" "+ type_fun) 

	def checkAssignStmt(self,instruction,vars_table):
		name = instruction.getName()
		instruction_type = instruction.getType(vars_table)
		if name in vars_table.keys():
			existing_type = vars_table[name]
			if existing_type != instruction_type:
				raise TypeError("Error "+ name + " already exists and has type " + existing_type +" not " + instruction_type)
		else:
			vars_table[name] = instruction_type

	def checkConditionStatment(self,instruction,vars_table,type_fun):
		conditionType = instruction.getCondition().getType(vars_table)
		if not conditionType == 'Bool':
			raise TypeError("Error statement condition must be a bool")
		blocks = instruction.getBlocks()
		for block in blocks:
			self.checkBlockFunction(block,type_fun,vars_table=vars_table)

	def checkVecAssing(self,instruction,vars_table):
		name = instruction.getName()
		if name in vars_table.keys():
			if vars_table[name] != 'Vec':
				raise TypeError("Error " + name + " is not a Vec") 
		else:
			raise NotDefinedError("Error the variable " + name + " must be already defined and be a vector")
				
		index = instruction.getIntExpression()
		if index.getType(vars_table) != 'Int': 
			raise TypeError("Error the index expression must be an integer")
				
		value = instruction.getValueExpression()
		if value.getType(vars_table) != 'Int': 
			raise TypeError("Error the value expression to save in a vec must be an integer")








