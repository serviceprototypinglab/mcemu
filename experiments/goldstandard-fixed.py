#!/usr/bin/env python
# -*- coding: utf-8 -*-

cap = [10, 40, 92, 120]
av = [0.96, 0.3, 0.99, 0.98]

color_red = "\033[91m"
color_green = "\033[92m"
color_yellow = "\033[93m"
color_reset = "\033[0m"

import itertools

import sys
sys.path.append("../mcsalgorithms")
from distavail import Service, ServiceSet

def log(s, debug=True):
	if debug:
		print(s)

def staggereddistribution(services, minav, mincap, debug=False, internaldebug=False):
	distributions = {}
	sliceconfigurations = []

	# Slice-wise availability calculation
	dispslicetotal = 0
	while len(services) > 0:
		dispslice = min([s.capacity for s in services]) - dispslicetotal
		log("- dispslice %i over %i nodes" % (dispslice, len(services)), debug)
		ss = ServiceSet(services, debug=internaldebug)
		sliceconfig = []
		for k in range(1, len(services) + 1):
			av = ss.availability(k)
			cap = k * dispslice
			log("  - k %i -> slice availability %3.4f effective slice capacity %i" % (k, av, cap), debug)
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
			if len(distributions) == 0:
				distributions["default"] = (allservices, allav, allcap)
			if allav > distributions["default"][1]:
				distributions["availability"] = (allservices, allav, allcap)
			if allcap > distributions["default"][2]:
				distributions["capacity"] = (allservices, allav, allcap)
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
		log(logstr, debug)

	if len(distributions) > 1:
		if not "capacity" in distributions:
			distributions["capacity"] = distributions["default"]
		if not "availability" in distributions:
			distributions["availability"] = distributions["default"]
		del distributions["default"]

	for variant in distributions.keys():
		log("%s%s -- av %3.4f / cap %i%s" % (color_yellow, variant, distributions[variant][1], distributions[variant][2], color_reset), debug)

	return distributions

minav = 0.90
mincap = 200

d1 = Service("D1", availability=av[0], capacity=cap[0])
d2 = Service("D2", availability=av[1], capacity=cap[1])
d3 = Service("D3", availability=av[2], capacity=cap[2])
d4 = Service("D4", availability=av[3], capacity=cap[3])
services = [d1, d2, d3, d4]

distributions = staggereddistribution(services, minav, mincap, debug=True)
print distributions
