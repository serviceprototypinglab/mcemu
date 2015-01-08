#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Syntax: calc-availability.py variances|availabilities|example [<inifile>]
# See distavail.py for documentation

import sys
import time

from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator

if len(sys.argv) == 1 or sys.argv[1] not in ("example", "variances", "availabilities"):
	print "Syntax: calc-availability.py [variances|availabilities|example] [<inifile>]"
	sys.exit(1)

if sys.argv[1] == "example":
	if len(sys.argv) == 3:
		sg = ServiceGenerator()
		services = sg.loadservices(sys.argv[2])
	else:
		s1 = Service("a", availability=0.1)
		s2 = Service("b", availability=0.4)
		s3 = Service("c", availability=0.27)
		services = [s1, s2, s3]

	ss = ServiceSet(services, debug=True)
	oav_tr = ss.availability(k=1)
	oav_hr = ss.availability(k=2)
	oav_sp = ss.availability(k=3)

	print "Overall availability:"
	print " [200%/triple replication k=1 m=2]:", oav_tr
	print " [50% replication, k=2 m=1]:", oav_hr
	print " [no replication, k=3]:", oav_sp
	if len(sys.argv) == 2:
		if abs(oav_tr - 0.6058) > 0.0001:
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
