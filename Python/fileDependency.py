# This function compares the modification time of input file and output file
# if the output file is not up-to-date, i.e. the modification time is earlier for output file
# updating steps will be called.
import os.path

class fileDependency():
	def __init__(self, inputFile, outputFile, *proc):
		# inputFile: input File path
		# outputFile: output File path
		# *proc: if the outputfile is not up-to-date, the processed to be taken
		
		self.inputModTime = os.path.getmtime(inputFile) # modificaiton time of the input file
		self.outputModTime = os.path.getmtime(outputFile) # modification time of the output file
		if self.inputModTime > self.outputModTime:
			# output file is not up-to-date, recalculate outputFile from inputFile
			print "Target file is not up-to-date. Updating..."
			result = proc	 
		return result

	
	
