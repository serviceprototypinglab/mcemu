#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Syntax: calc-availability.py variances|availabilities|precise|approximated [<inifile>]
# See distavail.py for documentation

import sys
import time
import os

sys.path.append("..")
os.chdir(os.path.dirname(sys.argv[0]))

from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator

if len(sys.argv) == 1 or sys.argv[1] not in ("precise", "approximated", "variances", "availabilities"):
	print "Syntax: calc-availability.py [variances|availabilities|precise|approximated] [<inifile>]"
	sys.exit(1)

if sys.argv[1] in ("precise", "approximated"):
	if len(sys.argv) == 3:
		sg = ServiceGenerator()
		services = sg.loadservices(sys.argv[2])
	else:
		s1 = Service("a", availability=0.1)
		s2 = Service("b", availability=0.4)
		s3 = Service("c", availability=0.27)
		services = [s1, s2, s3]

	ss = ServiceSet(services, debug=True)
	results = {}
	oavs = {}

	for k in range(1, len(services) + 1):
		oav = ss.availability(k=k, mode=sys.argv[1])

		m = len(services) - k
		hint = ""
		if m == 0:
			hint = "/no replication"
		elif m == k * 0.5:
			hint = "/50% replication"
		elif m == k:
			hint = "/full replication"
		elif m == k * 2:
			hint = "/double replication"
		elif m == k * 3:
			hint = "/triple replication"

		approx = ""
		if sys.argv[1] == "approximated":
			approx = "~"

		results[k] = "[k=%i m=%i%20s]: %s%3.4f" % (k, m, hint, approx, oav)
		oavs[k] = oav

	print "Overall availability:"
	for k in range(1, len(services) + 1):
		print " %s" % results[k]

	#ss.availabilitymontecarlo(k=1)

	if len(sys.argv) == 2:
		if abs(oavs[1] - 0.6058) > 0.0001:
			print "Test failed!"

	sys.exit(0)

print "# services,meanav,devav,avail(%),time(µs)"

for meanav in range(0, 100 + 1, 10):
	for maxservices in range(1, 10 + 1):
		services = []
		meanavs = []

		if len(sys.argv) == 3:
			sg = ServiceGenerator()
			services = sg.loadservices(sys.argv[2])
			for s in services:
				meanavs.append(s.availability)
		else:
			for service in range(1, maxservices + 1):
				xmeanav = meanav
				if sys.argv[1] == "variances":
					xmeanav = 50.0 + (1, -1)[service % 2] * (meanav / 5.0)
					if xmeanav > 100.0:
						xmeanav = 100.0
					meanavs.append(xmeanav)
				s = Service("S" + str(service), availability=(xmeanav / 100.0))
				services.append(s)

		ss = ServiceSet(services, debug=False)

		xmeanav = meanav
		devav = 0.00
		if sys.argv[1] == "variances":
			xmeanav = sum(meanavs) / len(meanavs)
			for m in meanavs:
				devav += (m - xmeanav) ** 2
			devav /= len(meanavs)

		t_start = time.time()
		for i in range(1000):
			oav = ss.availability()
		t_stop = time.time()

		t_diff = (t_stop - t_start) * 1000.0

		print "%i,%3.2f,%3.2f,%3.4f,%3.2f" % (maxservices, xmeanav, devav, oav, t_diff)
