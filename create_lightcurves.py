import os,sys,pyfits,glob
from numpy import *
import functions

def create_lightcurves(file_path,file_list,reflist,out_dir):
    jd_header = "UTMJD"


    lightcurves = []
    for i in reflist:
        lightcurves.append([])

    for input_file in file_list:

        hdulist = pyfits.open(file_path+input_file)
        jd = hdulist[0].header[jd_header]

        print input_file,jd

        phot = loadtxt(file_path+input_file+".phot")

        for star_i in range(len(reflist)):
            star_found = False
            #for star_j in phot:
            for j in range(len(phot)):
                star_j = phot[j]
                if reflist[star_i,0] == star_j[0]:

                    lightcurves[star_i].append([jd]+list(star_j[1:]))

                    star_found = True
                    break
            if not star_found:
                lightcurves[star_i].append([jd]+list(nan*zeros(len(phot[0]))))

    for i in range(len(reflist)):

        try:
            lc = array(lightcurves[i])

        except ValueError:
            print "ValueError in lightcurve",i
            lc = lightcurves[i]


        try:
            savetxt(out_dir+str(int(reflist[i,0]))+".rawlc",lc,fmt="%.5f")
        except (TypeError,ValueError):
            print "Error in writing lightcurve",i
            o = open(out_dir+str(int(reflist[i,0]))+".rawlc","w")
            functions.write_table(lc,o)
            o.close()

            
    

if __name__ == "__main__":
    file_path = functions.read_config_file("FILE_PATH")+"reduced/"
    program_dir = os.getcwd()+"/"
    os.chdir(file_path)
    temp_file_list = sort(glob.glob("*.fits"))
    file_list = []
    for filename in temp_file_list:
        if not ".bk.fits" in filename:
            file_list.append(filename)

    os.chdir(program_dir)

    reflist = loadtxt(file_path+"object_list")
    out_dir = file_path+"lc/"
    os.system("mkdir "+out_dir)

    create_lightcurves(file_path,file_list,reflist,out_dir)
