#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Checks parameters with which a Monte Carlo availability approximation works best

import sys
import time

sys.path.append("..")
from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator

sg = ServiceGenerator()
services = sg.loadservices("../simulations/goldstandardservices.ini")
#services = sg.loadservices("../simulations/tenservices.ini")

ss = ServiceSet(services, debug=False)
#preciseavs = {}
#approxavs = {}

for k in range(1, len(services) + 1):
	csv = open("mc%i.csv" % k, "w")
	print >>csv, "# epsilon,trials,avdiff (omega=n)"

	preciseav = ss.availabilitypicav(k=k)
	for epsilonint in range(1, 40, 4):
		epsilon = float(epsilonint) / 100
		for trials in range(10, 100, 10):
			approxav = ss.availabilitymontecarlo(k=k, epsilon=epsilon, trials=trials)
			#preciseavs[k] = preciseav
			#approxavs[k] = approxav
			avdiff = preciseav - approxav

			print >>csv, "%3.2f,%i,%3.4f" % (epsilon, trials, avdiff)
	csv.close()

for k in range(1, len(services) + 1):
	csv = open("mc%iom.csv" % k, "w")
	print >>csv, "# epsilon,omega-init,avdiff (trials=20)"

	preciseav = ss.availabilitypicav(k=k)
	for epsilonint in range(1, 40, 4):
		epsilon = float(epsilonint) / 100
		trials = 20
		for omega in range(2, 2 ** len(services), len(services)):
			approxav = ss.availabilitymontecarlo(k=k, epsilon=epsilon, trials=trials, om=omega)
			avdiff = preciseav - approxav

			print >>csv, "%3.2f,%i,%3.4f" % (epsilon, omega, avdiff)
	csv.close()
