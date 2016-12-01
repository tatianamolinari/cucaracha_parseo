from node import *

class CucarachaCompiler:

	def __init__(self):		
		self.program = None
		self.cuca_assembler = "section .data\n" + "lli_format_string db '%lli'\n" + "section . text\n" + "global main\n" + "extern exit, putChar, printf\n\n"
		self.registers_name = ["rsi","rbx","rcx","rdx","r8","r9","r10","r11","r12","r13","r14","r15"]
		self.registers = {"rsi":True, "rbx":True, "rcx":True, 
						  "rdx":True, "r8":True, "r9":True, "r10":True, "r11":True, 
						  "r12":True, "r13":True, "r14":True, "r15":True}
		self.dicParameters = {}
		self.local_variables = {}
		self.rax = True
		self.rdi = True
		self.current_label_index = 0
	
	def getNextLabel(self):
		self.current_label_index = self.current_label_index + 1
		return ".label_" + str(self.current_label_index)

	def freeRegister(self,name):
		if name=="rdi":
			self.rdi=True
		elif name=="rax":
			self.rax=True
		else:
			self.registers[name]=True


	def takeRegister(self, name=""):

		if name=="":
			if self.rdi:
				self.rdi=False
				return "rdi"
			
			for k in self.registers_name:
				 if self.registers[k]:
					self.registers[k]=False
					return k
		elif name=="rax" and self.rax:
			self.rax=False
			return "rax"
		elif name=="rax":
			return self.takeRegister()




	def registerIsFree(self,r):
		return self.registers[r]	

	def cuca_compile(self, program):
		print "------------------------------- Cucaracha Compiler ------------------------------- "
		self.program = program	
		try:
			self.compile_functions(program)
		except Error as e:
			print e
			return None

		self.compile_main()

		print self.cuca_assembler	

		print "-------------------------------------------------------------------------------------- "

	def compile_functions(self, node):
		if node.isFunction():
			name = node.getName()
			parameters_with_index = node.getParametersWithIndex()
			self.dicParameters = {}
			#if self.isPrimitive(name):
			#	self.compile_primitives(name)
			self.local_variables = node.getLocalVariables()
			self.cuca_assembler = self.cuca_assembler + node.getAssembler(self)
			self.compileBlockFunction(node.getBlock(),parameters_with_index)
			self.cuca_assembler = self.cuca_assembler + "  ret\n\n"
		else: 
			for child in node.children:
				self.compile_functions(child)

	def compileBlockFunction(self, blockFunction,parameters_with_index):
		current_variable = 0

		print "blockkkkkkkkkkkkkkkkkkkkk"
		for instruction in blockFunction.children:
			if instruction.isStmtAssign():
				self.compile_stmtAssign(instruction, parameters_with_index)
			if instruction.isCondtionStmt():
				self.compile_ConditionStmt(instruction, parameters_with_index)
			if instruction.isCallExpr():
				self.compile_callExpr(instruction, parameters_with_index)
			#if instruction.isBinaryIntAritmeticExpression():
			#	self.compile_BinaryIntAritmeticExpression(instruction, current_variable,parameters_with_index,dicParameters)

	def compile_main(self):
		self.cuca_assembler = self.cuca_assembler + "main:\n" + "    call cuca_main\n" + "    mov rdi , 0\n" + "    call exit\n"

	def compile_stmtAssign(self, instruction, parameters_with_index):
		self.cuca_assembler = self.cuca_assembler + instruction.getAssembler(self)
		register_result = instruction.children[1].resultRegister

		if instruction.getName() in parameters_with_index.keys():
			self.dicParameters[instruction.getName()] = "[rbp + 8 *(" + str(parameters_with_index[instruction.getName()]) + "+ 1)]"
			self.cuca_assembler = self.cuca_assembler + "mov [rbp + 8 *(" + str(parameters_with_index[instruction.getName()]) + "+ 1)], "+ register_result +"\n" 
		
		else:
			print "currrrrrrrrrrrrrrrrrrrrrrr "
			print self.local_variables[instruction.getName()]
			current_variable = 0
			current_variable = current_variable + 1
			self.dicParameters[instruction.getName()] = "[rbp - 8 * " + str(current_variable) + "]"
			self.cuca_assembler = self.cuca_assembler + "mov [rbp - 8 * " + str(current_variable) + "], "+ register_result +"\n"
		
		self.freeRegister(register_result)
	
	def compile_ConditionStmt(self, instruction, parameters_with_index):
		
		condition = instruction.getCondition()
		blocks = instruction.getBlocks()
		self.cuca_assembler = self.cuca_assembler + condition.getAssembler(self)
		label1 = self.getNextLabel()
		self.cuca_assembler = self.cuca_assembler + "cmp " + condition.resultRegister + " , 0 \n"
		self.cuca_assembler = self.cuca_assembler + "je " + label1 + ":\n"
		#assembler = assembler + blocks[0].getAssembler(self)
		self.compileBlockFunction(blocks[0],parameters_with_index)
		if len(blocks)==2:
			label2 = self.getNextLabel()
			self.cuca_assembler = self.cuca_assembler + "jmp" + label2 + ":\n"
			self.cuca_assembler = self.cuca_assembler + label1+" :\n"
			#assembler = assembler + blocks[1].getAssembler(self)
			self.compileBlockFunction(blocks[1],parameters_with_index)

		else:
			self.cuca_assembler = self.cuca_assembler + label1+" :\n"

	def compile_callExpr(self, instruction, parameters_with_index):
		if self.isPrimitive(instruction.getName()):
			self.compile_primitives(instruction)

	def isPrimitive(self, name):
		return name == "putChar" or name == "putNum"

	def compile_primitives(self, instruction):
		name = instruction.getName()
		list_parameters_expression = instruction.getParametersExpressions()
		for parameter_expression in list_parameters_expression:
			self.cuca_assembler = self.cuca_assembler + parameter_expression.getAssembler(self)
		if name == "putChar":
			self.cuca_assembler = self.cuca_assembler + "call putChar\n"
		if name == "putNum":
			current_result_register = list_parameters_expression[0].resultRegister
			self.freeRegister(current_result_register)
			if not(current_result_register == "rsi"):
				self.cuca_assembler = self.cuca_assembler + "mov rsi, " + current_result_register + "\n"
			self.cuca_assembler = self.cuca_assembler + "mov rdi , lli_format_string\n"
			self.cuca_assembler = self.cuca_assembler + "mov rax , 0\n"
			self.cuca_assembler = self.cuca_assembler + "call printf\n"