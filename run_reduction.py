import os,sys,glob,string,functions
from numpy import *
import os, time
import main

def monitor(path_to_watch):

    fits_list = glob.glob(path_to_watch+"*.fits")
    reduced_list = glob.glob(path_to_watch+"reduced/*.fits")

    if len(fits_list) == len(reduced_list):
        time.sleep(10)
        main.run()
    else:
        print "No new files"



if __name__ == "__main__":
    file_path = functions.read_config_file("FILE_PATH")
    main.run()
    monitor(file_path)
