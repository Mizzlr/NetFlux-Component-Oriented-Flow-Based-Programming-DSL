import utils 

class Linker(object):
	def __init__(self, logit=True):
		super(Linker, self).__init__()
		self.logit = logit

	def link(self, graph):
		if type(graph) is dict and graph.has_key('transporters'):
			transporters = graph['transporters']
		else:
			transporters = graph
			graph = {'transporters': transporters}

		graph['components'] = []

		for transporter in transporters:
			try:
				sourceComp, sourcePort, sinkComp, sinkPort = transporter
			except ValueError, ve:
				print "transporter: ", transporter
				exit()

			sourceComp.attachSink(sourcePort, sinkComp, sinkPort)
			self.log(transporter)
			if sourceComp not in graph['components']:
				graph['components'].append(sourceComp)
			if sinkComp not in graph['components']:
				graph['components'].append(sinkComp)

		return graph

	def log(self,transporter):
		if self.logit:
			print utils.COLOR.magenta,
			sourceComp, sourcePort, sinkComp, sinkPort = transporter
			print "\tLinkd: [%s [%s]] => [[%s] %s]" % \
				((sourceComp, sourcePort, sinkPort,sinkComp)),
			print utils.COLOR.white