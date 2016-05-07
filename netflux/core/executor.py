from scheduler import Scheduler
from linker import Linker
import utils, sys

class Executor(object):
	def __init__(self, someprocess=None, logit=True, ticks=sys.maxint):
		super(Executor,self).__init__()
		if someprocess:
			self.process = someprocess
		else:
			if ticks < sys.maxint:
				ticks += 1
			self.process = Scheduler(ticks=ticks, name="")
		self.logit = logit
		self.linker = Linker()

	def schedule(self, components):
		if type(components) is not list:
			components = components['components']

		self.process.send(('activate',components), 'control')
	
	def kill(self, components):
		if type(components) is not list:
			components = components['components']

		self.process.send(('deactivate',components), 'control')

	def build(self, links):
		self.graph = self.linker.link(links)
		self.schedule(self.graph)

	def run(self):
		for _ in self.process.run():
			if self.logit:
				print utils.COLOR.cyan,
				print "\tExecd: ", _,
				print utils.COLOR.white

