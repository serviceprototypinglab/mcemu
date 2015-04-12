#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from mcsalgorithms.staggered import Staggered
from mcsalgorithms.distavail import Service

CSV = True

cap = [10, 40, 92, 120]
av = [0.96, 0.3, 0.99, 0.98]

d1 = Service("D1", availability=av[0], capacity=cap[0])
d2 = Service("D2", availability=av[1], capacity=cap[1])
d3 = Service("D3", availability=av[2], capacity=cap[2])
d4 = Service("D4", availability=av[3], capacity=cap[3])
services = [d1, d2, d3, d4]

print "# min-availability,min-capacity,#results"
for av in range(80, 100+1):
	minav = av / 100.0
	for mincap in range(100, 260+1, 10):
		staggered = Staggered(debug=True, debugout=not CSV)
		distributions = staggered.staggered(services, minav, mincap, shortlist=False)
		print "%3.4f,%i,%i" % (minav, mincap, len(distributions))
