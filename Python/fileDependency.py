# This function compares the modification time of input file and output file
# if the output file is not up-to-date, i.e. the modification time is earlier for output file
# updating steps will be called.
import os.path

class fileDependency():
	def __init__(self, inputFile, outputFile, fun):
		# inputFile: input File path
		# outputFile: output File path
		# *proc: if the outputfile is not up-to-date, the process to be taken
		flag = True
		assert os.path.isfile(inputFile)
		if not os.path.isfile(outputFile):
			flag = False
		
		self.inputModTime = os.path.getmtime(inputFile) # modification time of the input file
		if flag:
			self.outputModTime = os.path.getmtime(outputFile) # modification time of the output file
		else:
			self.outputModTime = self.inputModTime - 1
		if (self.inputModTime > self.outputModTime) or (not flag):
			# output file is not up-to-date, recalculate outputFile from inputFile
			print "[STATUS] Target file (" + str(outputFile) + ") is not up-to-date. Updating..."
		 	fun()
		 	print "[STATUS] Done! "
		 	return None
		else:
			print "[STATUS] Target file (" + str(outputFile) + ") is up-to-date." 
			return None



