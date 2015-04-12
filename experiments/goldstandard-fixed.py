#!/usr/bin/env python
# -*- coding: utf-8 -*-

cap = [10, 40, 92, 120]
av = [0.96, 0.3, 0.99, 0.98]

minav = 0.90
mincap = 200

#color_red = "\e[1m\e[31m"
#color_green = "\e[1m\e[32m"
#color_reset = "\e[0m\e[0m"

color_red = "\033[91m"
color_green = "\033[92m"
color_reset = "\033[0m"

#from operator import mul
import itertools

import sys
sys.path.append("../mcsalgorithms")
from distavail import Service, ServiceSet

#powerset = itertools.chain.from_iterable(itertools.combinations(av, r) for r in range(0, len(av) + 1))
#print powerset
#for i, s in zip(itertools.count(), powerset):
#	print "*", i, s

d1 = Service("D1", availability=av[0], capacity=cap[0])
d2 = Service("D2", availability=av[1], capacity=cap[1])
d3 = Service("D3", availability=av[2], capacity=cap[2])
d4 = Service("D4", availability=av[3], capacity=cap[3])
services = [d1, d2, d3, d4]

###
#ss = ServiceSet(services, debug=True, debugout=True)
#ss.availability(k=1) # m=3; 300% redundancy
#ss.availability(k=2) # m=2; 100% redundancy
#ss.availability(k=3) # m=1; 33% redundancy
#ss.availability(k=4) # m=0; no redundancy
###

sliceconfigurations = []

dispslicetotal = 0
while len(services) > 0:
	dispslice = min([s.capacity for s in services]) - dispslicetotal
	print "- dispslice", dispslice, "over", len(services), "nodes"
	ss = ServiceSet(services, debug=False)
	sliceconfig = []
	for k in range(1, len(services) + 1):
		av = ss.availability(k)
		cap = k * dispslice
		print "  - k", k, "-> slice availability", av, "effective slice capacity", cap
		sliceconfig.append((av, cap, services, k))
	sliceconfigurations.append(sliceconfig)
	dispslicetotal += dispslice
	services = [s for s in services if s.capacity != dispslicetotal]

# Cartesian product over all slice configurations
configurations = list(itertools.product(sliceconfigurations[0], sliceconfigurations[1], sliceconfigurations[2], sliceconfigurations[3]))
#print list(configurations)
for config in configurations:
	#print "*", config
	allcap = 0
	allav = 0.0
	allservices = []
	allservicesreadable = []
	for dispslice in config:
		av, cap, services, k = dispslice
		allav += av * cap
		allcap += cap
		allservices.append((services, k))
		allservicesreadable.append(([s.name for s in services], k))
	allav /= allcap
	if allav >= minav and allcap >= mincap:
		rating = "%s%3s%s" % (color_green, "ok", color_reset)
	else:
		rating = "%s%3s%s" % (color_red, "bad", color_reset)
	print "  => {%s}" % rating,
	if allav >= minav:
		color_av = color_green
	else:
		color_av = color_red
	print "%savailability %3.4f%s" % (color_av, allav, color_reset),
	if allcap >= mincap:
		color_cap = color_green
	else:
		color_cap = color_red
	print "%seffective capacity %i%s" % (color_cap, allcap, color_reset),
	print "//", allservicesreadable
