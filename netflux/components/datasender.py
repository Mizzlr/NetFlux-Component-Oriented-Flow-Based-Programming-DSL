from netflux.core.component import Component 
from netflux.core.scheduler import Scheduler
from netflux.core.executor  import Executor

class DataSender(Component):
    def __init__(self, data, name='noname', logit=True):
        super(DataSender, self).__init__(name=name, logit=logit)
        self.send(data,'in')

    def run(self):
        while 1:
            yield 1
            if self.dataReady('in'):
                data = self.recv('in')
                self.send(data,'out')

if __name__ == '__main__':

    dataSender = DataSender({"some":"Data"})
    scheduler = Scheduler(ticks = 10)
    scheduler.activate(dataSender)

    executor = Executor(scheduler)
    executor.run()
