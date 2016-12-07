from ROOT import *
import makePlot_1D_fit
#RooMsgService.instance().Print() 
#RooMsgService.instance().getStream(1).removeTopic(RooFit.ObjectHandling)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.DataHandling)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.Eval)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.Caching)
#RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--min', dest='min_m4lErr', type=float, help='min for relMassZErr')
    parser.add_argument('--max', dest='max_m4lErr', type=float, help='max for relMassZErr')
    parser.add_argument('--channel', dest='channel', type=str, help='channel')
    parser.add_argument('--inpath', dest='inpath', type=str, help='')
    parser.add_argument('--filename', dest='filename', type=str, help='')
    parser.add_argument('--plotpath', dest='plotpath', type=str, help='')
    parser.add_argument('--outtxtName', dest='outtxtName', type=str, help='')
    parser.add_argument('--doubleCB_tail',dest='doubleCB_tail', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--doREFIT', dest='doREFIT', action='store_true', default=False, help='doREFIT')
    
    args = parser.parse_args()
    return args

args=ParseOption()

m4lErr_min = args.min_m4lErr #0.006
m4lErr_max = args.max_m4lErr #0.008
inputPath = args.inpath #'/cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/Ana_ZZ4L/Ntuples/'
inputFile = args.filename #'mH_125.root'
treeName = 'passedEvents'
savePath = args.plotpath #'/home/mhl/public_html/2016/20161021_mass/fitmassH/'
saveName = 'mass4l_HErr_' + str(m4lErr_min).replace('.','p') + '_' + str(m4lErr_max).replace('.','p') + '_' + args.channel
if args.doREFIT:
   saveName += '_refit'
else:
   saveName += '_reco'
doubleCB_a1 = args.doubleCB_tail[0]
doubleCB_n1 = args.doubleCB_tail[1]
doubleCB_a2 = args.doubleCB_tail[2]
doubleCB_n2 = args.doubleCB_tail[3]

channelCut = {'4mu':'(finalState == 1)', '4e':'(finalState == 2)', '2e2mu':'(finalState > 2)'}

cut = "passedFullSelection && mass4l > 105 && mass4l < 140 && "
#cut = "nFSRPhotons == 0 && passedFullSelection && mass4l > 105 && mass4l < 140 && "

#       mass4lErr/mass4l > " + str(m4lErr_min) + " && \
#       mass4lErr/mass4l < " + str(m4lErr_max)
#       mass4lErrREFIT/mass4lREFIT > " + str(m4lErr_min) + " && \
#       mass4lErrREFIT/mass4lREFIT < " + str(m4lErr_max)

if args.doREFIT:
   cut += "mass4lErrREFIT/mass4lREFIT > " + str(m4lErr_min) + " &&  mass4lErrREFIT/mass4lREFIT < " + str(m4lErr_max)   
else:
   cut += "mass4lErr/mass4l > " + str(m4lErr_min) + " &&  mass4lErr/mass4l < " + str(m4lErr_max)
#   cut += "mass4lErr > " + str(m4lErr_min) + " &&  mass4lErr < " + str(m4lErr_max)

cut += ' && ' + channelCut[args.channel]

plotParaConfig = \
{\
'binInfo': [100, 105, 140],
#'vars1': ['mass4l'],
#'vars1': ['mass4lREFIT'],
'cuts1': ['1'], #
'weight1': ['1'],
#'xTitle': 'mass4l(GeV)',
'yTitle': '',
'savePath': savePath,
'saveName': saveName, #
#'latexNote1': str(m4lErr_min) + ' < #sigma_{m4l}/m_{4l} < ' + str(m4lErr_max),
'pdfName': 'doubleCB',
'doubleCB_a1': doubleCB_a1,
'doubleCB_n1': doubleCB_n1,
'doubleCB_a2': doubleCB_a2,
'doubleCB_n2': doubleCB_n2
}

if args.doREFIT:
   plotParaConfig['vars1'] = ['mass4lREFIT']
   plotParaConfig['xTitle'] = 'mass4lREFIT(GeV)'
   plotParaConfig['latexNote1'] =  str(m4lErr_min) + ' < #sigma_{m4lREFIT}/m_{4lREFIT} < ' + str(m4lErr_max)
else:
   plotParaConfig['vars1'] = ['mass4l']
   plotParaConfig['xTitle'] = 'mass4l(GeV)'
   plotParaConfig['latexNote1'] =  str(m4lErr_min) + ' < #sigma_{m4l}/m_{4l} < ' + str(m4lErr_max)

#initialize to-be-saved fitted parameter 
fitResult = {'sigmaCB':0, 'sigmaDCB':0}

myFile = TFile(inputPath+inputFile,'READ')
myTree = myFile.Get(treeName)

#TProof.Open("")
#c = TChain("myTree")
#c.Draw(">>myList", cut, "entrylist")

#select part of tree to be used
myTree.Draw(">>myList", cut, "entrylist")
entryList = gDirectory.Get("myList")
myTree.SetEntryList(entryList)

myList.Print()

#plot and fit massZ, get fitted sigma
makePlot_1D_fit.MakeFitPlotFromTree(myTree, plotParaConfig, fitResult)

print fitResult
selector = TSelector.GetSelector("MySelector_m4l.C")
myTree.Process(selector)

#corred m4l = selector.mass4lErr

### should make following lines more clean ...
sigma_m4l = [fitResult['sigmaDCB'], fitResult['sigmaDCB_err'], \
             selector.mass4lErr_uncorr_sum/selector.nEvents,\
             selector.mass4lErr_corr_sum/selector.nEvents, \
             selector.mass4lErrREFIT_corr_sum/selector.nEvents]#,\
#                                 selector.massZErr_sum_rel/selector.nEvents,\
#                                 selector.massZErr_sum_rel_corr/selector.nEvents]
print ''
print sigma_m4l
sigma_m4l = [str(sigma_m4l[i]) for i in range(len(sigma_m4l))]

with open(args.outtxtName,'a') as myfile:
     myfile.write(sigma_m4l[0] + ' ' + sigma_m4l[1] + ' ' + sigma_m4l[2] + ' ' + sigma_m4l[3] + ' ' + sigma_m4l[4] + '\n')
with open(args.outtxtName+'para.txt','a') as myfile:
   if args.max_m4lErr < 1:
     myfile.write(str(args.min_m4lErr) + ' ' + str(args.max_m4lErr) + ' ' + str(fitResult['alphaDCB']) + ' ' + str(fitResult['nDCB']) + ' ' + str(fitResult['alpha2']) + ' ' + str(fitResult['n2']) + '\n')
     myfile.write(str(args.min_m4lErr) + ' ' + str(args.max_m4lErr) + ' ' + str(fitResult['alphaDCB_err']) + ' ' + str(fitResult['nDCB_err']) + ' ' + str(fitResult['alpha2_err']) + ' ' + str(fitResult['n2_err']) + '\n')

