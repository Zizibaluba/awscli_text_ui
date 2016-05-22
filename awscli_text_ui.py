import subprocess
import argparse
import re
import os
from pprint import pprint as fabprint

def awsListFiles():
	pass

def awsCopy(filename_list):
	pass

def awsPaste(filename_list):
	pass

def listAvailableProfile():
	pass

def awsProfileLocation(profile_location):
	profileList = {}
	os.chdir(profile_location)
	with open("credentials", "rU") as profile_file:
		i = 0 #Counter/Numbers for 
		for line in profile_file:

			credentialName = re.search("(?<=\[).*(?=\])", line)
			if credentialName:
				i += 1
				profileList(credentialName.group())
	fabprint(profileList)
	print #For readability
	return profileList

def helpFile():
	print "------Command List-------"
	print "copy [optional aws profile name] [source file] [optional destination]"
	print "cp == same as copy\n"
	print "listfile [optional aws profile name] [aws source]"
	print "ls == same as listfile"
	print "NOTE: If a previous listfile command is used, you can simply call it up from memory using listfile or ls\n"
	return

def missingProfile():
	print "Missing default profile. Please use [profile] to set new profile.\n"

def main():
	quit = ["q", "quit"]
	listFileCommand = ["listfile", "ls", "dir"]
	copyCommand = ["copy", "cp"]
	fileList = []
	profile = ""

	# Get current dir and print it so user knows what's initialized
	current_dir = os.getcwd()
	print "\nInitialized Directory:"
	print current_dir + "\n"

	# Argument parsing
	parser = argparse.ArgumentParser()
	parser.add_argument("--profile","-p", help = "Sets a profile before program goes into loop")
	parser.add_argument("--profile_location","-pl", help = "Sets profile location that isn't the default location")
	args = parser.parse_args()

	# Read in profiles
	if args.profile_location == None:
		pattern = re.compile(r"/(?P<root>[a-zA-Z0-9 ]+?)/(?P<user>[a-zA-Z0-9 ]+?)/")
		match = pattern.search(current_dir)
		profile_location = "/" + match.group("root") + "/" + match.group("user") + "/.aws/"
	else:
		profile_location = args.profile_location
	awsProfileLocation(profile_location)

	while True:
		response = raw_input("Type a command or \"help\" for a list of commands:\n")
		response = response.lower()

		# Split function away from response (for cases where file is acted on)
		responseList = response.split(" ")
		desiredFunction = responseList[0]

		# Quits awscli easy command
		if desiredFunction in quit:
			"Quitting..."
			break

		# Displays help file on commands
		elif desiredFunction in help:
			helpFile()

		# Lists profiles available and accepts an existing profile
		elif desiredFunction in profile:
			listAvailableProfile()
			while True:
				profile = raw_input("Enter new default profile: ")

		# Copies
		elif desiredFunction in copyCommand:
			if profile == "":
				missingProfile()
				continue
			if responseList > 1:
				awsCopy(responseList)
			print "Current profile: " + profile
			responseList.append(raw_input("Enter profile to copy use: "))
			responseList.append(raw_input("Enter file to copy: "))
			responseList.append(raw_input("Enter destination to copy file to: "))
			awsCopy(responseList)
		elif desiredFunction in listFilesCommand:
			if fileList == []:
				print "No file list in memory."
			elif profile == "":
				missingProfile()
				continue
		else:
			print "Not a valid command. Try again or type \"help\" for a list of commands.\n"

if __name__ == '__main__':
	main()