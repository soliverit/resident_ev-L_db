#####################################
# Resident Ev-L Python interface
#
# The Python interface for the 
# Residential Retrofit Evaluator
# Part L(A) dataset
#
####################################
# Native
import csv
from os.path import exists
##
# Dataset composite table class 
##
class REDataset():
	##
	# Table file aliases
	##
	CERTS_CSV_NAME		= "certificates.csv"
	TARGETS_CSV_NAME	= "targets.csv"
	RETROFITS_CSV_NAME	= "retrofits.csv"
	##
	# baseDir:	String path to directory with
	# 	the name format "domestic-<government_code>-<County>
	##
	def __init__(self, baseDir):
		##
		# Make sure the dataset exists
		##
		if not exists(baseDir):
			raise "REDataset:BaseDirNotFound - %s" %(baseDir)
		##
		# Define stuff
		##
		self.baseDir 	= baseDir
		# RERecord array
		self.records 	= []
		## Placeholders
		self.loaded		= False
	##
	# Retrieve RERecord by index
	#
	# idx:		Integer index
	#
	# Return:	RERecord
	##
	def __getitem__(self, idx):
		return self.records[idx]
	##
	# Return:	 Integer length of dataset
	##
	def __len__(self):
		return len(self.records)
	##
	# Path to certificates file
	##
	@property
	def certsPath(self):
		return self.baseDir + __class__.CERTS_CSV_NAME 
	##
	# Path to targets file
	##
	@property 
	def targetsPath(self):
		return self.baseDir + __class__.TARGETS_CSV_NAME 
	##
	# Path to retrofits file
	##
	@property
	def retrofitsPath(self):
		return self.baseDir + __class__.RETROFITS_CSV_NAME	
	##
	# Remove records which insufficient data for feature creation
	##
	def filterErrors(self):
		self.records = [record for record in self.records if not record.failed]
	##
	# Load the dataset
	##
	def load(self):
		# Don't do it twice!
		if self.loaded:
			return False
		##
		# Make sure all the files exist
		##
		if not exists(self.certsPath):
			raise "REDataset:CertsFileNotFound"
		if not exists(self.targetsPath):
			raise "REDataset:TargetsFileNotFound"
		if not exists(self.retrofitsPath):
			raise "REDataset:RetrofitsFileNotFound"
		##
		# Open the data files
		##
		certsFile 		= csv.reader(open(self.certsPath))
		targetsFile		= csv.reader(open(self.targetsPath))
		retrofitsFile	= csv.reader(open(self.retrofitsPath))
		##
		# Read records
		## 
		certsHeaders	= next(certsFile)
		targetsHeaders	= next(targetsFile)
		retrofitsHeaders= next(retrofitsFile)
		while True:
			##
			# Read the next row of each file,
			# bail out if you've reached the end
			##
			try:
				certsRecord		= next(certsFile)
			except StopIteration as se:
				break
			targetsRecord	= next(targetsFile)
			retrofitsRecord	= next(retrofitsFile)
			##
			# Build new RERecord input hash
			##
			record			= {}
			# Certificates
			for idx, value in enumerate(certsRecord):
				record[certsHeaders[idx]] 		= certsRecord[idx]
			# Targets 
			for idx, value in enumerate(targetsRecord):
				record[targetsHeaders[idx]] 	= targetsRecord[idx]
			# Retrofits
			for idx, value in enumerate(retrofitsRecord):
				record[retrofitsHeaders[idx]]	= retrofitsRecord[idx]
			##
			# Add new record
			##
			self.records.append(RERecord(record))
		##
		# Make sure we don't load it again (without malicious anyway)! 
		##
		self.loaded = True

##
# Dataset Record Object
##
class RERecord():
	##
	# cells:	Hash of properties
	##
	def __init__(self, cells):
		self.cells	= {}
		for key, value in cells.items():
			try: 
				self.cells[key] = float(value)
			except:
				self.cells[key] = str(value)
	##
	# Retrieve property - subscripted [] access
	#
	# key:	String key of property
	##
	def __getitem__(self, key):
		return self.cells[key]
	##
	# Return:	Array of record property labels
	##
	@property 
	def keys(self):
		return list(self.cells)
	##
	# Returns:	Bool did the record have errors
	#
	# Note:		Rather that mess with the original certificates
	#			file content, a known identifier from retorfits
	#			is used.
	##
	@property
	def failed(self):
		return self.cells["roof-Eff"] == -9999.0 # Since we don't track error in certs
