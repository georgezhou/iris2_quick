import os,sys,pyfits
from numpy import *
from pyraf import iraf

def fiphot(input_image,apertures="7.5:20:5,10:20:5,12.5:20:5,15:20:5,17.5:20:5,20:20:5"):
    
    cmd = "fiphot"
    cmd += " -i "+input_image
    cmd += " --output "+input_image+".phot"
    cmd += " --input-list "+input_image+".coord --col-xy 4,5"
    cmd += " --col-id 1"
    cmd += " --nan NaN"
    #cmd += " --spline"
    cmd += " --apertures "+apertures
    cmd += " --sky-fit median,iterations=1,sigma=3"
    cmd += " --format IXY,FfBbWDK"
    cmd += " --disjoint-annuli"

    os.system(cmd)
    #os.system("rm check.fits")
    #os.system("rm temp.fits*")

if __name__ == "__main__":
    input_image = sys.argv[1]

    fiphot(input_image)
