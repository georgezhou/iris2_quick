import os,sys,pyfits,functions,glob
from numpy import *
from scipy import stats
import matplotlib.pyplot as plt
#import calcor_iris2

def average_darks(darklist,dark):
    dark = pyfits.getdata(dark)

    dark_array = []
    for fits in darklist:
        print fits
        fits = pyfits.getdata(fits)

        if len(fits.shape) == 3:
            #fits = calcor_iris2.calcor(fits)
            for n in fits:
                dark_array.append(n-dark)
        else:
            #fits = calcor_iris2.calcor(fits)[0]
            dark_array.append(fits-dark)

    dark_array = array(dark_array)
    dark_array = median(dark_array,axis=0)
    dark_array /= median(dark_array)
    return dark_array

def apply_flatfield(fits,flat,dark):
    flat = pyfits.getdata(flat)
    dark = pyfits.getdata(dark)
    fitsdata = pyfits.getdata(fits)

    fitsdata = fitsdata - dark
    fitsdata /= flat

    fits = pyfits.open(fits,mode="update")
    fits.verify("silentfix")
    fits[0].data = fitsdata
    fits.flush()
    fits.close()



def main(file_path):

    darklist = functions.find_objname(file_path,functions.read_config_file("FLAT_HEADER"))

    if len(darklist) == 0:
        print "Error: no flats found"
        raise IOError

    master_dark = average_darks(darklist,file_path+"temp/master_dark.fits")
    
    try:
        functions.save_fits(master_dark,file_path+"temp/master_flat.fits")
    except IOError:
        os.system("mkdir "+file_path+"temp/")
        functions.save_fits(master_dark,file_path+"temp/master_flat.fits")

if __name__ == "__main__":
    main(sys.argv[1])
