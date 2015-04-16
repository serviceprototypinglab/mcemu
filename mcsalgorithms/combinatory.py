# -*- coding: utf-8 -*-
#
# Calculates availabilities for all sorts of service combinations...
# Trivial: k=1 if one service achieves target

import time
import itertools
import random
from distavail import Service, ServiceSet

class Combinatory:
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

	def combinatory(self, services, targetavailability, targetcapacity=0, targetprice=-1, maxruntime=-1):
		sservices = set(services)
		powerset = itertools.chain.from_iterable(itertools.combinations(services, r) for r in range(1, len(services) + 1))
		powersetlist = list(powerset)

		bestprice = None
		bests = 0
		bestk = 0
		bestoav = 0
		bestservices = None
		firstprice = None
		firsttime = None

		inittime = time.time()
		interrupted = False

		for s in powersetlist:
			for k in range(1, len(s) + 1):
				ss = ServiceSet(s, debug=self.internaldebug)
				oav = ss.availability(k)
				if oav >= targetavailability:
					##hit = len(s)
					price = sum([x.price for x in s])
					if not bestprice or price < bestprice:
						if targetprice == -1 or price < targetprice:
							if not bestprice:
								firstprice = price
								firsttime = time.time()
							bestprice = price
							bests = len(s)
							bestk = k
							bestoav = oav
							bestservices = s
							self.log("accept %s with k=%i" % (str(s), k))
						else:
							self.log("price too high %s" % str(s))
				else:
					self.log("availability too low %s" % str(s))
					##hit = 0
					price = 0
				#print "> %i,%i,%3.4f,%i,%3.2f" % (len(s), k, oav, hit, price)

				if maxruntime != -1:
					nowtime = time.time()
					if nowtime - inittime > maxruntime:
						interrupted = True
						self.log("runtime interruption enforced")
						break

			if interrupted:
				break

		if bestservices:
			counted = 0
			for service in services:
				if not service in bestservices:
					service.fragment = 0
				else:
					counted += 1
					if counted > bestk:
						service.fragment = 0
						service.redundant = 1

		return bestprice, firsttime, firstprice, bests, bestk, bestoav
