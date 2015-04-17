# -*- coding: utf-8 -*-
#
# Light-weight implementation of the PICav algorithm
# Will modify the service list in place and return the achieved overall availability
# Factor > 1 will achieve a more fine-grained distribution at the expense of higher runtime

import sys
from distavail import Service, ServiceSet

class PICav:
	def __init__(self, debug=False, internaldebug=False, debugout=False, calcmode=None):
		self.debug = debug
		self.internaldebug = internaldebug
		self.debugout = debugout
		self.logtext = ""
		self.calcmode = calcmode

	def log(self, s):
		if self.debug:
			if self.debugout:
				print "»", s
			self.logtext += "» " + str(s) + "\n"

	def getlog(self):
		return self.logtext

	def picav(self, services, minavail, maxiterations=10, factor=1):
		self.log("Services:")
		self.log(str(services))

		services.sort(key=lambda s: s.availability)

		self.log("Ordered services:")
		self.log(str(services))

		gi = (services[0].availability, services[-1].availability)

		self.log("Global availability interval:")
		self.log(gi)

		self.log("Iterative clustering:")

		for i in range(1, maxiterations + 1):
			self.log("(iteration:%i)" % i)
			intervals = []
			classes = []
			elements = 0

			for j in range(0, i):
				# Slicing the services list will not consider variances
				#interval = services[j * len(services) / i:(j + 1) * len(services) / i]
				interval = (gi[0] + j * (gi[1] - gi[0]) / i, gi[0] + (j + 1) * (gi[1] - gi[0]) / i)
				intervals.append(interval)
				eps = 0.0001
				classes.append(filter(lambda s: s.availability > interval[0] - eps and s.availability < interval[1] + eps, services))
				if len(classes[-1]) > 0:
					elements += 1
					assignedelements = elements
					for s in classes[-1]:
						s.redundant = elements - 1
				else:
					assignedelements = 0
				self.log(" (interval:%i) %s {%i services} à %i elements" % (j, str(interval), len(classes[-1]), assignedelements))

			k = len(services) * factor
			m = sum(s.redundant for s in services)
			ss = ServiceSet(services, debug=self.internaldebug, debugout=self.debugout)
			oav = ss.availability(k=k, mode=self.calcmode)
			if self.internaldebug:
				self.logtext += ss.getlog()
			self.log(" (calculation) k=%i m=%i => availability=%3.2f" % (k, m, oav))

			if oav > minavail:
				return oav

		return None
