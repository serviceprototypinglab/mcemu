# -*- coding: utf-8 -*-
#
# Calculates availabilities for all sorts of combinations...
# Trivial: k=1 if one service achieves target
# Syntax: redundancycombinations.py <inifile>

import time
import itertools
import random
from distavail import Service, ServiceSet

class Combinatory:
	def __init__(self):
		pass

	def combinatory(self, services, target):
		sservices = set(services)
		powerset = itertools.chain.from_iterable(itertools.combinations(services, r) for r in range(1, len(services) + 1))
		powersetlist = list(powerset)

		bestprice = None
		bests = 0
		bestk = 0
		bestoav = 0
		firstprice = None
		firsttime = None

		for s in powersetlist:
			for k in range(1, len(s) + 1):
				ss = ServiceSet(s, debug=False)
				oav = ss.availability(k)
				if oav >= target:
					hit = len(s)
					price = sum([x.price for x in s])
					if not bestprice or price < bestprice:
						if not bestprice:
							firstprice = price
							firsttime = time.time()
						bestprice = price
						bests = len(s)
						bestk = k
						bestoav = oav
				else:
					hit = 0
					price = 0
				#print "> %i,%i,%3.4f,%i,%3.2f" % (len(s), k, oav, hit, price)

		return bestprice, firsttime, firstprice, bests, bestk, bestoav
