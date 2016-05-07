from netflux.core.component import Component 
from netflux.core.scheduler import Scheduler
from netflux.core.executor  import Executor

class IterableSender(Component):
    def __init__(self, name='noname'):
        super(IterableSender, self).__init__(name=name)

    def run(self):
        while 1:
            yield 1
            if self.dataReady('in'):
                iterable = self.recv('in')
                for elem in iterable:
                    self.send(elem,'out')

if __name__ == '__main__':
    iterableSender = IterableSender(range(19))
    scheduler = scheduler.Scheduler()
    scheduler.activate(iterableSender)

    executor = executor.Executor(scheduler)
    executor.run()