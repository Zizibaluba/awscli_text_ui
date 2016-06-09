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

def setProfile(profileList):
	while True:
		listAvailableProfile()
		profileName = raw_input("Enter new default profile: ")
		if profileName in profileList:
			return profileName

def awsProfileLocation(profile_location):
	profileList = {}
	os.chdir(profile_location)
	with open("credentials", "rU") as profile_file:
		i = 0 #Counter/Numbers for 
		for line in profile_file:
			credentialName = re.search("(?<=\[).*(?=\])", line)
			if credentialName:
				i += 1
				profileList[i] = credentialName.group()
	fabprint(profileList)
	print #For readability
	return profileList

def helpFile():
	print "------Command List-------"
	print "copy [source files]"
	print "cp: Same as copy\n"
	
	
	print "listfile [aws location]"
	print "ls: Same as listfile"
	print "dir: Same as listfile"
	print "NOTE: If a previous listfile command is used, you can simply call it up from memory using listfile or ls\n"
	
	print "profile [profile number]"

	print "quit: Quits this script"
	print "q: Same as quit"
	print "exit: Same as quit\n"

	print "help: Opens up this command list\n"	
	return

def missingProfile():
	print "Missing default profile. Please use [profile] to set new profile.\n"

def main():
	# Commands and response lists
	quit = ["q", "quit", "exit"]
	listFileCommand = ["listfile", "ls", "dir"]
	copyCommand = ["copy", "cp"]
	profile = ["profile", "p"]
	yes = ["y", "yes"]
	no = ["n", "no"]

	# Constants kept in memory
	fileList = [] #ls that is kept in memory
	profileName = "" #Current name of profile kept in memory

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
			"""Should check if there are threads in process here"""
			print "Quitting..."
			break

		# Displays help file on commands
		elif desiredFunction in help:
			helpFile()

		# Lists profiles available and accepts an existing profile
		elif desiredFunction in profile:
			setProfile()

		# Copies files to a local location
		elif desiredFunction in copyCommand:
			if profileName == "":
				missingProfile()
				continue
			print "Current profile: " + profile

			# Check if there is already arguments for files
			if responseList > 1:
				fileList = responseList[1:]

			# Create a list of files to pull
			else:
				rawFileString = raw_input("Enter files to copy, separated by space: "))
				fileList = rawFileString.split(" ")

			while True:
				destination = list(raw_input("Enter destination to copy file to, leave blank to default to the current directory: "))
				if os.path.isdir(destination) != True:
					print "Destination does not exist, try again.\n"
			responseList.append(destination)

			if responseList > 1:
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