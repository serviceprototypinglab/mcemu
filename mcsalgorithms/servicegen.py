# Generates random services or loads a previous set of instances

import distavail
import random
#import iniparse
import ConfigParser
from distavail import Service

class ServiceGenerator:
	def __init__(self):
		pass

	def saveservices(self, services, filename):
		config = ConfigParser.ConfigParser()
		for s in services:
			config.add_section(s.name)
			config.set(s.name, "av", s.availability)
			config.set(s.name, "c", s.capacity)
			config.set(s.name, "p", s.price)
			for prop in s.properties.keys():
				config.set(s.name, prop, s.properties[prop])
		f = open(filename, "w")
		config.write(f)

	def loadservices(self, filename):
		services = []
		config = ConfigParser.ConfigParser()
		config.read(filename)
		sections = config.sections()
		for section in sections:
			av = config.getfloat(section, "av")
			try:
				c = config.getint(section, "c")
			except:
				c = 0
			try:
				p = config.getfloat(section, "p")
			except:
				p = 0.0
			if av > 1:
				av /= 100.0
			properties = {}
			items = config.items(section)
			for itemname, itemvalue in items:
				if itemname not in ("av", "c", "p"):
					properties[itemname] = itemvalue
			s = Service(section, availability=av, price=p, capacity=c, properties=properties)
			services.append(s)
		return services

	def genservices(self, num):
		services = []
		for i in range(num):
			av = random.random() / 10 + 0.9
			p = random.random() + av
			c = 0
			s = Service("s%i" % i, availability=av, price=p, capacity=c)
			services.append(s)
		return services
