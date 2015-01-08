#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See combinatory.py for details
# Syntax: redundancycombinations.py <inifile>

import sys
import time

sys.path.append("..")
from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator
from mcsalgorithms.combinatory import Combinatory

services = []

#print "# services: %s" % str(services)
print "# numservices[h],target(%),services[n],significant[k],overhead(%),avail(%),bestprice,time(ms),firstprice,firsttime(ms)"

sg = ServiceGenerator()
if len(sys.argv) == 2:
	xservices = sg.loadservices(sys.argv[1])
else:
	xservices = sg.genservices(10)

combinatory = Combinatory()

for xservice in xservices:
	services.append(xservice)

	for xtarget in range(900, 1000, 10):
		target = xtarget / 1000.0

		t_start = time.time()
		bestprice, firsttime, firstprice, bests, bestk, bestoav = combinatory.combinatory(services, target)
		t_stop = time.time()

		t_diff = (t_stop - t_start) * 1000.0

		if not bestprice:
			bestprice = 0.0
			firsttime = 0.0
			firstprice = 0.0
			overhead = 0.0
		else:
			firsttime = (firsttime - t_start) * 1000.0
			overhead = float(bests) / bestk - 1.0

		print "%i,%3.4f,%i,%i,%3.2f,%3.4f,%3.2f,%3.2f,%3.2f,%3.2f" % (len(services), target, bests, bestk, overhead, bestoav, bestprice, t_diff, firstprice, firsttime)
