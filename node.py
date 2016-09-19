import sys, os
sys.path.insert(0,"../..")

class Node:

	def __init__(self,typeNode,children=None,leaf=None):
	  	self.typeNode = typeNode
	  	if children:
	  		self.children = children
	  	else:
	  		self.children = [ ]
	    	self.leaf = leaf

	def __str__(self, level=0):
		ret = "\t"*level+ "(" +repr(self.typeNode)+"\n"
		#print self.typeNode
		#print self.children
	  	for child in self.children:
	  		#print child
	  		ret += child.__str__(level+1)
	  	return ret

	def __repr__(self):
		return self.typeNode + ' <tree node representation>'

class Id(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Id',children,leaf)

	def __str__(self,level=0):
	  	return "\t"*level+repr(self.leaf)+"\n"

class Type(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Type',children,leaf)

	def __str__(self,level=0):
	  	return "\t"*level+repr(self.leaf)+"\n"

class Function(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Function',children=children,leaf=leaf)

	def push(self,child):
		self.children.append(child)
		return self

class Program(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Program',children,leaf)

 	def push(self,child):
		self.children.append(child)
		return self

class Parameter(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Parameter',children,leaf)

 	def push(self,child):
		self.children.append(child)
		return self

class Block(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Block',children,leaf)

class StmtAssign(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtAssign',children,leaf)

class StmtVecAssign(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtVecAssign',children,leaf)

class StmtIf(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtIf',children,leaf)

class StmtIfElse(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtIfElse',children,leaf)

class StmtWhile(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtWhile',children,leaf)

class StmtReturn(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtReturn',children,leaf)

class StmtCall(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtCall',children,leaf)

class StmtAssign(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'StmtAssign',children,leaf)

class ExprVar(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVar',children,leaf)

class ExprConstNum(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprConstNum',children,leaf)
	
	def __str__(self,level):
	  	ret = "\t"*level+ "(" +repr(self.typeNode)+"\n"
	  	ret = ret + "\t"*(level+1)+repr(self.leaf)+"\n"
	  	ret = ret + "\t"*(level)+ ")" +"\n"
	  	return ret

class ExprConstBool(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprConstBool',children,leaf)

class ExprVecMake(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecMake',children,leaf)

class ExprVecLength(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecLength',children,leaf)

class ExprVecDeref(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprVecDeref',children,leaf)

class ExprCall(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprCall',children,leaf)

class ExprAnd(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprAnd',children,leaf)

class ExprOr(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprOr',children,leaf)

class ExprNot(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprNot',children,leaf)

class ExprLe(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprLe',children,leaf)

class ExprGe(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprGe',children,leaf)

class ExprLt(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprLt',children,leaf)

class ExprGt(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprGt',children,leaf)

class ExprEq(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprEq',children,leaf)

class ExprNe(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprNe',children,leaf)

class ExprAdd(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprAdd',children,leaf)

class ExprSub(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprSub',children,leaf)

class ExprMul(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'ExprMul',children,leaf)

















