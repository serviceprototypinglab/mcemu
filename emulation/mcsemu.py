#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Emulates storage service availabilities with launch/shutdown control over FTP servers (gatling)
# Syntax: mcsemu.py <inifile>

import sys
import time
import random
import subprocess

sys.path.append("..")
from mcsalgorithms.distavail import Service, ServiceSet
from mcsalgorithms.servicegen import ServiceGenerator

if len(sys.argv) != 2:
	print "Syntax: mcsemu.py <inifile>"
	sys.exit(1)

class EmulatedService:
	def __init__(self, service, ftpport, httpport):
		self.service = service
		self.ftpport = ftpport
		self.httpport = httpport
		self.avonline = 1
		self.avoffline = 0
		self.process = None
		self.online = None
		self.startservice()

	def realav(self):
		realav = float(self.avonline) / (self.avonline + self.avoffline)
		return realav

	def __repr__(self):
		onlinestate = " x"[self.online]
		return "ES[%s:ftp:%i,http:%i,av=%3.4f,realav:%3.4f][%s]" % (self.service.name, self.ftpport, self.httpport, self.service.availability, self.realav(), onlinestate)

	def startservice(self):
		cmd = "gatling -n -S -p %i -fp %i" % (self.httpport, self.ftpport)
		self.process = subprocess.Popen(cmd.split(" "))
		print ">> %s -> %i" % (cmd, self.process.pid)
		self.online = True

	def stopservice(self):
		print ">> kill %i" % self.process.pid
		self.process.kill()
		self.process = None
		self.online = False

sg = ServiceGenerator()
services = sg.loadservices(sys.argv[1])

print "Services to emulate:"
print services

ftpport = 2000
httpport = 3000
emulatedservices = []
for service in services:
	emulatedservices.append(EmulatedService(service, ftpport, httpport))
	ftpport += 1
	httpport += 1

print "Emulated services:"
print emulatedservices

print "Emulation starts..."
inittime = int(time.time())
while True:
	time.sleep(1)

	for es in emulatedservices:
		if es.online:
			es.avonline += 1
		else:
			es.avoffline += 1

		avdiff = es.realav() - es.service.availability
		switchprobability = random.random()

		if es.online:
			if avdiff > 0 and abs(avdiff) > switchprobability:
				es.stopservice()
		elif not es.online:
			if avdiff < 0 and abs(avdiff) > switchprobability:
				es.startservice()

	print "* virtual time [%5i]: %s" % (int(time.time()) - inittime, emulatedservices)
