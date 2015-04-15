#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Syntax: calc-distribution.py <inifile>|generated <min-availability/0> <min-capacity/0> <max-price/-1> <max-runtime/-1> <algorithm>
# Algorithms: fixed|proportional|picav|picav+|combinatory|staggered|all

import sys
import time

from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator
from mcsalgorithms.fixedproportional import FixedProportional
from mcsalgorithms.combinatory import Combinatory
from mcsalgorithms.picav import PICav
from mcsalgorithms.picavplus import PICavPlus
from mcsalgorithms.staggered import Staggered

def calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, mode, submode, debug):
	t_start = time.time()

	bestprice = None

	for service in services:
		service.redundant = 0

	if mode in ("fixed", "proportional"):
		fp = FixedProportional(debug=debug, debugout=True)
		oav = fp.fixedproportional(services, targetavailability, mode, submode)
	elif mode == "picav":
		picav = PICav(debug=debug, debugout=True)
		oav = picav.picav(services, targetavailability)
	elif mode == "picav+":
		picavplus = PICavPlus(debug=debug, debugout=True)
		oav = picavplus.picavplus(services, submode)
	elif mode == "combinatory":
		combinatory = Combinatory(debug=debug, debugout=True)
		bestprice, firsttime, firstprice, bests, bestk, bestoav = combinatory.combinatory(services, targetavailability, targetcapacity, targetprice, maxruntime)
		oav = bestoav
	elif mode == "staggered":
		staggered = Staggered(debug=debug, debugout=True)
		if not submode or submode == "plain":
			distributions = staggered.staggered(services, targetavailability, targetcapacity, targetprice, shortlist=True)
		else:
			distributions = staggered.staggeredcombinatoric(services, targetavailability, targetcapacity, targetprice, shortlist=True)
		oav = None
		if len(distributions) >= 1:
			oav = distributions[distributions.keys()[0]][1]
			bestprice = sum([s.price for s in distributions[distributions.keys()[0]][0][0][0]])
	else:
		return

	t_stop = time.time()

	t_diff = (t_stop - t_start) * 1000.0

	if oav and oav >= targetavailability:
		if bestprice:
			price = bestprice
		else:
			price = sum([s.price for s in services])
		if targetprice == -1 or price <= targetprice:
			overhead = float(len(services) + sum([s.redundant for s in services])) / len(services) - 1.0
			result = "availability=%3.4f price=%3.2f capacity-overhead=%3.2f" % (oav, price, overhead)
		else:
			result = "error, no solution found; discarding price=%3.2f" % price
	else:
		if not oav:
			oav = "(none)"
		else:
			oav = "%3.4f" % oav
		result = "error, no solution found; discarding availability=%s" % oav
	submodestr = "    "
	if submode:
		submodestr = "[%s]" % submode[0:2]
	dist = ""
	for service in services:
		if dist != "":
			dist += ","
		if service.redundant > 0 and service.redundant < 1:
			dist += "1+x"
		else:
			dist += "1+%i" % service.redundant
	print "Distribution [algorithm: %12s%3s time:%8.2f]: {%s} %s" % (mode, submodestr, t_diff, dist, result)

if len(sys.argv) != 7:
	print >>sys.stderr, "Multi cloud storage fragment distribution determination tool"
	print >>sys.stderr, "Syntax: %s <inifile>|generated <min-availability/0> <min-capacity/0> <max-price/-1> <max-runtime/-1> <algorithm>" % sys.argv[0]
	print >>sys.stderr, "Algorithms: fixed|proportional|combinatory|staggered|picav|picav+|all"
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

if mode in ("fixed", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "fixed", None, debug)
if mode in ("proportional", "all"):
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "proportional", "availability", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "proportional", "capacity", debug)
	calculatedistribution(services, targetavailability, targetcapacity, targetprice, maxruntime, "proportional", "price", debug)
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
