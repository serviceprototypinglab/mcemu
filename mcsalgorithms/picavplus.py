# -*- coding: utf-8 -*-
#
# Experimental implementation of the PICav+ algorithm
# Will modify the service list in place and return the achieved overall characteristics
# availability, capacity and price

import sys
from distavail import Service, ServiceSet

class PICavPlus:
	def __init__(self, debug=False, internaldebug=False, debugout=False):
		self.debug = debug
		self.internaldebug = internaldebug
		self.debugout = debugout
		self.logtext = ""

	def log(self, s):
		if self.debug:
			if self.debugout:
				print "»", s
			self.logtext += "» " + str(s) + "\n"

	def getlog(self):
		return self.logtext

	def picavplus(self, services, submode):
		self.log("Services:")
		self.log(str(services))

		if not submode or submode == "availability":
			services.sort(key=lambda s: s.availability)
		elif submode == "capacity":
			services.sort(key=lambda s: s.capacity)
		elif submode == "price":
			services.sort(key=lambda s: s.price, reverse=True)

		self.log("Ordered services:")
		self.log(str(services))

		gi = (services[0].availability, services[-1].availability)

		self.log("Global availability interval:")
		self.log(gi)

		return None
