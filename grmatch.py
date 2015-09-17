import os,sys
from numpy import *

def grmatch(refcat,incat):

    cmd = "grmatch"
    cmd += " --input-reference "+refcat
    cmd += " --col-ref 2,3"
    cmd += " --input "+incat
    cmd += " --col-inp 2,3"
    cmd += " --output "+incat+".match"
    cmd += " --output-transformation "+incat+".trans"
    cmd += " --max-distance 3"
    #cmd += " --order 1"
    os.system(cmd)
    

if __name__ == "__main__":
    incat = sys.argv[1]
    refcat = sys.argv[2]

    grmatch(refcat,incat)
