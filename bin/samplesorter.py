#!/usr/bin/python
"""
Version 0.1
This comes with absolutely no warranty
Use at your own risk
"""

import os
import re
import shutil
import datetime
from optparse import OptionParser

class SampleSorter:
	def __init__(self, src, dest):
		self.src = src.rstrip('/')
		self.dest = dest.rstrip('/')
		self.DirsToCreate = {
			'kick': '_Kicks',
			'clap': '_Claps',
			'snare': '_Snares',
			'tom': '_Toms',
			'hat': '_Hats',
			'hh': '_Hats',
			'cym': '_Hats',
			'shak': '_Shakers',
			'tamb': '_Shakers',
			'bake': "_Shakers",
			'perc': '_Percs',
			'bongo': '_Bongo',
			'cong': '_Bongo',
			'loop': '_Loops',
			'drumlp': '_Loops',
			'bell': '_Bells',
			'varied': '_Varied',
			'stab': '_Stabs',
			'pad': '_Pads',
			'string': '_Strings',
			'piano': '_Piano',
			'rhodes': '_Rhodes',
			'synth': '_Synth',
			'guitar': '_Guitar',
			'vox': '_Vocal',
			'shout': '_Vocal',
			'vocal': '_Vocal',
			'spoken': '_Vocal',
			'voco': '_Vocal',
			'bass': '_Bass',
			'brass': '_Brass',
			'trump': '_Brass',
			'horn': '_Brass',
			'tuba': '_Brass',
			'trombone': '_Brass',
			'flugelhorn': '_Brass',
			'sax': '_Woodwind',
			'flute': '_Woodwind',
			'piccolo': '_Woodwind',
			'clarinet': '_Woodwind',
			'bassoon': '_Woodwind',
			'oboe': '_Woodwind',
			'fx': '_FX',

		}

		self._set_up_dirs()

	# end __init__

	def _set_up_dirs(self):
		if not os.path.isdir(self.src):
			raise Exception("The Src folder is not a directory")
		# we can create this directory
		if not os.path.isdir(self.dest):
			os.makedirs(self.dest, mode=0775)

		for newDir in self.DirsToCreate.itervalues():
			if not os.path.isdir("%s/%s" % (self.dest, newDir)):
				os.makedirs("%s/%s" % (self.dest, newDir), mode=0775)

	# end set_up_dirs

	def read_files(self):

		for root, dirs, files in os.walk(self.src):
			# get the file creation time
			for name in files:

				current_file = "%s/%s" %(root, name)

				if re.search("^\.[^.]+|\.ini$|\.asd$", name):
					continue
				# Do we have access?
				if not os.access(current_file, os.R_OK):
					continue

				# figure out the directory
				current_file_date = datetime.date.fromtimestamp( os.path.getmtime(current_file) ).strftime("%Y")
				# where do you put it?
				pregmatch = self.DirsToCreate.keys()
				match = [i for i, x in enumerate(pregmatch) if re.search("%s" %(x), name, flags=re.IGNORECASE)]

				# our default store dir
				if len(match):
					store_dir = "%s/%s/%s" %(self.dest, self.DirsToCreate[pregmatch[match.pop()]], current_file_date)
				else:
					store_dir = "%s/%s/%s" %(self.dest, '_Varied', current_file_date)

				# make the new dir if we don't have it
				if not os.path.isdir(store_dir):
					os.makedirs(store_dir)

				shutil.copy2(current_file, "%s/%s" %(store_dir, name))
				print "Copied %s -> %s" %(name, store_dir)

		return True
	# end read_files

# end SampleCopier

if __name__ == "__main__":

	Usage = "Usage: [src folder] [dest folder]"
	parser = OptionParser(Usage)

	(options, args) = parser.parse_args()

	# Run through some checks first
	if len(args) < 2:
		print parser.print_usage()
		exit()

	try:
		ss = SampleSorter(os.path.normpath(args[0]), os.path.normpath(args[1]))
		ss.read_files()
		print "Done"
	except Exception as e:
		print e.message