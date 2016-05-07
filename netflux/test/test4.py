import sys
from netflux.core.executor import Executor 
from netflux.components.datasender import DataSender 
from netflux.components.filereader import FileReader
from testComponents import Reverser, Concatenator, ConsoleDumper

dataSender = DataSender(sys.argv[1],name="fileNameSender")
fileReader = FileReader(name="fluxFileReader")
reverserComp = Reverser(name="reverser")
concatenatorComp = Concatenator(name="concatenator")
cosoledumperComp = ConsoleDumper(name="cosoledumper")

links = [
	(dataSender, 'out', fileReader, 'in'),
	(fileReader, 'out', reverserComp, 'in'),
	(fileReader, 'out', concatenatorComp, 'op1'),
	(reverserComp, 'out', concatenatorComp,'op2'),
	(concatenatorComp, 'out2', cosoledumperComp, 'in'),
]

executor = Executor(ticks=2)
executor.build(links)
executor.run()
