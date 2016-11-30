from node import *

class CucarachaCompiler:

	def __init__(self):		
		self.program = None
		self.cuca_assembler = "section .data\n" + "lli_format_string db '%lli'\n" + "section . text\n" + "global main\n" + "extern exit, putChar, printf\n\n"
		self.registers_name = ["rsi","rbx","rcx","rdx","r8","r9","r10","r11","r12","r13","r14","r15"]
		self.registers = {"rsi":True, "rbx":True, "rcx":True, 
						  "rdx":True, "r8":True, "r9":True, "r10":True, "r11":True, 
						  "r12":True, "r13":True, "r14":True, "r15":True}
		self.dicParametres = {}
		self.rax = True
		self.rdi = True
	
	def freeRegister(self,name):
		self.registers[name]=True


	def takeRegister(self):
		
		for k in self.registers_name:
			 if self.registers[k]:
				self.registers[k]=False
				return k



	def registerIsFree(self,r):
		return self.registers[r]	

	def cuca_compile(self, program):
		print self.takeRegister()
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
			dicParameters = {}
			#if self.isPrimitive(name):
			#	self.compile_primitives(name)	
			self.cuca_assembler = self.cuca_assembler + node.getAssembler(self)
			self.compileBlockFunction(node.getBlock(),parameters_with_index,dicParameters)
			self.cuca_assembler = self.cuca_assembler + "  ret\n\n"
		else: 
			for child in node.children:
				self.compile_functions(child)

	def compileBlockFunction(self, blockFunction,parameters_with_index,dicParameters):
		current_variable = 0

		for instruction in blockFunction.children:
			if instruction.isStmtAssign():
				self.compile_stmtAssign(instruction, current_variable,parameters_with_index,dicParameters)
			if instruction.isBinaryIntAritmeticExpression():
				self.compile_stmtAssign(instruction, current_variable,parameters_with_index,dicParameters)

	def compile_main(self):
		self.cuca_assembler = self.cuca_assembler + "main:\n" + "    call cuca_main\n" + "    mov rdi , 0\n" + "    call exit\n"

	def compile_stmtAssign(self, instruction, current_variable,parameters_with_index,dicParameters):
		self.cuca_assembler = self.cuca_assembler + instruction.getAssembler(self)
		if instruction.isParameter() or instruction.getName() in parameters_with_index.keys():
			dicParameters[instruction.getName()] = "[rbp + 8 *(" + str(parameters_with_index[instruction.getName()]) + "+ 1)]"
			self.cuca_assembler = self.cuca_assembler + "mov [rbp + 8 *(" + str(parameters_with_index[instruction.getName()]) + "+ 1)], rdi\n" 
		else:
			print instruction
			current_variable = current_variable + 1
			dicParameters[instruction.getName()] = "mov [rbp - 8 * " + str(current_variable) + "]"
			self.cuca_assembler = self.cuca_assembler + "mov [rbp - 8 * " + str(current_variable) + "], rdi\n"

	def isPrimitive(self, name):
		return name == "putChar" or name == "putNum"

	#def compile_primitives(self, name):
	#	if name == "putChar":