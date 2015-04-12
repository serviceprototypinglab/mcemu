# -*- coding: utf-8 -*-
#
# Experimental implementation of the Staggered algorithm
# Returns a short list of staggered distributions which fulfil any combination of requirements

import sys
from distavail import Service, ServiceSet
import itertools

class Staggered:
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

	def staggered(self, services, minav=0.0, mincap=0, shortlist=True):
		color_red = "\033[91m"
		color_green = "\033[92m"
		color_yellow = "\033[93m"
		color_reset = "\033[0m"

		distributions = {}
		sliceconfigurations = []

		# Slice-wise availability calculation
		dispslicetotal = 0
		while len(services) > 0:
			dispslice = min([s.capacity for s in services]) - dispslicetotal
			self.log("- dispslice %i over %i nodes" % (dispslice, len(services)))
			ss = ServiceSet(services, debug=self.internaldebug)
			sliceconfig = []
			for k in range(1, len(services) + 1):
				av = ss.availability(k)
				cap = k * dispslice
				if cap == 0:
					cap = 10000 # fake elastic scaling to unlimited capacity
				self.log("  - k %i -> slice availability %3.4f effective slice capacity %i" % (k, av, cap))
				sliceconfig.append((av, cap, services, k))
			sliceconfigurations.append(sliceconfig)
			dispslicetotal += dispslice
			services = [s for s in services if s.capacity != dispslicetotal]

		# Cartesian product over all slice configurations
		configurations = list(itertools.product(*sliceconfigurations))
		for config in configurations:
			allcap = 0
			allav = 0.0
			allservices = []
			allservicesreadable = []
			# Weighted availability over the slices of the configuration
			for dispslice in config:
				av, cap, services, k = dispslice
				allav += av * cap
				allcap += cap
				allservices.append((services, k))
				allservicesreadable.append(([s.name for s in services], k))
			allav /= allcap
			if allav >= minav and allcap >= mincap:
				rating = "%s%3s%s" % (color_green, "ok", color_reset)
				if shortlist:
					if len(distributions) == 0:
						distributions["default"] = (allservices, allav, allcap)
					if allav > distributions["default"][1]:
						distributions["availability"] = (allservices, allav, allcap)
					if allcap > distributions["default"][2]:
						distributions["capacity"] = (allservices, allav, allcap)
				else:
					distributions["D%i%3.4f" % (allcap, allav)] = (allservices, allav, allcap)
			else:
				rating = "%s%3s%s" % (color_red, "bad", color_reset)
			logstr = "=> {%s}" % rating
			if allav >= minav:
				color_av = color_green
			else:
				color_av = color_red
			logstr += " %savailability %3.4f%s" % (color_av, allav, color_reset)
			if allcap >= mincap:
				color_cap = color_green
			else:
				color_cap = color_red
			logstr += " %seffective capacity %i%s" % (color_cap, allcap, color_reset)
			logstr += " // %s" % str(allservicesreadable)
			self.log(logstr)

		if shortlist and len(distributions) > 1:
			if not "capacity" in distributions:
				distributions["capacity"] = distributions["default"]
			if not "availability" in distributions:
				distributions["availability"] = distributions["default"]
			del distributions["default"]

		for variant in distributions.keys():
			self.log("%s%s -- av %3.4f / cap %i%s" % (color_yellow, variant, distributions[variant][1], distributions[variant][2], color_reset))

		return distributions
