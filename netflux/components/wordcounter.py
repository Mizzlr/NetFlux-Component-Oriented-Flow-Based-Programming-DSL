from netflux.core.component import Component 
from netflux.core.scheduler import Scheduler
from netflux.core.executor  import Executor

class WordCounter(Component):
    def __init__(self, name='noname'):
        super(WordCounter, self).__init__(name=name)

    def run(self):
        while 1:
            yield 1
            if self.dataReady("in"):
                self.count = 0
                line = self.recv("in").strip()
                line = line.split(' ')
                line = sum(map(lambda x: x.split('\n'),line),[])
                line = sum(map(lambda x: x.split('\r'),line),[])
                line = sum(map(lambda x: x.split('\t'),line),[])
                line = [elem for elem in line if elem is not '']
                # print line,self.count
                self.count += len(line)
                self.send(self.count, "out")