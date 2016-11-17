from subprocess import call
import time 

### z -> mumu
mass4lErr_bins = [0.7]
for i in range(10):
    mass4lErr_bins.append(mass4lErr_bins[-1]+(3-0.7)/10)
mass4lErr_bins.append(5)

inputpath = '/cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/Ana_ZZ4L/Ntuples/'
filename = 'mH_125.root'
plotpath = '/home/mhl/public_html/2016/20161023_mass/'
outtxtName = '../sigma_m2e2mu.txt'

call('echo " " > ' + outtxtName, shell=True)

for i in range(len(mass4lErr_bins)-1):

    cmd = 'python doClosure_m4l.py --min '+str(mass4lErr_bins[i])+' --max '+str(mass4lErr_bins[i+1]) \
        + ' --inpath ' + inputpath \
        + ' --filename ' + filename \
        + ' --plotpath ' + plotpath \
        + ' --outtxtName ' + outtxtName + ' --channel 2e2mu &'

    print cmd
    call(cmd, shell=True)


