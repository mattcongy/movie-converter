#!/usr/bin/env python

# Standard imports
import sys, getopt, os
from os.path import isfile,isdir, join, basename

# Mconverter imports
from mconverter.movieconverter import MovieConverter
from mconverter import config
from mconverter.movieconverterDB import ConverterDB

class movie_converter(object):
    """docstring for movie-converter"""
    def __init__(self, arg):
        super(movie-converter, self).__init__()
        self.arg = arg

    @staticmethod
    def printHelp():
        print("movie-converter.py <options>")
        print("Options : ")
        print(" -i --init     : Initialize embedded database")
        print(" -c --convert  : Launch conversion with config.py parameters")
        print(" -d --display  : Display configuration parameters")

    @staticmethod
    def initDB():
        ConvDB = ConverterDB(config.mc_db_path)

        if isfile(config.mc_db_path):
            print("Database file is already present.")
            print("Would you confirm removal of database file ? (y/n)")
            answer = input()

            if answer =="y":
                os.remove(config.mc_db_path)
                ConvDB.initDB()
                print("Database is initialized")
            else:
                print("No confirmation given. Initialization aborted.")
        else:
            ConvDB.initDB()

    @staticmethod
    def convert():
        converter = MovieConverter(config.mc_folder_in,config.mc_folder_out)
        converter.prepareFiles(None)
        converter.processFiles()


def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hdi",["init","display","convert"])
   except getopt.GetoptError:
      movie_converter.printHelp()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         movie_converter.printHelp()
         sys.exit()
      elif opt in ("-i", "--init"):
         movie_converter.initDB()
      elif opt in ("-d", "--display"):
         config.print_configuration()
      elif opt in ("-c", "--convert"):
         movie_converter.convert()


if __name__ == "__main__":
   main(sys.argv[1:])



