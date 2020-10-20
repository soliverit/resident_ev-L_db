#####################################
# Resident Ev-L Ruby interface
#
# The Ruby interface for the 
# Residential Retrofit Evaluator
# Part L(A) dataset
#
####################################
class REDataset
	##
	# Getters
	##
	attr_reader :baseDir, :certsPath, :targetsPath, :retrofitsPath
	##
	# Table file aliases
	##
	CERTS_CSV_NAME		= "certificates"
	TARGETS_CSV_NAME	= "targets"
	RETROFITS_CSV_NAME	= "retrofits"
	##
	# baseDir:	String path to region directory
	##
	def initialize baseDir
		##
		# Throw a fit if the region directory doesn't exist
		##
		unless File.directory? baseDir
			raise "REDataset:BaseDirNotFound"
		end
		##
		# Define stuff
		##
		@baseDir		= baseDir
		@certsPath		= @baseDir + CERTS_CSV_NAME + ".csv"
		@targetsPath	= @baseDir + TARGETS_CSV_NAME + ".csv"
		@retrofitsPath	= @baseDir + RETROFITS_CSV_NAME + ".csv"
		@records		= []
	end
	##
	# idx:		Integer row index
	#
	# Return	RERecord from records
	##
	def [] idx
		@records[idx]
	end
	##
	# Return:	Integer length of table, assuming it's been loaded
	##
	def length
		@records.length
	end
	##
	# Do block with each record
	##
	def each &block
		@records.each{|record| yield record}
	end
	##
	# Remove records which are invalid
	##
	def filterErrors
		return if @errorsRemoved
		@records.select!{|record| ! record.failed}
		@errorsRemoved = true
	end
	##
	# Load Dataset 
	#
	#	Loads the certificates, targets and retrofits tables
	##
	def load 
		# Don't do it twice
		return if @records.any?
		# Pretend to fail gracefully... ... ... ...
		raise "REDataset:DataFileNotFound #{certsPath}" unless File.exists? certsPath
		raise "REDataset:DataFileNotFound #{certsPath}" unless File.exists? targetsPath
		raise "REDataset:DataFileNotFound #{certsPath}" unless File.exists? retrofitsPath
		# Open stuff
		certsFile 			= CSV.open(certsPath)
		targetsFile			= CSV.open(targetsPath)
		retrofitsFile		= CSV.open(retrofitsPath)
		# Get headers
		certsHeaders		= certsFile.shift.map{|header| header.to_sym}
		targetsHeaders		= targetsFile.shift.map{|header| header.to_sym}
		retrofitsHeaders	= retrofitsFile.shift.map{|header| header.to_sym}
		# Read stuff (kind of dirty but whatever)
		while certsRecord = certsFile.shift
			# Get the other 
			targetsRecord	= targetsFile.shift
			retrofitsRecord	= retrofitsFile.shift
			# Build the new record
			newRecord 		= {}
			certsHeaders.each_with_index{|key, idx| newRecord[key] = certsRecord[idx]}
			targetsHeaders.each_with_index{|key, idx| newRecord[key] = targetsRecord[idx]}
			retrofitsHeaders.each_with_index{|key, idx| newRecord[key] = retrofitsRecord[idx]}
			# Append to table
			@records.push RERecord.new(newRecord)
		end
	end
end
##
# Dataset Record, mergeable
##
class RERecord
	##
	# cells:	Hash of record properties
	##
	def initialize cells
		##
		# Convert values into numbers if appropriate
		##
		cells.keys.each{|key|cells[key] = cells[key].to_f rescue cells[key].to_s} 
		@cells = cells
	end
	##
	# Returns:	Bool did the record have errors
	#
	# Note:		Rather that mess with the original certificates
	#			file content, a known identifier from retorfits
	#			is used.
	##
	def failed
		@cells[:"roof-Eff"].to_i == -9999 # As good as anything else, I guess
	end
	##
	# Subscripted access to properties
	##
	def [] key
		@cells[key]
	end
	##
	# Return:	Array of record properties
	##
	def keys
		@keys ||= @cells.keys.dup
	end
end