# -*- coding: utf-8 -*-
#
# Experimental implementation of the PICav+ algorithm based on PICav and Staggered
# Will modify the service list in place and return the achieved overall characteristics
# availability, capacity and price; or rather:
# Returns a short list of staggered distributions which fulfil any combination of requirements

import sys
from distavail import Service, ServiceSet
import itertools
import time

class PICavPlus:
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

	def picavplus(self, services, submode, minav=0.0, mincap=0, maxprice=-1, shortlist=True, maxruntime=-1):
		inittime = time.time()

		powerset = itertools.chain.from_iterable(itertools.combinations(services, r) for r in range(0, len(services) + 1))
		combinatoricdistributionscandidates = []
		combinatoricdistributions = {}
		for serviceset in powerset:
			if len(serviceset) > 0:
				self.log("staggered set: %s" % str(serviceset))
				distributions = self.picavplusstaggered(serviceset, minav, mincap, maxprice, shortlist, maxruntime)
				self.log("staggered result: %s" % str(distributions))
				combinatoricdistributionscandidates += distributions.values()

				if maxruntime != -1:
					nowtime = time.time()
					if nowtime - inittime > maxruntime:
						self.log("runtime interruption enforced")
						break

		if shortlist:
			if len(combinatoricdistributionscandidates) == 1:
				combinatoricdistributions["default"] = combinatoricdistributionscandidates[0]
			else:
				for candidate in combinatoricdistributionscandidates:
					if not "capacity" in combinatoricdistributions or candidate[2] > combinatoricdistributions["capacity"][2]:
						combinatoricdistributions["capacity"] = candidate
					# FIXME: should be candidate[1]??? (also in staggered)
					if not "availability" in combinatoricdistributions or candidate[2] > combinatoricdistributions["availability"][1]:
						combinatoricdistributions["availability"] = candidate
			self.log("shortlisted staggered result: %s" % str(combinatoricdistributions))
		else:
			for candidate in combinatoricdistributionscandidates:
				combinatoricdistributions["CD%i" % len(combinatoricdistributions)] = candidate
			self.log("complete staggered result: %s" % str(combinatoricdistributions))

		return combinatoricdistributions

	def picavplusstaggered(self, services, minav=0.0, mincap=0, maxprice=-1, shortlist=True, maxruntime=-1):
		color_red = "\033[91m"
		color_green = "\033[92m"
		color_yellow = "\033[93m"
		color_reset = "\033[0m"

		services = list(services)
		distributions = {}
		sliceconfigurations = []
		allservices = []
		allav = 0.0
		allprice = 0.0
		allcap = 0

		dispslicetotal = 0
		while len(services) > 0:
			dispslice = min([s.capacity for s in services]) - dispslicetotal
			self.log("- dispslice %i over %i nodes" % (dispslice, len(services)))
			price = sum([s.price for s in services]) * dispslice * len(services)
			if maxprice != -1 and price > maxprice:
				return distributions

			slicedistribution = self.picavslice(services, minav, mincap, maxprice)
			if slicedistribution:
				k, av = slicedistribution
				cap = k * dispslice
				if cap == 0:
					cap = 10000
				self.log("  - k %i -> slice availability %3.4f effective slice capacity %i price %3.2f" % (k, av, cap, price))
				sliceconfigurations.append((av, cap, price, services, k))

			dispslicetotal += dispslice
			services = [s for s in services if s.capacity != dispslicetotal]
			if dispslice >= mincap:
				services = []

		# in staggered, config == dispslice
		for config in sliceconfigurations:
			av, cap, price, services, k = config
			allav += av * cap
			allprice += price
			allcap += cap
			allservices.append((services, k, cap))
		allav /= allcap
		allprice /= allcap

		distributions["picav"] = (allservices, allav, allcap)

		return distributions

	def picavslice(self, services, minav=0.0, mincap=0, maxprice=-1, submode="availability"):
		self.log("Slice services:")
		self.log(str(services))

		if not submode or submode == "availability":
			services.sort(key=lambda s: s.availability)
		elif submode == "capacity":
			services.sort(key=lambda s: s.capacity)
		elif submode == "price":
			services.sort(key=lambda s: s.price, reverse=True)

		self.log("Ordered slice services:")
		self.log(str(services))

		gi = (services[0].availability, services[-1].availability)

		self.log("Global availability interval:")
		self.log(gi)

		self.log("Iterative clustering:")

		##!!
		maxiterations = 100
		factor = 1

		for i in range(1, maxiterations + 1):
			self.log("(iteration:%i)" % i)
			intervals = []
			classes = []
			elements = 0

			for j in range(0, i):
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

			if oav > minav:
				return k, oav

		return None
