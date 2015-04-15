# -*- coding: utf-8 -*-
#
# Calculates the overall availability of data which is split into k shares
# k=1: *replicated* data, i.e. >= 1 service needs to be available,
# or k>1: *dispersed* data with/without redundancy, i.e. k/k-m (m<k?) needs to be available

import itertools
import random

class Service:
	def __init__(self, name, availability=1.0, redundant=0, price=0, capacity=0):
		self.name = name
		self.availability = availability
		self.redundant = redundant
		self.price = price
		self.capacity = capacity

	def __repr__(self):
		return "S[%s:av=%3.4f,r=%i,p=%3.2f,c=%i]" % (self.name, self.availability, self.redundant, self.price, self.capacity)

class ServiceSet:
	def __init__(self, services, debug=True, debugout=True):
		self.services = services
		self.debug = debug
		self.debugout = debugout
		self.logtext = ""

	def availabilitymontecarlo(self, k=1):
		numservices = len(self.services)

		# 50% redundancy assumed; n=k*1.5
		for i, service in enumerate(self.services):
			#service.redundant = i % 2
			service.redundant = 0

		om = len(self.services)
		probs = []

		for om in range(1, 2 ** numservices + 1):
			for trial in range(10):
				samples = []
				for i in range(om):
					sample = random.randint(0, 2 ** numservices - 1)
					samples.append(sample)

				prob = 0.0
				for sample in samples:
					#print "STATES:", sample
					for i in range(numservices):
						state = (sample & (1 << i)) >> i
						prob += (self.services[i].redundant + 1) * self.services[i].availability * state
						#print "//prob", prob, "@state", state
				prob /= numservices
				prob /= om
				probs.append(prob)

			meanprob = sum(probs) / len(probs)
			varianceprob = 0.0
			for prob in probs:
				varianceprob += (meanprob - prob) ** 2
			varianceprob /= len(probs)

			self.log("monte carlo samples (h/N=%i om=%i states=%i): %s => µ%3.4f/σ%3.4f" % (numservices, om, 2 ** numservices, str(samples), meanprob, varianceprob))

	def availability(self, k=1):
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
			for s in ss:
				av *= s.availability
				red += s.redundant
			for s in ts:
				av *= (1 - s.availability)
			if len(ss) >= k:
				accept = "x"
				oav += av
			elif len(ss) + red >= k:
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
