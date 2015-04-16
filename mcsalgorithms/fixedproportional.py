# -*- coding: utf-8 -*-
#
# Calculates availabilities for fixed + proportional + absolute assignments
# (redundancy support only in fixed:replication, secret sharing only in fixed:splitting)

from distavail import Service, ServiceSet

class FixedProportional:
	def __init__(self, debug=False, debugout=False):
		self.debug = debug
		self.debugout = debugout
		self.logtext = ""

	def log(self, s):
		if self.debug:
			if self.debugout:
				print "»", s
			self.logtext += "» " + str(s) + "\n"

	def getlog(self):
		return self.logtext

	def fixedproportional(self, services, target, mode, submode=None):
		#multiplier = len(services) * 10
		multiplier = len(services)
		absservice = None

		if mode == "fixed":
			shares = [int(multiplier * 1.0 / len(services)) for s in services]
		elif mode == "proportional":
			if not submode or submode == "availability":
				services.sort(key=lambda s: s.availability)
				sumavailability = sum([s.availability for s in services])
				if sumavailability == 0:
					sumavailability = 1
				shares = [int(multiplier * float(s.availability) / sumavailability) for s in services]
			elif submode == "capacity":
				services.sort(key=lambda s: s.capacity)
				sumcapacity = sum([s.capacity for s in services])
				if sumcapacity == 0:
					sumcapacity = 1
				shares = [int(multiplier * float(s.capacity) / sumcapacity) for s in services]
			elif submode == "price":
				services.sort(key=lambda s: s.price, reverse=True)
				maxprice = services[0].price
				sumprice = sum([maxprice - s.price for s in services])
				if sumprice == 0:
					sumprice = 1
				shares = [int(multiplier * float(maxprice - s.price) / sumprice) for s in services]
		elif mode == "absolute":
			if not submode or submode == "availability":
				services.sort(key=lambda s: s.availability, reverse=True)
				absservice = services[0]
			elif submode == "capacity":
				services.sort(key=lambda s: s.capacity, reverse=True)
			elif submode == "price":
				services.sort(key=lambda s: s.price)
			absservice = services[0]
			shares = [len(services)] + [0] * (len(services) - 1)

		# FIXME: Should better account for proportionality of decimal places
		while sum(shares) < multiplier:
			self.log("Share adjustment +1")
			shares[-1] += 1
		while sum(shares) > multiplier:
			self.log("Share adjustment -1")
			shares[-1] -= 1

		self.log("Shares [%s/%s] = %s" % (mode, submode, str(shares)))

		k = len(services)

		if mode == "fixed":
			if submode == "replication":
				k = 1
				for service in services[1:]:
					service.fragment = 0
					service.redundant = 1
			else:
				for service in services:
					service.redundant = 0
		elif mode == "proportional":
			for i in range(len(services)):
				# Over- or underproportional distribution -- leads to less capacity overhead
				#services[i].redundant = i
				# Staggered proportional distribution with equal+dontcare parts
				services[i].fragment = shares[i]
				#services[i].redundant = shares[i]
		elif mode == "absolute":
			for service in services:
				service.fragment = 0
			absservice.fragment = len(services)
			#return absservice.availability
		else:
			return None

		ss = ServiceSet(services, debug=False)
		oav = ss.availability(k)

		return oav
