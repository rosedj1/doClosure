from subprocess import call
import time 

def doAllClosure(fs, plotPath, Z_width, plotBinInfo, singleCB_tail, pTErrCorrections):

    massZErr_rel_bins = [0, 0.008]
    nDiv = 10
    for i in range(nDiv):
        massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.02-0.008)/nDiv)
    massZErr_rel_bins.append(0.05)

    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/'
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut/'
    filename = 'DYJetsToLL_M-50_kalman_v4_m'+fs+'.root'
    outtxtName = '../makeSummaryPlots/sigma_m'+fs+'.txt'

    call('echo " " > ' + outtxtName, shell=True)

    for i in range(len(massZErr_rel_bins)-1):

        cmd = 'python doClosure_mZ.py --min '+str(massZErr_rel_bins[i])+' --max '+str(massZErr_rel_bins[i+1]) \
            + ' --inpath ' + inputpath \
            + ' --filename ' + filename \
            + ' --plotpath ' + plotpath \
            + ' --zWidth ' + str(Z_width) \
            + ' --plotBinInfo ' + plotBinInfo  \
            + ' --singleCB_tail ' + singleCB_tail \
            + ' --pTErrCorrections ' + pTErrCorrections \
            + ' --outtxtName ' + outtxtName + ' --fs ' + fs + ' &'

        #    print cmd
        call(cmd, shell=True)


plotBinInfo = '300 60 120'
plotpath = '/home/mhl/public_html/2016/20161124_mass/test/'

singleCB_tail_mu = '1.583 1.086' #first is alpha, second is n of singleCB
singleCB_tail_e = '1.071 2.985' #first is alpha, second is n of singleCB

pTErrCorrections_mu = '1.251 1.292 1.117 1'
pTErrCorrections_e = '1.245 1.290 1.116'

ZWidth_mu = 2.44

doAllClosure('2mu', plotpath, ZWidth_mu, plotBinInfo, singleCB_tail_mu, pTErrCorrections_mu)
#doAllClosure('2e', plotpath)

