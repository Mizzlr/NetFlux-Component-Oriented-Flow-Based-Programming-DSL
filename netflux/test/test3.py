from netflux.math.adder import Adder
from netflux.math.multiplier import Multiplier
from netflux.components.datasender import DataSender

from netflux.core.scheduler import Scheduler 
from netflux.core.executor import Executor 
from netflux.core.linker import Linker

logit = True
multr1 = Multiplier(name="multr1", logit=logit)
multr2 = Multiplier(name="multr2", logit=logit)
adder1 = Adder(name="adder1", logit=logit)


data1 = DataSender(12, name="data1", logit=logit)
data2 = DataSender(23, name="data2", logit=logit)
data3 = DataSender(43, name="data3", logit=logit)
data4 = DataSender(21, name="data4", logit=logit)

graph = {
	'transporters': [
		(data1,'out',multr1,'op1'),
		(data2,'out',multr1,'op2'),
		(data3,'out',multr2,'op1'),
		(data4,'out',multr2,'op2'),
		(multr1,'out',adder1,'op1'),
		(multr2,'out',adder1,'op2')
	]
}

linker = Linker()
graph = linker.link(graph)

scheduler = Scheduler(ticks = 5, logit=logit)
executor = Executor(scheduler, logit=logit)
executor.schedule(graph)

executor.run()