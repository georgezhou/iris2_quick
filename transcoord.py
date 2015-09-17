import os,sys,pyfits
from numpy import *
import matplotlib.pyplot as plt
import fistar,grmatch

def grtrans(input_coord,trans,output):
    cmd = "grtrans"
    cmd += " --input "+input_coord
    cmd += " --output "+output
    cmd += " --input-transformation "+trans
    cmd += " --col-xy 2,3"
    cmd += " --col-out 4,5"
    
    print cmd

    os.system(cmd)

def transcoord(input_image,reflist,refcat):

    ### First get trans file
    secat = fistar.fistar(input_image)
    grmatch.grmatch(refcat,input_image+".fistar")

    ### Now transform reference coordinates
    grtrans(reflist,input_image+".fistar.trans",input_image+".coord")

    coord = loadtxt(input_image+".coord")
    #se_findstar.plot_image(input_image,coord,xcol=3,ycol=4)

if __name__ == "__main__":
    input_image = sys.argv[1]
    refcat = sys.argv[2]

    transcoord(input_image,refcat)


