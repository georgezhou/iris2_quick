import os,sys,functions
from numpy import *
import matplotlib.pyplot as plt

frame_scale = eval(functions.read_config_file("FRAME_SCALE"))
guider_scale = eval(functions.read_config_file("GUIDER_SCALE"))

 
def find_median_offset(data,original_x,original_y):
    return median(data[:,1])-original_x,median(data[:,2])-original_y


def read_xy(file_path):

    current_dir = os.getcwd()
    os.chdir(file_path)

    lc = loadtxt("0.rawlc")

    hjd = lc[:,0]
    xcoord = lc[:,1]
    ycoord = lc[:,2]

    data = transpose(array([hjd,xcoord,ycoord]))


    # ### Find initial position
    # ### find if already calculated

    # if os.path.exists("init_pos"):
    #     init_pos = loadtxt("init_pos")

    # ### Otherwise, calculate by median first 10 mins
    # else:
    mask = hjd < min(hjd)+0.0068
    
    init_pos = array([median(xcoord[mask]),median(ycoord[mask])])
    #savetxt(init_pos,"init_pos",fmt="%.5f")

    ### Now calculate offset

    ### Work out the region to calculate offset
    
    #if init_pos[2] == 0:
        ### use the last 10 minutes
    mask = hjd > max(hjd) - 0.00347
    #init_pos[2] = max(hjd)
    offset_x,offset_y = find_median_offset(data[mask],init_pos[0],init_pos[1])
        
    # else:
        
    #     mask = hjd > init_pos[2]
    #     init_pos[2] = max(hjd)
    #     offset_x,offset_y = find_median_offset(data[mask],init_pos[0],init_pos[1])

    
    ### Calculate required guiding inputs
    print "###################################"
    print "Offsets",offset_x,offset_y

    guiding_inputs = array([-1*offset_x*frame_scale,-1*offset_y*frame_scale])#-guider_pos[1:]

    guiding_corrections = ""
    if guiding_inputs[0] < 0:
        print abs(guiding_inputs[0]),"E"
        guiding_corrections += str(abs(round(guiding_inputs[0],2)))+"E "
    else:
        print abs(guiding_inputs[0]),"W"
        guiding_corrections += str(abs(round(guiding_inputs[0],2)))+"W "


    if guiding_inputs[1] < 0:
        print abs(guiding_inputs[1]),"S"
        guiding_corrections += str(abs(round(guiding_inputs[1],2)))+"S "

    else:
        print abs(guiding_inputs[1]),"N"
        guiding_corrections += str(abs(round(guiding_inputs[1],2)))+"N "



    plt.figure(figsize=(5,7))
    
    #plt.title(guiding_corrections)
    
    ax=plt.subplot(211)

    plt.text(0.1,1.1,"Corrections: "+guiding_corrections,transform=ax.transAxes,fontsize=18)

    plt.axvline((min(hjd)+0.0068)-floor(hjd[0]),color="r")
    plt.axvline((min(hjd))-floor(hjd[0]),color="r")

    plt.axvline((max(hjd)-0.00347)-floor(hjd[0]),color="k")
    plt.axvline((max(hjd))-floor(hjd[0]),color="k")

    plt.scatter(hjd-floor(hjd[0]),xcoord)
    plt.axhline(init_pos[0])
    plt.ylabel("X")

    plt.ylim(min(xcoord),max(xcoord))
    plt.subplot(212)


    plt.axvline((min(hjd)+0.0068)-floor(hjd[0]),color="r")
    plt.axvline((min(hjd))-floor(hjd[0]),color="r")

    plt.axvline((max(hjd)-0.00347)-floor(hjd[0]),color="k")
    plt.axvline((max(hjd))-floor(hjd[0]),color="k")

    plt.scatter(hjd-floor(hjd[0]),ycoord)
    plt.axhline(init_pos[1])
    plt.ylim(min(ycoord),max(ycoord))

    plt.ylabel("Y")
    plt.savefig("guiding.png")
    #plt.show()
    plt.close()
    os.system("open guiding.png")


if __name__ == "__main__":
    
    #file_path = sys.argv[1]
    file_path = functions.read_config_file("FILE_PATH")+"reduced/lc/"
    read_xy(file_path)
