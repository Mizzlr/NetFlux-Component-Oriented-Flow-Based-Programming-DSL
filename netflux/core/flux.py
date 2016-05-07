class Flux(object):
	def __init__(self, component, port):
		super(Flux, self).__init__()
		self.component = component
		self.port = port

	def __rshift__(self, other):
		self.otherComp = other.component
		self.otherPort = other.port
		return self

	def __lshift__(self, other):
		other.otherComp = self.component
		other.otherPort = self.port
		return other

	def __getitem__(self, index):
		if index == 0:
			return self.component
		elif index == 1:
			return self.port
		elif index == 2:
			return self.otherComp
		elif index == 3:
			return self.otherPort
		else:
			raise StopIteration("Flux: invalid index %d" % index)

	def __or__(self, other):
		netflux = NetFlux(self)
		netflux = netflux | other
		return netflux


	def __repr__(self):
		if hasattr(self, 'otherComp') and hasattr(self, 'otherPort'):
			return "Flux(%s[%s] >> %s[%s])" % ((self.component.name,self.port,
				self.otherComp.name,self.otherPort))
		else:
			return "Flux(%s[%s])" % ((self.component.name,self.port))

class NetFlux(object):
	def __init__(self, flux):
		super(NetFlux, self).__init__()
		self.fluxes = [flux]

	def __or__(self,other):
		if isinstance(other, Flux):
			self.fluxes.append(other)
		else:
			self.fluxes.extend(other.fluxes)
		return self

	def __iter__(self):
		return iter(self.fluxes)

	def __repr__(self):
		return "NetFlux(%s)" % str(self.fluxes).replace(",","|")
