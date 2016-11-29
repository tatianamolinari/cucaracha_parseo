from node import *

class CucarachaCompiler:

	def __init__(self):		
		self.program = None
		self.cuca_assembler = "section .data\n" + "lli_format_string db '%lli'\n" + "section . text\n" + "global main\n" + "extern exit, putChar, printf\n\n"

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
			#if self.isPrimitive(name):
			#	self.compile_primitives(name)	
			self.cuca_assembler = self.cuca_assembler + node.getAssembler()
			self.compileBlockFunction(node.getBlock())
			self.cuca_assembler = self.cuca_assembler + "  ret\n\n"
		else: 
			for child in node.children:
				self.compile_functions(child)

	def compileBlockFunction(self, blockFunction):
		current_parameter = 0
		current_variable = 0
		for instruction in blockFunction.children:
			if instruction.isStmtAssign():
				self.compile_stmtAssign(instruction, current_parameter, current_variable)

	def compile_main(self):
		self.cuca_assembler = self.cuca_assembler + "main:\n" + "    call cuca_main\n" + "    mov rdi , 0\n" + "    call exit\n"

	def compile_stmtAssign(self, instruction, current_parameter, current_variable):
		self.cuca_assembler = self.cuca_assembler + instruction.getAssembler()
		if instruction.isParameter():
			current_parameter = current_parameter + 1
			self.cuca_assembler = self.cuca_assembler + "mov [rbp + 8 *(" + str(current_parameter) + "+ 1)], rdi\n" 
		else:
			current_variable = current_variable + 1
			self.cuca_assembler = self.cuca_assembler + "mov [rbp - 8 * " + str(current_variable) + "], rdi\n"

	def isPrimitive(self, name):
		return name == "putChar" or name == "putNum"

	#def compile_primitives(self, name):
	#	if name == "putChar":