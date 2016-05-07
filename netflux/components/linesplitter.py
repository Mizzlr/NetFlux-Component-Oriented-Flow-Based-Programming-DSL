from netflux.core.component import Component 
from netflux.core.scheduler import Scheduler
from netflux.core.executor  import Executor

class LineSplitter(Component):
    def __init__(self, name='noname'):
        super(LineSplitter, self).__init__(name=name)
        
    def run(self):
        while 1:
            yield 1
            if self.dataReady('in'):
                lines = self.recv('in').split('\n')
                for line in lines:
                    self.send(line, "out")


		