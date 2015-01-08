#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See picav.py for details
# Syntax: picavcombinations.py <inifile>

import sys
import time

sys.path.append("..")
from mcsalgorithms.picav import PICav
from mcsalgorithms.distavail import Service
from mcsalgorithms.servicegen import ServiceGenerator

CSV = True

def picavfactors(services, target):
	global CSV

	picav = PICav(debug=False)
	for factor in range(1, 5):
		t_start = time.time()
		oav = picav.picav(services, target, maxiterations=15, factor=factor)
		t_stop = time.time()

		t_diff = (t_stop - t_start) * 1000

		if not oav:
			if not CSV:
				print "factor %i: ---" % factor
		else:
			if not CSV:
				m = sum(s.redundant for s in services)
				k = len(services) * factor
				print "factor %i: availability=%3.4f overhead=%3.2f" % (factor, oav, float(k + m) / k - 1.0)

		if CSV:
			if not oav:
				oav = 0.0
				m = 0
				k = 1
				price = 0.0
			else:
				m = sum(s.redundant for s in services)
				k = len(services) * factor
				price = sum([x.price for x in services])
			print "%i,%3.4f,%i,%i,%3.2f,%3.4f,%3.2f,%3.2f" % (len(services), target, factor, k, float(k + m) / k - 1.0, oav, price, t_diff)

services = []

if CSV:
	print "# numservices[h/n],target(%),factor,significant[k],overhead(%),avail(%),price,time(ms)"

sg = ServiceGenerator()
if len(sys.argv) == 2:
	xservices = sg.loadservices(sys.argv[1])
else:
	xservices = sg.genservices(10)

for xservice in xservices:
	services.append(xservice)

	for xtarget in range(900, 1000, 10):
		target = xtarget / 1000.0

		picavfactors(services, target)
