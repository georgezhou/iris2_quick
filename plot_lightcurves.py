import os,sys,string,glob,functions
from numpy import *
import matplotlib.pyplot as plt
from scipy import stats


def gen_lc(file_path,lcn,avoid,ap):
    lclist = sort(glob.glob(file_path+"*.rawlc"))

    ### read in target lightcurve
    lc = genfromtxt(file_path+str(lcn)+".rawlc",invalid_raise=False)
    hjd = lc[:,0]
    lc = lc[:,ap] / stats.nanmedian(lc[:,ap])

    
    ### read in all the reference light curves
    reflc = []
    for entry in lclist:
        entry = string.split(entry,"/")[-1]
        starno = int(string.split(entry,".rawlc")[0])
        if starno != lcn and not starno in avoid:
            ref = genfromtxt(file_path+str(starno)+".rawlc",invalid_raise=False)
            reflc.append(ref[:,ap] / stats.nanmedian(ref[:,ap]))
    
    reflc = array(reflc)

    ### Get a temporary ref lightcurve
    reflc_temp = []
    for i in range(len(reflc[0])):
        reflc_temp.append(stats.nanmean(reflc[:,i]))
    reflc_temp = array(reflc_temp)

    ### Work out the weights
    flux_weight = []
    for reflc_i in reflc:
        reflc_i = reflc_i/reflc_temp
        mask = reflc_i == reflc_i
        fit = polyfit(hjd[mask]-floor(hjd[0]),reflc_i[mask],1)
        fit = polyval(fit,hjd-floor(hjd[0]))    
        reflc_i /= fit
        flux_weight.append(stats.nanstd(reflc_i))

    flux_weight = array(flux_weight)

    ### Calculate the weighted mean reference light curve
    reflc_median = []
    for i in range(len(lc)):
        mask = reflc[:,i] == reflc[:,i]

        flux_i = reflc[:,i][mask]
        weight_i = flux_weight[mask]

        weight_i = 1/(weight_i**2)
        weight_i /= sum(weight_i)
        flux_i = sum(flux_i*weight_i)
        
        reflc_median.append(flux_i)

    reflc_median = array(reflc_median)
    
    lc /= reflc_median

    return hjd,lc
                            

def plot_lc(hjd,lclist):
    plt.subplot(211)
    plt.ylabel("Relative flux (all apertures)")

    std_list = []
    lclist_detrend = []
    for i in range(len(lclist)):
        plt.scatter(hjd-floor(hjd[0]),lclist[i])
        mask = lclist[i]==lclist[i]
        
        fit = polyfit(hjd[mask]-floor(hjd[0]),lclist[i][mask],1)
        fit = polyval(fit,hjd-floor(hjd[0]))

        lclist_detrend.append(lclist[i]/fit)
        std_i = stats.nanstd(lclist[i]/fit)
        if std_i != std_i:
            std_i = 99
        std_list.append(std_i)


    
    plt.subplot(212)
    plt.ylabel("Relative flux (best aperture)")

    print "STD of apertures",std_list
    best_lc = argmin(std_list)
    plt.scatter(hjd-floor(hjd[0]),lclist_detrend[best_lc])
    
if __name__ == "__main__":
    
    file_path = functions.read_config_file("FILE_PATH")+"reduced/lc/"
    lclist = glob.glob(file_path+"*.rawlc")
    lc_no = []
    for entry in lclist:
        entry = string.split(entry,"/")[-1]
        starno = int(string.split(entry,".rawlc")[0])
        lc_no.append(starno)
    lc_no = sort(array(lc_no))
    
    apertures = [3,10,17,24,31]

    for lcn in lc_no:
        print "calculating ",lcn
        lc_aps = []
        for ap in apertures:
            hjd,lc = gen_lc(file_path,lcn,[lcn,0],ap)
            lc_aps.append(lc)

            if len(lclist) > 3:
                for lc_i in lc_no:
                    if lc_i != lcn and lc_i != 0:
                        hjd,lc = gen_lc(file_path,lcn,[lcn,0,lc_i],ap)
                        lc_aps.append(lc)


        plt.figure(figsize=(5,7))
        plt.title(lcn)

        plot_lc(hjd,lc_aps)
        plt.xlabel("HJD-floor(HJD)")
        plt.savefig(file_path+str(lcn)+".png")
        #plt.clf()
        plt.close()

    os.system("open "+file_path+"0.png")
