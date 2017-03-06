from subprocess import call
import time 

def doAllClosure(fs, plotPath, Z_width, plotBinInfo, singleCB_tail, pTErrCorrections):

#    massZErr_rel_bins = [0,0.009]
#    nDiv = 8
#    for i in range(nDiv):
#       massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.03-0.009)/nDiv)
#    massZErr_rel_bins.append(0.04)
#    massZErr_rel_bins.append(0.1)
#    massZErr_rel_bins.append(1)
    massZErr_rel_bins = [0,1]


    '''
    massZErr_rel_bins = [0,1]
    nDiv = 8
    for i in range(nDiv):
        massZErr_rel_bins.append(massZErr_rel_bins[-1]+(4.0-1.0)/nDiv)
    massZErr_rel_bins.append(5)
    '''
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/'
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/'
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut/'
 
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/Data_2015D/'   
#    filename = 'DoubleLepton_m'+fs+'.root'
#2016MC
    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v1_20170222/'
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/Data_2016_v1_20170223/'

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


#plotBinInfo = '100 80 100'
plotBinInfo = '300 60 120'
plotpath = '/home/mhl/public_html/2017/20170306_checkZPeak_mumu/'

singleCB_tail_mu = '1.583 1.086' #first is alpha, second is n of singleCB
singleCB_tail_e = '1.1443 2.5964' #first is alpha, second is n of singleCB
doubleCB_tail_e = '1 2.13 1.262 50'

pTErrCorrections_mu = '1.251 1.292 1.117 1'
pTErrCorrections_e = '1.245 1.140 1.077 1.178'

ZWidth = 2.44
#ZWidth = 2.49

doAllClosure('2mu', plotpath, ZWidth, plotBinInfo, singleCB_tail_mu, pTErrCorrections_mu)
#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, singleCB_tail_e, pTErrCorrections_e)
#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, doubleCB_tail_e, pTErrCorrections_e)


