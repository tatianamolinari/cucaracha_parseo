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
	def __init__(self,children=None,leaf=None):
		Node.__init__(self,'Function',children=children,leaf=leaf)

	def push(self,child):
		self.children.append(child)

class Program(Node):
	def __init__(self):
		Node.__init__(self,'Program',children=[],leaf=None)

 	def push(self,child):
		self.children.append(child)

class Param(Node):
	def __init__(self):
		Node.__init__(self,'Param',children=[],leaf=None)

 	def push(self,child):
		self.children.append(child)

class Block(Node):
	def __init__(self):
		Node.__init__(self,'Block',children=[],leaf=None)