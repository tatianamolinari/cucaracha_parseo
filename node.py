import sys, os
sys.path.insert(0,"../..")
from semantic_exceptions import *
from collections import OrderedDict

class Node:

	def __init__(self,typeNode,children=None,leaf=None):
	  	self.typeNode = typeNode
	  	self.resultRegister = ""
	  	self.helper_register = "" 
	  	if children:
	  		self.children = children
	  	else:
	  		self.children = [ ]
	    	self.leaf = leaf

	def assemblerInstructionName(self):
		return ""

	def isExprVecMake(self):
		return False

	def isBinaryIntExpression(self):
		return True
	
	def isWhileStmt(self):
		return False

	def isFunction(self):
		return False

	def equals(self,something):
		return False

	def isBlock(self):
		return False

	def isStmtAssign(self):
		return False

	def isParameter(self):
		return False

	def isCondtionStmt(self):
		return False

	def isCallStmt(self):
		return False

	def isCallExpr(self):
		return False

	def isReturnStmt(self):
		return False

	def isVecAssing(self):
		return False

	def getType(self,table={}):
		return None

	def isBinaryIntAritmeticExpression(self):
		return False

	def getAssembler(self,complier):
		return ""

	def __str__(self, level=0):
		ret = "  "*level+ "(" +str(self.typeNode)+"\n"
	  	for child in self.children:
	  		ret += child.__str__(level+1)
	  	ret += "  "*level+ ") \n"
	  	return ret

	def __repr__(self):
		return self.typeNode + ' <tree node representation>'

class Id(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Id',children,leaf)

	def __str__(self,level=0):
	  	return "  "*level+str(self.leaf)+"\n"

	def getType(self,table={}):
		name = self.leaf
		if name in table.keys():
			return table[name]
		else:
			raise NotDefinedError("ERROR " + name + " is not defined")

class Type(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Type',children,leaf)

	def __str__(self,level=0):
	  	return "  "*level+str(self.leaf)+"\n"

	def equals(self,something):
		return self.leaf==something

	def getType(self,table={}):
		return self.leaf

class Function(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Function',children=children,leaf=leaf)

	def push(self,child):
		self.children.append(child)
		return self
	
	def getName(self):
		return self.children[0].leaf

	def getType(self,table={}):
		return self.children[1].getType(table)

	def getBlock(self):
		return self.children[-1]

	def getParameters(self):
		params = {}
		for child in self.children:
			if child.isParameter():
				params[child.children[0].leaf] = child.children[1].leaf
		return params

	def getParametersWithIndex(self):
		i = 0
		params = {}
		for child in self.children:
			if child.isParameter():
				i=i+1
				params[child.children[0].leaf] = i
		return params

	def getParametersTypes(self):
		params = []
		for child in self.children:
			if child.isParameter():
				params.append(child.getType())
		return params

	def isFunction(self):
		return True

	def getLocalVariables(self):
		localVariables = OrderedDict()
		self.getBlock().getLocalVariables(localVariables)
		for parameter in self.getParameters():
			if localVariables.get(parameter):
				localVariables.pop(parameter)
		return localVariables

	def getAssembler(self,compiler): 
		c_code = "cuca_" + self.getName() + ":\n" 
		c_code = c_code + "push rbp\n" + "mov rbp , rsp\n"
		cant_variables = len(self.getLocalVariables())
		if cant_variables != 0:
			c_code = c_code + "sub rsp, " + str(8*cant_variables) + "\n"
		
		return c_code

class Program(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Program',children,leaf)

 	def push(self,child):
		self.children = [child] + self.children
		return self

class Parameter(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Parameter',children,leaf)

	def getType(self,table={}):
		return self.children[1].getType(table)	

	def isParameter(self):
		return True

class Block(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Block',children,leaf)

	def isBlock(self):
		return True

	def getLocalVariables(self, localVariables={}):
		for inst in self.children:
			inst.getLocalVariables(localVariables)
		return localVariables


class StmtAssign(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtAssign',children,leaf)

	def getName(self):
		return self.children[0].leaf

	def getType(self,table={}):
		return self.children[1].getType(table)

	def isStmtAssign(self):
		return True

	def getLocalVariables(self, localVariables={}):
		localVariables[self.getName()] = self

	def getAssembler(self,compiler):
		return self.children[1].getAssembler(compiler)


class StmtVecAssign(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtVecAssign',children,leaf)

	def isVecAssign(self):
		return True

	def getName(self):
		return self.children[0].leaf

	def getIntExpression(self):
		return self.children[1]

	def getValueExpression(self):
		return self.children[1]

	def isVecAssing(self):
		return True

	def getLocalVariables(self, localVariables={}):
		sasa = "" #todo


class ConditionStmt(Node):

	
	def isCondtionStmt(self):
		return True

	def getCondition(self):
		return self.children[0]

	def getBlocks(self):
		return [self.children[1]]

	def getLocalVariables(self, localVariables={}):
		for block in self.getBlocks():
			block.getLocalVariables(localVariables)

class StmtIf(ConditionStmt):
	def __init__(self,children=[],leaf=None):
		ConditionStmt.__init__(self,'StmtIf',children,leaf)

class StmtIfElse(ConditionStmt):
	def __init__(self,children=[],leaf=None):
		ConditionStmt.__init__(self,'StmtIfElse',children,leaf)

	def getBlocks(self):
		return [self.children[1],self.children[2]]

class StmtWhile(ConditionStmt):
	def __init__(self,children=[],leaf=None):
		ConditionStmt.__init__(self,'StmtWhile',children,leaf)

	def isWhileStmt(self):
		return True

class StmtReturn(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtReturn',children,leaf)

	def getType(self,table={}):
		return self.children[0].getType(table)

	def isReturnStmt(self):
		return True

	def getLocalVariables(self, localVariables={}):
		return ""

class ExprVar(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVar',children,leaf)

	def __str__(self,level=0):
	  	ret = "  "*level+ "(" +str(self.typeNode)+"\n"
	  	ret = ret + "  "*(level+1)+self.leaf.leaf+"\n"
	  	ret = ret + "  "*(level)+ ")" +"\n"
	  	return ret

	def getAssembler(self, compiler):
		self.resultRegister = compiler.dicParameters[self.leaf.leaf]
		return ""

	def getType(self,table={}):
		name = self.leaf.leaf
		if name in table.keys():
			return table[name]
		else:
			raise NotDefinedError("ERROR " + name + " is not defined")

class ExprConstNum(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprConstNum',children,leaf)

	def getAssembler(self,compiler):
		register = compiler.takeRegister()
		self.resultRegister = register
		return "mov " + register + ", " + str(self.leaf) + "\n"

	
	def __str__(self,level=0):
	  	ret = "  "*level+ "(" +str(self.typeNode)+"\n"
	  	ret = ret + "  "*(level+1)+str(self.leaf)+"\n"
	  	ret = ret + "  "*(level)+ ")" +"\n"
	  	return ret

	def getType(self,table={}):
		return 'Int'

	  

class ExprConstBool(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprConstBool',children,leaf)
	
	def __str__(self,level=0):
	  	ret = "  "*level+ "(" +str(self.typeNode)+"\n"
	  	ret = ret + "  "*(level+1)+str(self.leaf)+"\n"
	  	ret = ret + "  "*(level)+ ")" +"\n"
	  	return ret

	def getType(self,table={}):
		return 'Bool'

	def getAssembler(self,compiler):
		register = compiler.takeRegister()
		self.resultRegister = register
		c_code = ""
		if self.leaf == "True":
			c_code = "mov " + register + ", " +"-1\n"
		else:
			c_code = "mov " + register + ", " +"0\n"
		return c_code

class ExprVecMake(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecMake',children,leaf)

	def isExprVecMake(self):
		return True

	def getElements(self):
		return self.children

	def getType(self,table={}):
		for exp in self.children:
			exp_type = exp.getType(table)
			if exp_type != 'Int':
				raise TypeError("ERROR vectors only supports int values")
		return 'Vec'

class ExprVecLength(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecLength',children,leaf)

	def __str__(self,level=0):
	  	ret = "  "*level+ "(" +str(self.typeNode)+"\n"
	  	ret = ret + "  "*(level+1)+str(self.leaf)+"\n"
	  	ret = ret + "  "*(level)+ ")" +"\n"
	  	return ret

	def getType(self,table={}):
		name = self.leaf
		if name in table.keys():
			if table[name] != 'Vec':
				raise TypeError("Error " + name + " must be a vect to express vector lenght by #name") 
			return 'Int'
		else:
			raise NotDefinedError("ERROR " + name + " vector is not defined")

class ExprVecDeref(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecDeref',children,leaf)

	def getType(self,table={}):
		name = self.children[0].leaf
		if name in table.keys():
			if table[name] != 'Vec':
				raise TypeError("Error " + name + " must be a vect to access values by index")
			indexType = self.children[1].getType(table)
			if indexType != 'Int':
				raise TypeError("Error. " + name + " parameter cant be " + indexType + " type")
			return 'Int'
		else:
			raise NotDefinedError("ERROR " + name + " vector is not defined")

class StmtCall(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtCall',children,leaf)

	def getName(self):
		return self.children[0].leaf

	def getParametersExpressions(self):
		params_expressions = self.children[1:]
		return params_expressions

	def getAssembler(self,compiler):
		paramters_expressions = self.getParametersExpressions()
		number_of_parameters = len(paramters_expressions)
		c_code = c_code + "sub rsp, " + str(number_of_parameters*8) + "\n"
		i = 0
		for exp in paramters_expressions:
			c_code = c_code + exp.getAssembler(compiler)
			register = exp.resultRegister
			if compiler.isRegister(register):
				compiler.freeRegister(register)
			else:
				aux_register = compiler.takeRegister()
				c_code = c_code + "mov " + aux_register +"," + register + "\n"
				register = aux_register
				compiler.freeRegister(register)

			c_code = c_code + "mov [ rsp + " +str(i*8)+"] ," + register + "\n"
			i=i+1
		c_code = c_code + "call_" + self.getName() + "\n"
		c_code = c_code + "add rsp, " + str(number_of_parameters*8) + "\n"
		c_code = c_code + "pop rbp \n"
		return c_code

	def isCallStmt(self):
		return True

	def getType(self,table={}):
		name = self.getName()
		if name in table.keys():
			function = table[name]
			function_params = function.getParametersTypes()
			params_expressions_call = self.getParametersExpressions()
			function_params_num = len(function_params)
			params_expressions_num = len(params_expressions_call)
			if function_params_num != params_expressions_num:
				raise TypeError("ERROR function " + name + " expected " + str(function_params_num) + " recived " + str(params_expressions_num) )
			for i in range(0, function_params_num):
				if function_params[i] != params_expressions_call[i].getType(table):
					raise TypeError("ERROR params type does not match")
			return function.getType(table)
		else:
			raise NotDefinedError("ERROR function " + name + " is not defined")

class ExprCall(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprCall',children,leaf)

	def getName(self):
		return self.children[0].leaf

	def getParametersExpressions(self):
		params_expressions = self.children[1:]
		return params_expressions

	def isCallExpr(self):
		return True

	def getAssembler(self,compiler):
		paramters_expressions = self.getParametersExpressions()
		number_of_parameters = len(paramters_expressions)
		c_code = ""
		if number_of_parameters>0:
			c_code = "sub rsp, " + str(number_of_parameters*8) + "\n"
			i = 0
			for exp in paramters_expressions:
				c_code = c_code + exp.getAssembler(compiler)
				register = exp.resultRegister
				if compiler.isRegister(register):
					compiler.freeRegister(register)
				else:
					aux_register = compiler.takeRegister()
					c_code = c_code + "mov " + aux_register +"," + register + "\n"
					register = aux_register
					compiler.freeRegister(register)
				c_code = c_code + "mov [ rsp + " +str(i*8)+"] ," + register + "\n"
				i=i+1
		c_code = c_code + "call cuca_" + self.getName() + "\n"
		if number_of_parameters>0:
			c_code = c_code + "add rsp, " + str(number_of_parameters*8) + "\n"
			#c_code = c_code + "pop rbp \n"
		return c_code

	def getType(self,table={}):
		name = self.getName()
		if name in table.keys():
			function = table[name]
			function_params = function.getParametersTypes()
			params_expressions_call = self.getParametersExpressions()
			function_params_num = len(function_params)
			params_expressions_num = len(params_expressions_call)
			if function_params_num != params_expressions_num:
				raise TypeError("ERROR function " + name + " expected " + str(function_params_num) + " recived " + str(params_expressions_num) )
			for i in range(0, function_params_num):
				if function_params[i] != params_expressions_call[i].getType(table):
					raise TypeError("ERROR params type does not match")
			return function.getType(table)
		else:
			raise NotDefinedError("ERROR function " + name + " is not defined")

	def getLocalVariables(self, localVariables={}):
		return ""

class BinaryBooleanExpression(Node):
	def getType(self,table={}):
		if(self.children[0].getType(table) == "Bool" and self.children[1].getType(table) == "Bool"):
			return 'Bool'
		else:
			raise TypeError("ERROR expected two booleans")
			return None

	def getAssembler(self,compiler):
		  
		assembler = self.children[0].getAssembler(compiler) + self.children[1].getAssembler(compiler)
		result1 = self.children[0].resultRegister
		result2 = self.children[1].resultRegister
		self.resultRegister=result1
		compiler.freeRegister(result2)
		return assembler + self.assemblerInstructionName() +" " + result1 + " , " + result2 + "\n"


class ExprAnd(BinaryBooleanExpression):
	def __init__(self,children=[],leaf=None):
		BinaryBooleanExpression.__init__(self,'ExprAnd',children,leaf)

	def assemblerInstructionName(self):
		return "and"

class ExprOr(BinaryBooleanExpression):
	def __init__(self,children=[],leaf=None):
		BinaryBooleanExpression.__init__(self,'ExprOr',children,leaf)
	
	def assemblerInstructionName(self):
		return "or"


class ExprNot(BinaryBooleanExpression):
	def __init__(self,children=[],leaf=None):
		BinaryBooleanExpression.__init__(self,'ExprNot',children,leaf)

	def assemblerInstructionName(self):
		return "not"

	def getAssembler(self,compiler):
		  
		assembler = self.children[0].getAssembler(compiler)
		result1 = self.children[0].resultRegister
		self.resultRegister=result1
		return assembler + self.assemblerInstructionName() +" " + result1 + "\n"

	def getType(self,table={}):
		if(self.children[0].getType(table) == "Bool"):
			return 'Bool'
		else:
			"ERROR"
			return None

class BinaryIntExpression(Node):
	def getType(self,table={}):
		if(self.children[0].getType(table) == "Int" and self.children[1].getType(table) == "Int"):
			return 'Bool'
		else:
			raise TypeError("ERROR expected two integers")
			return None
	def isBinaryIntExpression(self):
		return True

	def getAssembler(self,compiler):
		assembler = self.children[0].getAssembler(compiler) + self.children[1].getAssembler(compiler)
		result1 = self.children[0].resultRegister
		result2 = self.children[1].resultRegister
		self.resultRegister=result1
		compiler.freeRegister(result2)
		label1 = compiler.getNextLabel() 
		label2 = compiler.getNextLabel() 
		assembler = assembler + "cmp " + result1 + " , " + result2  + "\n" 
		assembler = assembler + self.assemblerInstructionName(compiler) + " " + label1 + "\n"
		register_cmp = compiler.takeRegister()
		assembler = assembler + "mov " + register_cmp + " , 0 \n"
		assembler = assembler + "jmp " + label2 + "\n"
		assembler = assembler + label1+" :\n"
		assembler = assembler + "mov " + register_cmp + " , -1 \n"
		assembler = assembler + label2+" :\n"
		self.helper_register = register_cmp
		return assembler


class ExprLe(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprLe',children,leaf)

	def assemblerInstructionName(self,compiler):
		return "jle "

class ExprGe(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprGe',children,leaf)
	
	def assemblerInstructionName(self,compiler):
		return "jge "

class ExprLt(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprLt',children,leaf)
	
	def assemblerInstructionName(self,compiler):
		return "jlt "

class ExprGt(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprGt',children,leaf)

	def assemblerInstructionName(self,compiler):
		return "gt "

class ExprEq(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprEq',children,leaf)

	def assemblerInstructionName(self,compiler):
		return "je "

	def getType(self,table={}):
		return 'Bool'

class ExprNe(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprNe',children,leaf)

	def assemblerInstructionName(self,compiler):
		return "jne "

	def getType(self,table={}):
		return 'Bool'

class BinaryIntAritmeticExpression(Node):
	def getType(self,table={}):
		if(self.children[0].getType(table) == "Int" and self.children[1].getType(table) == "Int"):
			return 'Int'
		else:
			raise TypeError("ERROR expected two integers")
			return None


	def getAssembler(self,compiler):
		  
		assembler = self.children[0].getAssembler(compiler) + self.children[1].getAssembler(compiler)
		result1 = self.children[0].resultRegister
		result2 = self.children[1].resultRegister
		self.resultRegister=result1
		compiler.freeRegister(result2)
		return assembler + self.assemblerInstructionName() +" " + result1 + " , " + result2 + "\n"

	def isBinaryIntAritmeticExpression(self):
		return True


class ExprAdd(BinaryIntAritmeticExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntAritmeticExpression.__init__(self,'ExprAdd',children,leaf)

	def assemblerInstructionName(self):
		return "add"

class ExprSub(BinaryIntAritmeticExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntAritmeticExpression.__init__(self,'ExprSub',children,leaf)

	def assemblerInstructionName(self):
		return "sub"

class ExprMul(BinaryIntAritmeticExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntAritmeticExpression.__init__(self,'ExprMul',children,leaf)

	def assemblerInstructionName(self):
		return "imul"

	def getAssembler(self,compiler):
		  
		assembler = self.children[0].getAssembler(compiler) + self.children[1].getAssembler(compiler)
		result1 = self.children[0].resultRegister
		result2 = self.children[1].resultRegister
		other_register = result2
		register = "rax"
		if not result1=="rax" and not result2=="rax":
			register = compiler.takeRegister("rax")
			assembler = assembler + "mov " + register + " , " + result1 + "\n"
			compiler.freeRegister(result1)
			self.children[0].resultRegister= register
		elif result2=="rax":
			other_register = result1
			register = result2
			compiler.freeRegister(result2)

		self.resultRegister=register
		compiler.freeRegister(other_register)
		return assembler + self.assemblerInstructionName() + " " + other_register + "\n"













