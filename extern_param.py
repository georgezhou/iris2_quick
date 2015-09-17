import os,sys,functions
from numpy import *
import matplotlib.pyplot as plt

def plot_extern(lc):
    """
    0 hjd
    1 X
    2 Y 
    3 rawflux
    4 rawfluxerr
    5 background
    6 background_err
    7 S
    8 D
    9 K
    """

    hjd = lc[:,0]-floor(lc[0,0])

    plt.subplot(231)
    plt.scatter(hjd,lc[:,3])
    plt.xlabel("HJD")
    plt.ylabel("Raw Flux")

    plt.subplot(232)
    plt.scatter(hjd,lc[:,5])
    plt.xlabel("HJD")
    plt.ylabel("Background")

    plt.subplot(233)
    plt.scatter(hjd,sqrt(2/lc[:,7])*2.35)
    plt.xlabel("HJD")
    plt.ylabel("FWHM")
        
    plt.subplot(234)
    plt.scatter(hjd,lc[:,8])
    plt.xlabel("HJD")
    plt.ylabel("D")
        
    plt.subplot(235)
    plt.scatter(hjd,lc[:,9])
    plt.xlabel("HJD")
    plt.ylabel("K")
        
def main():
    file_path = functions.read_config_file("FILE_PATH")+"reduced/lc/"
    lc = genfromtxt(file_path+"0.rawlc",invalid_raise=False)

    plt.figure(figsize=(12,6))
    plt.subplots_adjust(left=0.07,right=0.98,wspace=0.3)
    plot_extern(lc)

    plt.savefig(file_path+"extern_param.png")
    #plt.show()
    plt.close()
    os.system("open "+file_path+"extern_param.png")
    
if __name__ == "__main__":

    main()
