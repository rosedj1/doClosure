from subprocess import call
import time 

import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--isData', dest='isData', action='store_true', default=False, help='isData')
    parser.add_argument('--range',dest='range', nargs='+', help='', type=float)#, required=True)
    args = parser.parse_args()
    return args

def doAllClosure(fs, plotPath, Z_width, plotBinInfo, singleCB_tail, baseCutRange, isData, cutVar, cut_bins):

#    cut_bins = [5,100]
#    cut_bins = [5,20,30,40,50,60,100,200,300]
#    massZErr_rel_bins = [-2.4,-2.2,-1.8,-0.9,0,0.9,1.8,2.2,2.4]

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
       outtxtName = '../makeSummaryPlots/lepsacles/data_'+fs+'_' + str(baseCutRange[0]) + '_' + str(baseCutRange[1]) + '.txt'

    else:

#       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v1_20170222/'
#       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v3_20170312_afterApproval/'
#       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v1_20170427/'
#       filename = 'DYJetsToLL_M-50_kalman_v4_m'+fs+'.root'
       inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/liteUFHZZ4LAnalyzer/Ntuples/'
#       filename = 'ggH125_2016MC_20170223.root'
       filename = 'ZZTo4L_13TeV_powheg_pythia8_ext1_RunIISummer16MiniAODv2.root'
       outtxtName = '../makeSummaryPlots/lepsacles/mc_'+fs+'_' + str(baseCutRange[0]) + '_' + str(baseCutRange[1]) + '.txt'



    call('echo " " > ' + outtxtName, shell=True)

    for i in range(len(cut_bins)-1):

        cmd = 'python doClosure_mZ.py --min '+str(cut_bins[i])+' --max '+str(cut_bins[i+1]) + ' --cutVar ' + cutVar \
            + ' --inpath ' + inputpath \
            + ' --filename ' + filename \
            + ' --plotpath ' + plotpath \
            + ' --zWidth ' + str(Z_width) \
            + ' --plotBinInfo ' + plotBinInfo  \
            + ' --singleCB_tail ' + singleCB_tail \
            + ' --outtxtName ' + outtxtName + ' --fs ' + fs \
            + ' --minBasecut ' + str(baseCutRange[0]) + ' --maxBasecut ' + str(baseCutRange[1])

        if isData:
  
           cmd +=  ' --isData &'

        else:

           cmd += ' &'

        #    print cmd
        call(cmd, shell=True)

args=ParseOption()

baseCutRange = [(args.range)[0],(args.range)[1]]#[1.4,2.4]

#plotBinInfo = '100 80 100'
plotBinInfo = '100 -0.1 0.1'

isData = args.isData
#isData = False

ZWidth = 2.49
plotpath = ''
if isData:
   plotpath += '/home/mhl/public_html/2017/20170420_checkZPeak/mu/data_'+str(baseCutRange[0]).replace('.','p')+'_'+str(baseCutRange[1]).replace('.','p')+'_DCB_withBKG_randomCut/'
else:
#   plotpath += '/home/mhl/public_html/2017/20170420_checkZPeak/mu/mc_'+str(baseCutRange[0]).replace('.','p')+'_'+str(baseCutRange[1]).replace('.','p')+'_DCB_withBKG_randomCut_reco/'
#   plotpath = '/home/mhl/public_html/2017/20170420_checkZPeak/'
#   plotpath = '/home/mhl/public_html/2017/20170420_checkZPeak/mc_pTZ_reco/'
   plotpath = '/home/mhl/public_html/2017/20170427_checkZPeak/pTResidual_vs/Z4LSample/'
   ZWidth = 2.44

singleCB_tail_mu = '1.583 1.086' #first is alpha, second is n of singleCB
singleCB_tail_e = '1.1443 2.5964' #first is alpha, second is n of singleCB

cutVar = "pT_4th_muon"
#cut_bins = [5,20,30,40,50,60,100,200,300]
#cut_bins = [-2.4,-2.2,-1.8,-0.9,0,0.9,1.8,2.2,2.4]
cut_bins = [5,7,9,11,13,15,17,19]

doAllClosure('2mu', plotpath, ZWidth, plotBinInfo, singleCB_tail_mu, baseCutRange, isData, cutVar, cut_bins)
#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, singleCB_tail_e, pTErrCorrections_e, etaRange, isData)
