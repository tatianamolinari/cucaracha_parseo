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

class Function(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Function',children=children,leaf=leaf)

	def push(self,child):
		self.children.append(child)

class Program(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Program',children,leaf)

 	def push(self,child):
		self.children.append(child)

class Parameter(Node):
	def __init__(self,children=[],leaf=None):
		Node.__init__(self,'Parameter',children,leaf)

 	def push(self,child):
		self.children.append(child)

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




