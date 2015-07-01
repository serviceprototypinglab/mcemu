import os
import subprocess

def check_output_remote(arglist):
	key = "spio_aws.pem"
	#account = "core@172.17.42.1"
	account = "core@52.24.97.44"
	home = os.getenv("HOME")
	return subprocess.check_output(["ssh", "-i", "%s/.ssh/%s" % (home, key), account] + arglist)

def get_docker_images():
	images = []
	output = check_output_remote(["docker", "images"])
	for line in output.split("\n"):
		try:
			image = line.split()[0]
			if not image.startswith("icclab"):
				continue
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
			if not image.startswith("icclab"):
				continue
			imagebase = image.split(":")[0]
			instances[instanceid] = imagebase
		except:
			pass
	return instances

def shutdown(image):
	instances = get_docker_instances()
	for instanceid in instances:
		imagebase = instances[instanceid]
		if imagebase == image:
			print "+++++ kill", imagebase, instanceid
			check_output_remote(["docker", "kill", instanceid])
	pass

def instantiate(image):
	#check_output_remote(["docker", "run", "-d", image])
	pass
