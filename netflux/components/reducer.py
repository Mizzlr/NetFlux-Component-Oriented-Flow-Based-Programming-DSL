from netflux.core.component import Component 
from netflux.core.scheduler import Scheduler
from netflux.core.executor  import Executor

class Reducer(Component):
	def __init__(self, reductionFunction, accumulator, name='noname'):
		super(Reducer, self).__init__(name=name)
		self.accumulator = accumulator
		self.reductionFunction = reductionFunction

	def run(self):
		while 1:
			yield 1
			if self.dataReady('in'):
				data = self.recv('in')
				self.accumulator = self.reductionFunction(data,
					self.accumulator) 
				self.send(self.accumulator,'out')

class Totaller(Component):
	def __init__(self, name='noname'):
		super(Totaller, self).__init__(name=name)
		self.accumulator = 0
		self.reductionFunction = lambda x,y: x + y 

	def run(self):
		while 1:
			yield 1
			if self.dataReady('in'):
				data = self.recv('in')
				self.accumulator = self.reductionFunction(data,
					self.accumulator) 
				self.send(self.accumulator,'out')