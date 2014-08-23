#!/usr/bin/python

import logging
import locale
import hashlib
import os
import shutil

from os import listdir
from os.path import isfile, join, basename

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

	def listFiles(self):
		 onlyfiles = [ f for f in listdir(self.infolder) if isfile(join(self.infolder,f)) ]
		 #print(onlyfiles)


	def prepareFiles(self):
		dirs = listdir(self.infolder);
		pathfile = ""
		md5tool = hashlib.md5()


		# Calculate MD5Sum for this file
		for file in dirs:
			if not file.startswith('.'):
				pathfile = join(self.infolder,file)
				print(file,pathfile)


				with open(pathfile,"rb") as file_to_check:
					data = file_to_check.read()
					md5_returned = hashlib.md5(data).hexdigest()
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
		ext = config.mc_video_audio_preset['format']
		print(ext)
		out_path = config.mc_folder_out + "/" + name_wo_ext +"." + ext
		print ("configOut is :", config.mc_folder_out)
		print ("BaseName is :", name_wo_ext)
		print ("Out path is : ",out_path)

		print ("-----------------------------------------------")
		print (" Convert File :", mFile.name)
		print (" To Output dir:", out_path)
		print (" Converted dir:", config.mc_folder_conv)
		print ("-----------------------------------------------")

		conv = c.convert(mFile.path,out_path,config.mc_video_audio_preset)

		for timecode in conv:
    			print("Converting  ...%2d%%\r " % timecode,end="")

		print ("Converted.                [DONE]")

		# Once converted, we move original file to 'Done' folder


		shutil.move(mFile.path,config.mc_folder_conv)



