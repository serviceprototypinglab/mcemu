#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Syntax: calc-distribution.py <inifile>|generated <min-availability/0> <min-capacity/0> <max-price/-1> <max-runtime/-1> <algorithm>
# Algorithms: fixed|proportional|absolute|random|picav|picav+|combinatory|staggered|all

import sys
import time

from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator
from mcsalgorithms.fixedproportional import FixedProportional
from mcsalgorithms.combinatory import Combinatory
from mcsalgorithms.picav import PICav
from mcsalgorithms.picavplus import PICavPlus
from mcsalgorithms.staggered import Staggered
from mcsalgorithms.randomtargets import Random

def calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, mode, submode, debug):
	t_start = time.time()

	color_red = "\033[91m"
	color_green = "\033[92m"
	color_yellow = "\033[93m"
	color_reset = "\033[0m"

	bestprice = None

	for service in services:
		service.reset()

	if mode in ("fixed", "proportional", "absolute"):
		fp = FixedProportional(debug=debug, debugout=True)
		oav = fp.fixedproportional(services, mode, submode)
	elif mode == "random":
		rt = Random(debug=debug, debugout=True)
		oav = rt.random(services)
	elif mode == "picav":
		picav = PICav(debug=debug, debugout=True)
		oav = picav.picav(services, targetavailability)
	elif mode == "picav+":
		picavplus = PICavPlus(debug=debug, debugout=True)
		distributions = picavplus.picavplus(services, submode, targetavailability, targetcapacity, targetprice, shortlist=True, maxruntime=maxruntime)

		oav = None
		if len(distributions) >= 1:
			oav = distributions[distributions.keys()[0]][1]
			bestprice = sum([s.price for s in distributions[distributions.keys()[0]][0][0][0]])
			dist = distributions[distributions.keys()[0]][0][0][0]
			for service in services:
				if not service in dist:
					service.fragment = 0
	elif mode == "combinatory":
		combinatory = Combinatory(debug=debug, debugout=True)
		bestprice, firsttime, firstprice, bests, bestk, bestoav = combinatory.combinatory(services, targetavailability, targetcapacity, targetprice, maxruntime=maxruntime)
		oav = bestoav
	elif mode == "staggered":
		staggered = Staggered(debug=debug, debugout=True)
		if not submode or submode == "plain":
			distributions = staggered.staggered(services, targetavailability, targetcapacity, targetprice, shortlist=True, maxruntime=maxruntime)
		else:
			distributions = staggered.staggeredcombinatoric(services, targetavailability, targetcapacity, targetprice, shortlist=True, maxruntime=maxruntime)
		oav = None
		if len(distributions) >= 1:
			oav = distributions[distributions.keys()[0]][1]
			bestprice = sum([s.price for s in distributions[distributions.keys()[0]][0][0][0]])
			# Assign lowest staggered service configuration here because only the application chooses which distribution to use
			dist = distributions[distributions.keys()[0]][0][0][0]
			for service in services:
				if not service in dist:
					service.fragment = 0
	else:
		return

	t_stop = time.time()

	t_diff = (t_stop - t_start) * 1000.0

	services.sort(key=lambda s: s.name)

	color = color_reset
	if oav and oav >= targetavailability:
		if bestprice:
			price = bestprice
		else:
			price = sum([s.price for s in services if (s.fragment + s.redundant) > 0])
		if targetprice == -1 or price <= targetprice:
			epsilon = 10.0
			if maxruntime == -1 or t_diff < maxruntime * 1000 + epsilon:
				overhead = float(len(services) + sum([s.redundant for s in services])) / len(services) - 1.0
				result = "availability=%3.4f price=%3.2f capacity-overhead=%3.2f" % (oav, price, overhead)
				color = color_green
			else:
				result = "error, solution found but runtime exceeded by %3.2fs" % (t_diff / 1000.0 - maxruntime)
				color = color_yellow
		else:
			result = "error, no solution found; discarding price=%3.2f" % price
			color = color_red
	else:
		if not oav:
			oav = "(none)"
		else:
			oav = "%3.4f" % oav
		result = "error, no solution found; discarding availability=%s" % oav
		color = color_red
	submodestr = "    "
	if submode:
		submodestr = "[%s]" % submode[0:2]
	dist = ""
	for service in services:
		if dist != "":
			dist += ","
		if service.redundant > 0 and service.redundant < 1:
			dist += "%i+x" % service.fragment
		else:
			dist += "%i+%i" % (service.fragment, service.redundant)
	print "Distribution [algorithm: %s%12s%3s%s time:%8.2f]: {%s%s%s} %s%s%s" % (color, mode, submodestr, color_reset, t_diff, color, dist, color_reset, color, result, color_reset)

if len(sys.argv) != 7:
	print >>sys.stderr, "Multi cloud storage fragment distribution determination tool"
	print >>sys.stderr, "Syntax: %s <inifile>|generated <min-availability/0> <min-capacity/0> <max-price/-1> <max-runtime/-1> <algorithm>" % sys.argv[0]
	print >>sys.stderr, "Algorithms: fixed|proportional|absolute|random|combinatory|staggered|picav|picav+|all"
	sys.exit(1)

sg = ServiceGenerator()
if sys.argv[1] == "generated":
	services = sg.genservices(10)
else:
	services = sg.loadservices(sys.argv[1])

targetavailability = float(sys.argv[2])
if targetavailability > 1.0:
	targetavailability /= 100.0

targetcapacity = int(sys.argv[3])
targetprice = float(sys.argv[4])

maxruntime = float(sys.argv[5])

if targetavailability < 0 or targetavailability > 1.0 or targetcapacity < 0 or targetprice < -1 or maxruntime < -1:
	print >>sys.stderr, "Out of range: min-availability or min-capacity or max-price or max-runtime"
	sys.exit(1)

mode = sys.argv[6]

debug = True
if mode == "all":
	debug = False

services.sort(key=lambda s: s.name)
print "Services: %s" % ",".join([s.name for s in services])

if mode in ("fixed", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "fixed", "splitting", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "fixed", "replication", debug)
if mode in ("proportional", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "proportional", "availability", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "proportional", "capacity", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "proportional", "price", debug)
if mode in ("absolute", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "absolute", "availability", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "absolute", "capacity", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "absolute", "price", debug)
if mode in ("random", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "random", None, debug)
if mode in ("combinatory", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "combinatory", None, debug)
if mode in ("staggered", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "staggered", "plain", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "staggered", "combinatoric", debug)
if mode in ("picav", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "picav", None, debug)
if mode in ("picav+", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "picav+", "availability", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "picav+", "capacity", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "picav+", "price", debug)
