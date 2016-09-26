import sys, os
sys.path.insert(0,"../..")
from semantic_exceptions import *

class Node:

	def __init__(self,typeNode,children=None,leaf=None):
	  	self.typeNode = typeNode
	  	if children:
	  		self.children = children
	  	else:
	  		self.children = [ ]
	    	self.leaf = leaf

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

	def isReturnStmt(self):
		return False

	def isVecAssing(self):
		return False

	def getType(self,table={}):
		return None

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

	def getParametersTypes(self):
		params = []
		for child in self.children:
			if child.isParameter():
				params.append(child.getType())
		return params

	def isFunction(self):
		return True

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

class StmtAssign(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtAssign',children,leaf)

	def getName(self):
		return self.children[0].leaf

	def getType(self,table={}):
		return self.children[1].getType(table)

	def isStmtAssign(self):
		return True

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


class ConditionStmt(Node):
	
	def isCondtionStmt(self):
		return True

	def getCondition(self):
		return self.children[0]

	def getBlocks(self):
		return [self.children[1]]


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


class StmtReturn(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtReturn',children,leaf)

	def getType(self,table={}):
		return self.children[0].getType(table)

	def isReturnStmt(self):
		return True

class ExprVar(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVar',children,leaf)

	def __str__(self,level=0):
	  	ret = "  "*level+ "(" +str(self.typeNode)+"\n"
	  	ret = ret + "  "*(level+1)+self.leaf.leaf+"\n"
	  	ret = ret + "  "*(level)+ ")" +"\n"
	  	return ret

	def getType(self,table={}):
		name = self.leaf.leaf
		if name in table.keys():
			return table[name]
		else:
			raise NotDefinedError("ERROR " + name + " is not defined")

class ExprConstNum(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprConstNum',children,leaf)
	
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

class ExprVecMake(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecMake',children,leaf)

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
			indexType = self.children[1].getType()
			if indexType != 'Int':
				raise TypeError("Error. " + name + " parameter cant be " + indexType + " type")
			return 'Int'
		else:
			raise NotDefinedError("ERROR " + name + " vector is not defined")

class ExprCall(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprCall',children,leaf)

	def getName(self):
		return self.children[0].leaf

	def getParametersExpressions(self):
		params_expressions = self.children[1:]
		return params_expressions

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
		

class BinaryBooleanExpression(Node):
	def getType(self,table={}):
		if(self.children[0].getType(table) == "Bool" and self.children[1].getType(table) == "Bool"):
			return 'Bool'
		else:
			raise TypeError("ERROR expected two booleans")
			return None

class ExprAnd(BinaryBooleanExpression):
	def __init__(self,children=[],leaf=None):
		BinaryBooleanExpression.__init__(self,'ExprAnd',children,leaf)

class ExprOr(BinaryBooleanExpression):
	def __init__(self,children=[],leaf=None):
		BinaryBooleanExpression.__init__(self,'ExprOr',children,leaf)


class ExprNot(BinaryBooleanExpression):
	def __init__(self,children=[],leaf=None):
		BinaryBooleanExpression.__init__(self,'ExprNot',children,leaf)

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


class ExprLe(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprLe',children,leaf)

class ExprGe(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprGe',children,leaf)

class ExprLt(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprLt',children,leaf)

class ExprGt(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprGt',children,leaf)

class ExprEq(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprEq',children,leaf)

	def getType(self,table={}):
		return 'Bool'

class ExprNe(BinaryIntExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntExpression.__init__(self,'ExprNe',children,leaf)

	def getType(self,table={}):
		return 'Bool'

class BinaryIntAritmeticExpression(Node):
	def getType(self,table={}):
		if(self.children[0].getType(table) == "Int" and self.children[1].getType(table) == "Int"):
			return 'Int'
		else:
			raise TypeError("ERROR expected two integers")
			return None

class ExprAdd(BinaryIntAritmeticExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntAritmeticExpression.__init__(self,'ExprAdd',children,leaf)

class ExprSub(BinaryIntAritmeticExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntAritmeticExpression.__init__(self,'ExprSub',children,leaf)

class ExprMul(BinaryIntAritmeticExpression):
	def __init__(self,children=[],leaf=None):
		BinaryIntAritmeticExpression.__init__(self,'ExprMul',children,leaf)

















