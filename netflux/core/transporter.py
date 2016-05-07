from microprocess import MicroProcess 
import utils

class Transporter(MicroProcess):
    def __init__(self, sourceComponent, sourcePort, 
            sinkComponent, sinkPort,name = 'noname',logit=True):
        super(Transporter,self).__init__()
        self.sourceComponent = sourceComponent
        self.sourcePort = sourcePort
        self.sinkComponents = [sinkComponent]
        self.sinkPorts = [sinkPort]
        self.name = name
        self.logit = logit
    
    def run(self):
        while 1:
            yield 1
            if self.sourceComponent.dataReady(self.sourcePort):
                self.log("/" + "=" * 70 + "\\")
                self.log(utils.COLOR.green + \
                    "Transporter <%s> receiving from %s <%s>" % \
                    ((self.name,self.sourceComponent,self.sourcePort)))
                d = self.sourceComponent.recv(self.sourcePort)
                for sinkComponent, sinkPort in zip(self.sinkComponents,
                        self.sinkPorts):
                    self.log(utils.COLOR.green + \
                        "Transporter <%s> sending to %s <%s>" % \
                        ((self.name,sinkComponent,sinkPort)))
                    sinkComponent.send(d, sinkPort)
                self.log("\\" + "=" * 70 + "/")
                self.log(utils.COLOR.white + "\r")

    def addSink(self, sinkComponent, sinkPort):
        self.sinkComponents.append(sinkComponent)
        self.sinkPorts.append(sinkPort)

    def log(self, str):
        if self.logit:
            print str

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Transporter <%s> " % self.name

