USE components

DS := DataSender(
	['../components/component.py','nosuchfile.txt',
	'../components/datasender.py','../components/executor.py'])

ITS := IterableSender
FR 	:= FileReader
LS 	:= LineSplitter
WC 	:= WordCounter
TR 	:= Totaller

DS  [OUT] => [IN] ITS
ITS [OUT] => [IN] FR
FR  [OUT] => [IN] LS
LS  [OUT] => [IN] WC
WC  [OUT] => [IN] TR
