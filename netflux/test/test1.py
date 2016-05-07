from netflux.core.component import Component, ComponentBuilder
from netflux.core.transporter import Transporter
from netflux.core.scheduler import Scheduler 
from netflux.core.executor import Executor

class Producer(Component):
    def __init__(self, message, name="noname"):
        super(Producer,self).__init__(name=name)
        self.message = message
        self.ports['out2'] = []
    
    def run(self):
        while 1:
            yield 1
            self.send(self.message, "out2")

class Consumer(Component):
    def __init__(self, name="noname"):
        super(Consumer,self).__init__(name=name)

    def run(self, this=None):
        count = 0
        while 1:
            yield 1
            count += 1 # This is to show our data is changing :-)
            if self.dataReady("in"):
                data = self.recv("in")
                print data, count
                self.send(data,"out")

if __name__ == '__main__':
    
    cb = ComponentBuilder()

    def run(this):
        this.send(this.message, "out2")
    
    BuiltProducer = cb.build(run, 
        initDict= {"message":"hi there"},
        ports=["out2"], 
        name="BuiltProducer")
    
    def run2(this):
        if this.dataReady('in'):
            data = this.recv('in')
            this.mystring += data
            this.send(this.mystring, 'out')

    Concater = cb.build(run2,
        initDict={"mystring":''},
        name="Concater")


    bp = BuiltProducer(name="bp")
    p = Producer("Hello World",name='p')

    c1 = Consumer(name='c1')
    c2 = Consumer(name='c2')
    c3 = Concater(name='c3')
    
    bp.attachSink("out2",c1,"in")
    bp.attachSink("out2",c2,"in")
    c1.attachSink("out",c3,"in")
    c2.attachSink("out",c3,"in")

    scheduler = Scheduler(ticks=5)
    scheduler.activate(bp)
    scheduler.activate(c1)
    scheduler.activate(c2)
    scheduler.activate(c3)
    # scheduler.activate(t)

    executor = Executor(scheduler)
    executor.run()