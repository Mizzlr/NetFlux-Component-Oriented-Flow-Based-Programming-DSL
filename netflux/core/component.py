from microprocess import MicroProcess
from transporter import Transporter
from flux import Flux
import utils

class Component(MicroProcess):
    def __init__(self,name='noname',logit=True):
        super(Component, self).__init__()
        self.ports = { "in" : [], "out": [] , "control": [], "error": []}
        self.pipes = []
        self.logit = logit
        self.name = name
    
    def send(self, value, outPortName):
        self.ports[outPortName].append(value)
        if self.logit:
            strVal = str(value)
            if len(strVal) > 50:
                strVal = "\n" + strVal[:40] + " ... <%d bytes>" % len(strVal)
            print utils.COLOR.blue,
            print '%s <%s> <%s> sent: %s' % \
                ((self.__class__.__name__, self.name, outPortName, strVal)),
            print utils.COLOR.white

    def recv(self, inPortName):
        result = self.ports[inPortName][0]
        if self.logit:
            strVal = str(result)
            if len(strVal) > 50:
                strVal = "\n" +  strVal[:40] + " ... <%d bytes>" % len(strVal)
            print utils.COLOR.yellow,
            print '%s <%s> <%s> recvd: %s' % \
                ((self.__class__.__name__, self.name, inPortName, strVal)),
            print utils.COLOR.white

        del self.ports[inPortName][0]
        return result
    
    def dataReady(self, inPortName):
        return len(self.ports[inPortName])

    def error(self, exc):
        print '\033[31m',
        print exc,
        print '\033[37m'
        self.send(exc, 'error')

    def attachSink(self, outPortName, sinkComponent, sinkInPortName):

        for index, pipe in enumerate(self.pipes):
            if outPortName == pipe.sourcePort:
                pipe.addSink(sinkComponent, sinkInPortName)
                self.pipes[index] = pipe
                break
        else:
            pipe = Transporter(self, outPortName, sinkComponent, sinkInPortName,
                name="%s:%s" % ((self.name,outPortName)), logit=self.logit)
            self.pipes.append(pipe)

    def __getitem__(self, port):
        return Flux(self, port)
        
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s <%s>" % ((self.__class__.__name__, self.name))


class ComponentBuilder(object):
    def __init__(self):
        super(ComponentBuilder, self).__init__()

    @classmethod
    def build(self, run, initDict={}, ports=[], name="NewComponent",
            logit=True, engineType='function', inports=['in'], outports=['out']):

        class NewComponent(Component):
            def __init__(self, name="noname", logit=logit):
                super(NewComponent, self).__init__(name=name,logit=logit)
                self.engineType = engineType
                self.inports = inports
                self.outports = outports

                for key,value in initDict.items():
                    setattr(self, key, value)
                for port in ports + inports + outports:
                    self.ports[port] = []

            def run(self):
                while 1:
                    yield 1
                    if self.engineType == 'function':
                        if all([self.dataReady(inport) 
                                for inport in self.inports]):
                            try:
                                datas = [self.recv(inport) 
                                        for inport in self.inports]
                                results = run(*datas)
                                if not hasattr(results, '__iter__'):
                                    results = (results,)
                                for result, outport in zip(results, self.outports):
                                    self.send(result, outport)
                            except Exception, e:
                                self.error(e)
                                self.send(e,'error')
                    else:
                        run(self)

        NewComponent.__name__ = name  
        return NewComponent

