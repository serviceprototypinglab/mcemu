# -*- coding: utf-8 -*-
#
# Calculates availabilities for fixed + for proportional assignments

from distavail import Service, ServiceSet

class FixedProportional:
	def __init__(self):
		pass

	def fixedproportional(self, services, target, mode):
		services.sort(key=lambda s: s.availability)

		if mode == "fixed":
			for i in range(len(services)):
				services[i].redundant = 0
		elif mode == "proportional":
			for i in range(len(services)):
				services[i].redundant = i
		else:
			return None

		k = len(services)

		ss = ServiceSet(services, debug=False)
		oav = ss.availability(k)

		return oav
