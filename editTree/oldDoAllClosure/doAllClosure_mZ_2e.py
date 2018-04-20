from subprocess import call
import time 

### z -> ee
massZErr_rel_bins = [0,0.008]
nDiv = 10
for i in range(nDiv):
    massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.02-0.008)/nDiv)
massZErr_rel_bins.append(0.05)

inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/'
filename = 'DYJetsToLL_M-50_kalman_v4_m2e.root'
plotpath = '/home/mhl/public_html/2016/20161122_mass/fitmassZ/'
outtxtName = '../makeSummaryPlots/sigma_m2e.txt'

call('echo " " > ' + outtxtName, shell=True)

for i in range(len(massZErr_rel_bins)-1):

    cmd = 'python doClosure_mZ.py --min '+str(massZErr_rel_bins[i])+' --max '+str(massZErr_rel_bins[i+1]) \
        + ' --inpath ' + inputpath \
        + ' --filename ' + filename \
        + ' --plotpath ' + plotpath \
        + ' --outtxtName ' + outtxtName + ' --fs 2e & '

#    print cmd
    call(cmd, shell=True)


