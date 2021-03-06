#!/usr/bin/python

import logging
import locale
import hashlib
import os
import shutil

from os import listdir
from os.path import isfile,isdir, join, basename

from mconverter.moviefile import MovieFile
from mconverter.movieconverterDB import ConverterDB
from mconverter import Converter
from mconverter import config

class MovieConverter(object):
	files = []

	"""docstring for MovieConverter"""
	def __init__(self, infolder,outfolder):
		super(MovieConverter, self).__init__()
		self.infolder = infolder
		self.outfolder = outfolder

	def setPreset(self,preset):
		self.preset = preset
		print("preset set")

	def listFiles(self):
		 onlyfiles = [ f for f in listdir(self.infolder) if isfile(join(self.infolder,f)) ]
		 #print(onlyfiles)

	def md5_for_file(self,f, block_size=32768):
	    md5 = hashlib.md5()
	    while True:
	        data = f.read(block_size)
	        if not data:
	            break
	        md5.update(data)
	    return md5.digest()

	def prepareFiles(self,filePath):

		if filePath is None:
			filePath = self.infolder

		dirs = listdir(filePath);
		pathfile = ""
		md5tool = hashlib.md5()


		# Calculate MD5Sum for this file
		for file in dirs:
			pathfile = join(filePath,file)
			if isdir(pathfile):
				self.prepareFiles(pathfile)
			else:
				if not file.startswith('.'):

					print(file,pathfile)

					# Read only 128-bytes of file to update MD5.
					with open(pathfile,"rb") as file_to_check:
						md5_returned = self.md5_for_file(file_to_check)
						movFile = MovieFile(file,pathfile,md5_returned)

						# Check if MD5 file is already in database
						ConvDB = ConverterDB()
						getNameFromDB = ConvDB.getMovieInfo(md5_returned)
						if getNameFromDB is not None:
							print("MD5 is already in database. File ignored...");
							print("NameFromDB:",getNameFromDB)
						else:
							ConvDB.insertMovie(movFile)
							MovieConverter.files.append(movFile)

					#with open(pathfile,"rb") as file_to_check:
					#	data = file_to_check.read()
					#	md5_returned = hashlib.md5(data).hexdigest()
					#	movFile = MovieFile(file,pathfile,md5_returned)


	def processFiles(self):
		"""
			Process File from queue. Send it to FFMpeg for conversion
		"""
		print("Process Files from queue:")
		for file in MovieConverter.files:
			print("Processing with file '",file.name,"'")
			self.convertFile(file)

	def convertFile(self,mFile):
		"""
			Process File from queue. Send it to FFMpeg for conversion
			@parameter path : To be converted file path.
		"""
		c = Converter()
		info = c.probe(mFile.path)

		name_wo_ext = basename(os.path.splitext(mFile.path)[0])
		ext = self.preset['format']
		out_path = config.mc_folder_out + "/" + name_wo_ext +"." + ext
		print ("configOut is :", config.mc_folder_out)
		print ("BaseName is :", name_wo_ext)
		print ("Out path is : ",out_path)

		print ("-----------------------------------------------")
		print (" Convert File :", mFile.name)
		print (" To Output dir:", out_path)
		print (" Converted dir:", config.mc_folder_conv)
		print ("-----------------------------------------------")

		conv = c.convert(mFile.path,out_path,self.preset)

		for timecode in conv:
    			print("Converting  ...%2d%%\r " % timecode,end="")

		print ("Converted.                [DONE]")

		# Once converted, we move original file to 'Done' folder
		shutil.move(mFile.path,config.mc_folder_conv)



