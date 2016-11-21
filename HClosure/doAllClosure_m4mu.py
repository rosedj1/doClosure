from subprocess import call
import time 

### z -> mumu
mass4lErr_bins = [0, 0.005, 0.007, 0.008]
nDiv = 8
for i in range(nDiv):
    mass4lErr_bins.append(mass4lErr_bins[-1]+(0.02-0.008)/nDiv)
mass4lErr_bins.append(0.05)

#    mass4lErr_bins.append(mass4lErr_bins[-1]+(2-0.6)/nDiv)
#mass4lErr_bins.append(5)

inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/liteUFHZZ4LAnalyzer/Ntuples/'
#inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/Mass_2015MC/Fit_PereventMerr/'
filename = 'test_tripleGauss_symErrHESSE_corrMuPtScale.root'
plotpath = '/home/mhl/public_html/2016/20161121_mass_addMuonPtScaleCorr/fitmassHREFIT/'
outtxtName = '../makeSummaryPlots/sigma_m4mu.txt'

call('echo " " > ' + outtxtName, shell=True)

for i in range(len(mass4lErr_bins)-1):

    cmd = 'python doClosure_m4l.py --min '+str(mass4lErr_bins[i])+' --max '+str(mass4lErr_bins[i+1]) \
        + ' --inpath ' + inputpath \
        + ' --filename ' + filename \
        + ' --plotpath ' + plotpath \
        + ' --outtxtName ' + outtxtName + ' --channel 4mu &'

    print cmd
    call(cmd, shell=True)


