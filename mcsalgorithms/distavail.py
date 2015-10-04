# -*- coding: utf-8 -*-
#
# Calculates the overall availability of data which is split into k shares
# k=1: *replicated* data, i.e. >= 1 service needs to be available,
# or k>1: *dispersed* data with/without redundancy, i.e. k/k-m (m<k?) needs to be available
# Service.redundant: extra local redundancy, which increases availability but increasingly breaks secret sharing

import itertools
import random

class Service:
	def __init__(self, name, availability=1.0, redundant=0, price=0, capacity=0, properties={}):
		self.name = name
		self.fragment = 1
		self.redundant = redundant
		self.availability = availability
		self.price = price
		self.capacity = capacity

		self.properties = properties

	def reset(self):
		self.fragment = 1
		self.redundant = 0

	def __repr__(self):
		extraprops = ""
		for prop in self.properties.keys():
			extraprops += "," + prop + "=" + self.properties[prop]
		return "S[%s:f=%i/r=%i,av=%3.4f,p=%3.2f,c=%i%s]" % (self.name, self.fragment, self.redundant, self.availability, self.price, self.capacity, extraprops)

class ServiceSet:
	def __init__(self, services, debug=True, debugout=True):
		self.services = services
		self.debug = debug
		self.debugout = debugout
		self.logtext = ""

	def availability(self, k=1, mode="precise"):
		if not mode or mode == "precise":
			return self.availabilitypicav(k)
		elif mode == "approximated":
			return self.availabilitymontecarlo(k)

	def availabilitymontecarlo(self, k=1, epsilon=0.03, trials=20, om=None):
		numservices = len(self.services)

		if not om:
			om = len(self.services)
		probs = []

		while True:
			for trial in range(trials):
				samples = []
				for i in range(om):
					sample = 0
					for j in range(numservices):
						if random.random() < self.services[j].availability:
							sample += (1 << j)
					samples.append(sample)

				prob = 0
				for sample in samples:
					#print "STATES:", sample
					loadablefragments = 0
					for i in range(numservices):
						state = (sample & (1 << i)) >> i
						loadablefragments += (self.services[i].redundant + self.services[i].fragment) * state
						#print "//prob", prob, "@state", state
					if loadablefragments >= k:
						prob += 1
				prob = float(prob) / om
				probs.append(prob)

			meanprob = sum(probs) / len(probs)
			varianceprob = 0.0
			for prob in probs:
				varianceprob += (meanprob - prob) ** 2
			varianceprob /= len(probs)

			self.log("monte carlo samples (h/N=%i om=%i states=%i): %s => µ%3.4f/σ%3.4f" % (numservices, om, 2 ** numservices, str(samples), meanprob, varianceprob))

			if varianceprob < epsilon:
				self.log("found good approximation")
				return meanprob
			if om >= 2 ** numservices:
				self.log("no approximation found, bailing out")
				return 0
			om += 1

	def availabilitypicav(self, k=1):
		if k < 1:
			return

		services = set(self.services)
		powerset = itertools.chain.from_iterable(itertools.combinations(services, r) for r in range(0, len(services) + 1))

		oav = 0
		for i, s in zip(itertools.count(), powerset):
			ss = set(s)
			ts = services - ss
			av = 1
			red = 0
			#fragments = len(ss)
			fragments = 0
			for s in ss:
				av *= s.availability
				red += s.redundant
				fragments += s.fragment
			for s in ts:
				av *= (1 - s.availability)
			if fragments >= k:
				accept = "x"
				oav += av
			elif fragments + red >= k:
				accept = "R"
				oav += av
			else:
				accept = " "
			self.log("[%s] a%i: %3.4f / S: %s / T: %s" % (accept, i, av, str(ss), str(ts)))
		self.log("availability-sum: %3.4f" % oav)
		return oav

	def log(self, s):
		if self.debug:
			if self.debugout:
				print "#", s
			self.logtext+= "# " + s + "\n"

	def getlog(self):
		return self.logtext
