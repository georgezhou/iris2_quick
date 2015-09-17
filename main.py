import os,sys,functions,pyfits,glob,string
from numpy import *
import matplotlib.pyplot as plt
import flatfield


def process(input_file,output_dest):

    fits_name_base = string.split(input_file,"/")[-1]
    fits_name_base = string.split(fits_name_base,".fits")[0]

    os.system("cp "+input_file+" "+output_dest+fits_name_base+".fits")
    data = pyfits.getdata(input_file)

    fits = pyfits.open(output_dest+fits_name_base+".fits",mode="update")
    fits.verify("silentfix")
    fits[0].data = data
    fits.flush()
    fits.close()

    return output_dest+fits_name_base+".fits"

def delete_all(file_path):
    os.system("rm -rf "+file_path+"temp/*")
    os.system("rm -rf "+file_path+"reduced/*")
    os.system("mkdir "+file_path+"reduced/")

def setup_dir(file_path):
    os.system("mkdir "+file_path+"temp")
    os.system("mkdir "+file_path+"reduced")

def main(file_path):
    ### Setup
    setup_dir(file_path)
    if functions.read_config_file("DELETE_ALL") == "true":
        delete_all(file_path)

    ### Make bias
    if not os.path.exists(file_path+"temp/master_dark.fits"):
        import master_dark
        master_dark.main(file_path)

    ### Make flatfield
    if not os.path.exists(file_path+"temp/master_flat.fits"):
        flatfield.main(file_path)

    ### load sciencelist
    sciencelist_temp = functions.find_objname(file_path,functions.read_config_file("OBJECT_HEADER"))

    ### Check if each one has been fully downloaded
    sciencelist = []
    for fits in sciencelist_temp:
        try:
            test = pyfits.getdata(fits)
            sciencelist.append(fits)
            print "OK",fits

        except ValueError:
            pass

    for fits in sciencelist:
        fits_base = string.split(fits,"/")[-1]
        fits_base = string.split(fits_base,".")[0]

        
        if not os.path.exists(file_path+"reduced/"+fits_base+".fits"):

            print "********************************"
            print "Reducing",fits

            fits_path = process(fits,file_path+"reduced/")
            flatfield.apply_flatfield(fits_path,file_path+"temp/master_flat.fits",file_path+"temp/master_dark.fits")

    
    ### Now extract sources in reference image, match, and do photometry
    import fistar,transcoord,fiphot
    
    refimage = functions.read_config_file("REFERENCE_IMAGE")
    refimage_coords=fistar.fistar(file_path+"reduced/"+refimage)
    reflist = loadtxt(functions.read_config_file("OBJECT_LIST"))
    
    ###reformat reflist so that it reflects the refimage actual star coordinates
    ### So that the extraction coordinates are exact
    new_reflist = []
    for star in reflist:
        dist = sqrt((star[1]-refimage_coords[:,1])**2 + (star[2]-refimage_coords[:,2])**2)
        indx = argmin(dist)
        star[1] = refimage_coords[indx,1]
        star[2] = refimage_coords[indx,2]
        new_reflist.append(star)

    savetxt(file_path+"reduced/object_list",array(new_reflist))
    
            

    for fits in sciencelist:
        fits_base = string.split(fits,"/")[-1]
        fits_base = string.split(fits_base,".")[0]

        if not os.path.exists(file_path+"/reduced/"+fits_base+".fits.phot"):
            ### transform the coordinates of extraction
            transcoord.transcoord(file_path+"/reduced/"+fits_base+".fits",file_path+"reduced/object_list",file_path+"reduced/"+refimage+".fistar")
            ### Now apply fiphot and get real photometry out
            fiphot.fiphot(file_path+"/reduced/"+fits_base+".fits")
        


def run():

    print "**** REMEMBER - ENTER OBJECT COORDS INTO OBJECT_COORDS.TXT ****"

    ### Reduce and create photometry
    main(functions.read_config_file("FILE_PATH"))
    os.system("cp config_file "+functions.read_config_file("FILE_PATH"))

    ### create light curve from reduced photometry
    os.system("python create_lightcurves.py")

    ### Generating guiding offset
    os.system("python guiding_offset.py")

    ### Plot the light curves
    os.system("python plot_lightcurves.py")

    ### Plot external parameters
    os.system("python extern_param.py")


if __name__ == "__main__":
    run()
