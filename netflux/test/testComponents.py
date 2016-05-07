from netflux.core.component import ComponentBuilder

def reverser(string):
	return string[::-1]

def concatenator(this, that):
	return this + that

def cosoledumper(dump):
	print dump
	return dump

Reverser = ComponentBuilder.build(reverser, 
	name="Reverser")

Concatenator = ComponentBuilder.build(concatenator, 
	name="Concatenator",
	inports=['op1','op2'], outports=['out2'])

ConsoleDumper = ComponentBuilder.build(cosoledumper,
	name="CosoleDumper")