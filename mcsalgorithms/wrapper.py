# -*- coding: utf-8 -*-

from fixedproportional import FixedProportional
from combinatory import Combinatory
from picav import PICav
from picavplus import PICavPlus
from staggered import Staggered
from randomtargets import Random

class DistributionWrapper:
	def __init__(self):
		pass

	def assigndistribution(self, services, targetavailability, mode):
		if mode == "fixed" or mode == "fixed:splitting":
			ret = self.assign(services, targetavailability, "fixed", "splitting")
		elif mode == "fixed:replication":
			ret = self.assign(services, targetavailability, "fixed", "replication")
		elif mode == "proportional":
			ret = self.assign(services, targetavailability, "proportional", "availability")
		elif mode == "absolute":
			ret = self.assign(services, targetavailability, "absolute", "availability")
		elif mode == "random":
			ret = self.assign(services, targetavailability, "random", None)
		elif mode == "combinatory":
			ret = self.assign(services, targetavailability, "combinatory", None)
		elif mode == "staggered" or mode == "staggered:plain":
			ret = self.assign(services, targetavailability, "staggered", "plain")
		elif mode == "staggered:combinatoric":
			ret = self.assign(services, targetavailability, "staggered", "combinatoric")
		elif mode == "picav":
			ret = self.assign(services, targetavailability, "picav", None)
		elif mode == "picav+":
			ret = self.assign(services, targetavailability, "picav+", "availability")
		return ret

	def assign(self, services, targetavailability, mode, submode):
		for service in services:
			service.reset()

		if mode in ("fixed", "proportional", "absolute"):
			fp = FixedProportional()
			oav = fp.fixedproportional(services, mode, submode)
		elif mode == "random":
			rt = Random()
			oav = rt.random(services)
		elif mode == "picav":
			picav = PICav()
			oav = picav.picav(services, targetavailability)
		elif mode == "picav+":
			picavplus = PICavPlus()
			distributions = picavplus.picavplus(services, submode, targetavailability, 0, -1, shortlist=True)
			oav = None
			if len(distributions) >= 1:
				oav = distributions[distributions.keys()[0]][1]
				dist = distributions[distributions.keys()[0]][0][0][0]
				for service in services:
					if not service in dist:
						service.fragment = 0
		elif mode == "combinatory":
			combinatory = Combinatory()
			bestprice, firsttime, firstprice, bests, bestk, bestoav = combinatory.combinatory(services, targetavailability, 0, -1)
			oav = bestoav
		elif mode == "staggered":
			staggered = Staggered()
			if not submode or submode == "plain":
				distributions = staggered.staggered(services, targetavailability, 0, -1, shortlist=True)
			else:
				distributions = staggered.staggeredcombinatoric(services, targetavailability, 0, -1, shortlist=True)
			oav = None
			if len(distributions) >= 1:
				oav = distributions[distributions.keys()[0]][1]
				dist = distributions[distributions.keys()[0]][0][0][0]
				for service in services:
					if not service in dist:
						service.fragment = 0
		else:
			return

		services.sort(key=lambda s: s.name)

		if oav and oav >= targetavailability:
			return True
		else:
			return False
