# Setup environment variables:
# DOCKERKEY (SSH PEM file) and DOCKERHOST (e.g. core@localhost)

import os
import subprocess

def check_output_remote(arglist):
	runcommand = []
	dockerhost = os.getenv("DOCKERHOST")
	if dockerhost:
		runcommand = ["ssh"]
		dockerkey = os.getenv("DOCKERKEY")
		if dockerkey:
			runcommand += ["-i", dockerkey]
		runcommand += [dockerhost]
	return subprocess.check_output(runcommand + arglist)

def get_docker_images():
	images = []
	output = check_output_remote(["docker", "images"])
	for line in output.split("\n"):
		try:
			image = line.split()[0]
			#if not image.startswith("icclab"):
			#	continue
			images.append(image)
		except:
			pass
	return images

def get_docker_instances():
	instances = {}
	output = check_output_remote(["docker", "ps"])
	for line in output.split("\n"):
		try:
			instanceid = line.split()[0]
			image = line.split()[1]
			#if not image.startswith("icclab"):
			#	continue
			imagebase = image.split(":")[0]
			instances[instanceid] = imagebase
		except:
			pass
	return instances

def shutdown(image, output=True):
	instances = get_docker_instances()
	for instanceid in instances:
		imagebase = instances[instanceid]
		if imagebase == image:
			if output:
				print "+++++ kill", imagebase, instanceid
			check_output_remote(["docker", "kill", instanceid])
	pass

def instantiate(image, output=True):
	#check_output_remote(["docker", "run", "-d", image])
	# Note: If 'dynamite' is detected, instances are assumed to be running already, but otherwise they should be started
	pass
