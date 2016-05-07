from microprocess import MicroProcess
from component import Component 
import utils, sys

class Scheduler(Component):
    def __init__(self,logit=True, ticks = sys.maxint, name='noname'):
        super(Scheduler, self).__init__(name=name)
        self.active = []
        self.newqueue = []
        self.ports['control'] = []
        self.logit = logit
        self.ticks = ticks

    def run(self): 
        for _ in xrange(self.ticks):
            for current in self.active:
                try:
                    result = current[1].next()
                    if result is not -1:
                        self.newqueue.append(current)
                except StopIteration:
                    pass
                yield "[tick:%d] %s <%s>" % \
                    ((_,current[0].__class__.__name__,current[0].name,))

            if self.dataReady('control'):
                cmd, components = self.recv('control')
                if cmd == "activate":
                    for component in components:
                        self.activate(component)
                elif cmd == "deactivate":
                    for component in components:
                        self.deactivate(component)

            self.active = self.newqueue
            self.newqueue = []

    def activate(self, someprocess):
        self.log('\tSched:  activated %s <%s>' % \
            ((someprocess.__class__.__name__,someprocess.name )))
        microthread = (someprocess, someprocess.run())
        self.newqueue.append(microthread)
        for pipe in someprocess.pipes:
            microthread = (pipe, pipe.run())
            self.newqueue.append(microthread)
        
    def deactivate(self, someprocess):
        for index, elem in enumerate(self.active):
            if elem[0].name == someprocess.name and \
                elem[0].__class__.__name__ == someprocess.__class__.__name__:
                self.log('\tSched: deactivated %s <%s>' % \
                    ((someprocess.__class__.__name__,someprocess.name )))
                self.active.pop(index)

        for index, elem in enumerate(self.newqueue):
            if elem[0].name == someprocess.name and \
                elem[0].__class__.__name__ == someprocess.__class__.__name__:
                self.log('\tSched:  deactivated %s <%s>' % \
                    ((someprocess.__class__.__name__,someprocess.name )))
                self.newqueue.pop(index)

    def log(self, string):
        if self.logit:
            print utils.COLOR.magenta,
            print string,
            print utils.COLOR.white

    def __repr__(self):
        return " %s: \n\tactive: %s \n\tnewqueue: %s" % \
            ((self.__class__.__name__,str(self.active), str(self.newqueue)))