from subprocess import call
import time 

import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--isData', dest='isData', action='store_true', default=False, help='isData')
    args = parser.parse_args()
    return args

def doAllClosure(fs, plotPath, Z_width, plotBinInfo, singleCB_tail, pTErrCorrections, etaRange, isData):

#    massZErr_rel_bins = [5,15,25,35,40,45,55,65,100]
#    massZErr_rel_bins = [7,20,30,40,50,60,100]
#    massZErr_rel_bins = [5,15,20,25,30,35,40,45,50,55,60,65,100]

    massZErr_rel_bins = [-2.4,-2.2,-1.8,-0.9,0,0.9,1.8,2.2,2.4]
#    massZErr_rel_bins = [-2.4,-1.8,-1.4,-1.1,-0.9,0,0.9,1.1,1.4,1.8,2.4]
#    massZErr_rel_bins = [-2.4,-1.8]

#    massZErr_rel_bins = [7,15,25,35,40,50,100]
#    massZErr_rel_bins = [0,0.8,1.5,2,2.5]
#    massZErr_rel_bins = [-2.5,-2,-1.5,-1.2,-1,-0.8,0,0.8,1,1.2,1.5,2,2.4]

#    massZErr_rel_bins = [0,0.01,0.012,0.014,0.017,0.02,0.03,0.04,0.1]   
#    nDiv = 8
#    massZErr_rel_bins = [0,0.01]
#    for i in range(nDiv):
#       massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.025-0.01)/nDiv)
#    massZErr_rel_bins.append(0.03)
#    massZErr_rel_bins.append(0.04)
#    massZErr_rel_bins.append(0.1)
    

#2016 data and mc

    if isData:

#       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/Data_2016_v1_20170223/'
       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/Data_2016_v1_20170312_afterApproval/'
       filename = 'DoubleLepton_m'+fs+'.root'
       outtxtName = '../makeSummaryPlots/lepsacles/data_'+fs+'_' + str(etaRange[0]) + '_' + str(etaRange[1]) + '.txt'

    else:

#       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v1_20170222/'
       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v3_20170312_afterApproval/'
       filename = 'DYJetsToLL_M-50_kalman_v4_m'+fs+'.root'
       outtxtName = '../makeSummaryPlots/lepsacles/mc_'+fs+'_' + str(etaRange[0]) + '_' + str(etaRange[1]) + '.txt'



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
            + ' --outtxtName ' + outtxtName + ' --fs ' + fs \
            + ' --minEta ' + str(etaRange[0]) + ' --maxEta ' + str(etaRange[1]) 

        if isData:
  
           cmd +=  ' --isData &'

        else:

           cmd += ' &'

        #    print cmd
        call(cmd, shell=True)


#etaRange = [0.0,0.9]
#etaRange = [0.9,1.8]
#etaRange = [1.8,2.4]
etaRange = [5,100]
#etaRange = [7,100]
#etaRange = [0.0,2.5]
#etaRange = [0,0.1]
#mu
plotBinInfo = '50 80 100'
#e
#plotBinInfo = '100 70 110'
#m2muerr
#plotBinInfo = '60 75 105'

args=ParseOption()

isData = args.isData
#isData = False

ZWidth = 2.49
plotpath = ''
if isData:
   plotpath += '/home/mhl/public_html/2017/20170312_checkLepScale/mu/data_'+str(etaRange[0]).replace('.','p')+'_'+str(etaRange[1]).replace('.','p')+'_DCB_withBKG_randomCut/'
#   plotpath += '/home/mhl/public_html/2017/20170313_checkLepScale_vsM2lErr/e/data_vs_m2lerr/'
else:
   plotpath += '/home/mhl/public_html/2017/20170312_checkLepScale/mu/mc_'+str(etaRange[0]).replace('.','p')+'_'+str(etaRange[1]).replace('.','p')+'_DCB_withBKG_randomCut/'
#   plotpath += '/home/mhl/public_html/2017/20170313_checkLepScale_vsM2lErr/e/mc_vs_m2lerr/'
   ZWidth = 2.44

singleCB_tail_mu = '1.583 1.086' #first is alpha, second is n of singleCB
singleCB_tail_e = '1.1443 2.5964' #first is alpha, second is n of singleCB
pTErrCorrections_mu = '1.251 1.292 1.117 1'
pTErrCorrections_e = '1.245 1.140 1.077 1.178'

#ZWidth = 2.44
#ZWidth = 2.49



doAllClosure('2mu', plotpath, ZWidth, plotBinInfo, singleCB_tail_mu, pTErrCorrections_mu, etaRange, isData)
#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, singleCB_tail_e, pTErrCorrections_e, etaRange, isData)

#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, singleCB_tail_e, pTErrCorrections_e)
#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, doubleCB_tail_e, pTErrCorrections_e)


