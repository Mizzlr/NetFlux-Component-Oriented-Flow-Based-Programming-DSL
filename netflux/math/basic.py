from netflux.core.components import ComponentBuilder

def add(op1, op2):
	return op1 + op2

def sub(op1, op2):
	return op1 - op2

def mult(op1, op2):
	return op1 * op2

def div(op1, op2):
	return op1 / op2

Adder = ComponentBuilder.build(add, inports = ['op1','op2'], name="Adder")
Subtractor = ComponentBuilder.build(add, inports = ['op1','op2'], name="Subtractor")
Multiplier = ComponentBuilder.build(add, inports = ['op1','op2'], name="Multiplier")
Divider = ComponentBuilder.build(add, inports = ['op1','op2'], name="Divider")