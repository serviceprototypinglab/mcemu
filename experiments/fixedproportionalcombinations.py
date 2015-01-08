#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See fixedproportional.py for details
# Syntax: fixedproportionalcombinations.py <inifile> [fixed|proportional]

import sys
import time

sys.path.append("..")
from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator
from mcsalgorithms.fixedproportional import FixedProportional

MODE = "proportional" # fixed/proportional default

services = []

print "# numservices[h],target(%),significant[k],overhead(%),avail(%),price,time(ms)"

sg = ServiceGenerator()
if len(sys.argv) >= 2:
	xservices = sg.loadservices(sys.argv[1])
else:
	xservices = sg.genservices(10)

if len(sys.argv) == 3:
	MODE = sys.argv[2]

fp = FixedProportional()

for xservice in xservices:
	services.append(xservice)

	for xtarget in range(900, 1000, 10):
		target = xtarget / 1000.0

		t_start = time.time()
		oav = fp.fixedproportional(services, target, MODE)
		t_stop = time.time()

		t_diff = (t_stop - t_start) * 1000.0

		if oav >= target:
			price = sum([s.price for s in services])
			overhead = float(len(services) + sum([s.redundant for s in services])) / len(services) - 1.0
		else:
			price = 0.0
			overhead = 0.0

		k = len(services)

		print "%i,%3.4f,%i,%3.2f,%3.4f,%3.2f,%3.2f" % (len(services), target, k, overhead, oav, price, t_diff)
