import os,sys,pyfits,functions
from numpy import *
import matplotlib.pyplot as plt
from scipy import ndimage

def fistar(fits):
    ### Use this command to automatically identify stars within an image
    ### to create a catalogue for matching

    ### first apply median filter to image
    data = pyfits.getdata(fits)
    data = ndimage.filters.median_filter(data,10)
    functions.save_fits(data,"temp.fits")
    
    command = "fistar "
    #command += "-i "+fits+" "
    command += "-i temp.fits "
    command += "-o "+fits+".fistar "
    command += "-t 100 "
    #command += "-f 1000 "
    command += "-M badpix.fits "
    command += "-F id,cx,cy,fwhm"
    
    os.system(command)

    ### Now plot image
    image = pyfits.getdata(fits)

    coords = loadtxt(fits+".fistar")

    mask = coords[:,3] > 3.
    
    mask *= coords[:,1] > 10 
    mask *= coords[:,1] < len(image[0])-10
    mask *= coords[:,2] > 10 
    mask *= coords[:,2] < len(image[0])-10
    coords = coords[mask]


    savetxt(fits+".fistar",coords,fmt="%.5f")

    #sigma = 0.01
    #stdev = std(image)
    lim = 500
    med = median(image)

    plt.clf()
    plt.imshow(image,cmap="gray",origin="lower",vmin=med-0.5*lim,vmax=med+lim,interpolation="nearest")

    plt.scatter(coords[:,1],coords[:,2],marker="o",facecolor="None",edgecolor="r",s=200)
    plt.savefig(fits+".png")
    #plt.show()
    plt.close()


    return coords

if __name__ == "__main__":
    fistar(sys.argv[1])
    
