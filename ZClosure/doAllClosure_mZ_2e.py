from subprocess import call
import time 

### z -> mumu
massZErr_rel_bins = [0.007]
#for i in range(4):
#    massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.014-0.007)/4)
#for i in range(5):
#    massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.03-0.014)/5)
#massZErr_rel_bins.append(0.05)
for i in range(15):
    massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.03-0.007)/15)

inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/HZZ4L_Mass/makeSlimTree/DY_2015MC_kalman_v4/'
filename = 'DYJetsToLL_M-50_kalman_v4_m2e.root'
plotpath = '/home/mhl/public_html/2016/20161020_mass/fitmassZ/'
outtxtName = '../sigma_m2e.txt'

call('echo " " > ' + outtxtName, shell=True)

for i in range(len(massZErr_rel_bins)-1):

    cmd = 'python doClosure_mZ.py --min '+str(massZErr_rel_bins[i])+' --max '+str(massZErr_rel_bins[i+1]) \
        + ' --inpath ' + inputpath \
        + ' --filename ' + filename \
        + ' --plotpath ' + plotpath \
        + ' --outtxtName ' + outtxtName + ' --fs 2e & '

#    print cmd
    call(cmd, shell=True)


