# -*- coding: utf-8 -*-
#
# Calculates availabilities for fixed + for proportional assignments

from distavail import Service, ServiceSet

class FixedProportional:
	def __init__(self):
		pass

	def fixedproportional(self, services, target, mode, submode=None):
		if not submode or submode == "availability":
			services.sort(key=lambda s: s.availability)
		elif submode == "capacity":
			services.sort(key=lambda s: s.capacity)
		elif submode == "price":
			services.sort(key=lambda s: s.price, reverse=True)

		if mode == "fixed":
			for i in range(len(services)):
				services[i].redundant = 0
		elif mode == "proportional":
			for i in range(len(services)):
				# FIXME: this is not exactly corresponding to a true
				# staggered proportional distribution with equal+dontcare parts
				services[i].redundant = i
		else:
			return None

		k = len(services)

		ss = ServiceSet(services, debug=False)
		oav = ss.availability(k)

		return oav
