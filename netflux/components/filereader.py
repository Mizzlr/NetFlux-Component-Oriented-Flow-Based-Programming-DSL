from netflux.core.component import Component 
from netflux.core.scheduler import Scheduler
from netflux.core.executor  import Executor

class FileReader(Component):
	def __init__(self, name='noname'):
		super(FileReader, self).__init__(name=name)

	def run(self):
		while 1:
			yield 1
			if self.dataReady('in'):
				filename = str(self.recv('in'))
				try:
					file = open(filename,'rb')
					data = file.read()
					self.send(data,'out')
					file.close()
				except Exception, exc:
					self.error(exc)

if __name__ == '__main__':
	fr = FileReader()
	fr.send(__file__, 'in')
	fr.send("nosuchfile.txt",'in')
	fr.send('scheduler.py','in')
	executor = Executor(fr)
	executor.run()