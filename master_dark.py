import os,sys,pyfits,functions,glob
from numpy import *
from scipy import stats
import matplotlib.pyplot as plt
#import calcor_iris2

def average_darks(darklist):
    dark_array = []
    for fits in darklist:
        print fits
        fits = pyfits.getdata(fits)

        if len(fits.shape) == 3:
            #fits = calcor_iris2.calcor(fits)
            for n in fits:
                dark_array.append(n)
        else:
            #fits = calcor_iris2.calcor(fits)[0]
            dark_array.append(fits)

    dark_array = array(dark_array)
    dark_array = mean(dark_array,axis=0)
    return dark_array
        

def main(file_path):

    darklist = functions.find_objname(file_path,functions.read_config_file("BIAS_HEADER"))
    master_dark = average_darks(darklist)
    try:
        functions.save_fits(master_dark,file_path+"temp/master_dark.fits")
    except IOError:
        os.system("mkdir "+file_path+"temp/")
        functions.save_fits(master_dark,file_path+"temp/master_dark.fits")

if __name__ == "__main__":
    main(sys.argv[1])
