from netflux.core.scheduler import Scheduler 
from netflux.core.executor import Executor
from netflux.core.linker import Linker 

from netflux.components.filereader import FileReader 
from netflux.components.wordcounter import WordCounter 
from netflux.components.datasender import DataSender
from netflux.components.linesplitter import LineSplitter
from netflux.components.iterablesender import IterableSender 
from netflux.components.reducer import Reducer, Totaller 


ds = DataSender(['../components/component.py','nosuchfile.txt',
	'../components/datasender.py','../components/executor.py'],name='DS')
its = IterableSender(name='ITS')
fr = FileReader(name='FR')
ls = LineSplitter(name='LS')
wc = WordCounter(name='WC')
tr = Totaller(name="TR")

graph = {
	"transporters": [
		(ds,  'out',	its, 	'in'),
		(its, 'out',	fr,		'in'),
		(fr,  'out',	ls,		'in'),
		(ls,  'out', 	wc,		'in'),
		(wc,  'out', 	tr,'in'),
	]
}

linker = Linker(logit=False)
graph = linker.link(graph)

scheduler = Scheduler(ticks = 100, logit=True)
executor = Executor(scheduler)

executor.schedule(graph)
executor.run()

