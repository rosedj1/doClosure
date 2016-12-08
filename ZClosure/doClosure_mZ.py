from ROOT import *
import makePlot_1D_fit
from subprocess import call
#RooMsgService.instance().Print() 
#RooMsgService.instance().getStream(1).removeTopic(RooFit.ObjectHandling)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.DataHandling)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.Eval)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.Caching)
#RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--min', dest='min_relM2lErr', type=float, help='min for relMassZErr')
    parser.add_argument('--max', dest='max_relM2lErr', type=float, help='max for relMassZErr')
    parser.add_argument('--inpath', dest='inpath', type=str, help='')
    parser.add_argument('--filename', dest='filename', type=str, help='')
    parser.add_argument('--plotpath', dest='plotpath', type=str, help='')
    parser.add_argument('--outtxtName', dest='outtxtName', type=str, help='')
    parser.add_argument('--fs', dest='fs', type=str, help='')
    parser.add_argument('--zWidth', dest='Z_width', type=float, help='Z width in MC or pdg value')
    parser.add_argument('--plotBinInfo', dest='binInfo', nargs='+', help='', type=int)#, required=True)
    parser.add_argument('--singleCB_tail',dest='singleCB_tail', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--doubleCB_tail',dest='doubleCB_tail', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--pTErrCorrections', dest='pTErrCorrections', nargs='+', help='', type=float)#, required=True)

    args = parser.parse_args()
    return args

args=ParseOption()

massZErr_rel_min = args.min_relM2lErr 
massZErr_rel_max = args.max_relM2lErr 
inputPath = args.inpath 
inputFile = args.filename
treeName = 'passedEvents'
savePath = args.plotpath 
saveName = 'massZ_relmZErr_' + str(massZErr_rel_min) + '_' + str(massZErr_rel_max) + '_' + args.fs
binInfo = args.binInfo
singleCB_a = args.singleCB_tail[0]
singleCB_n = args.singleCB_tail[1]
#doubleCB_a1 = args.doubleCB_tail[0]
#doubleCB_n1 = args.doubleCB_tail[1]
#doubleCB_a2 = args.doubleCB_tail[2]
#doubleCB_n2 = args.doubleCB_tail[3]
pTErrCorrections = args.pTErrCorrections

cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
       massZErr/massZ > " + str(massZErr_rel_min) + " && \
       massZErr/massZ < " + str(massZErr_rel_max)

plotParaConfig = \
{\
'binInfo': binInfo,
'vars1': ['massZ'],
'cuts1': ['1'], #
'weight1': ['1'],
'xTitle': 'massZ',
'yTitle': '',
'savePath': savePath,
'saveName': saveName, #
'latexNote1': str(massZErr_rel_min) + ' < #sigma_{2l}/m_{2l} < ' + str(massZErr_rel_max),
'pdfName': 'model',
#'pdfName': 'BWxDCB',
'z_width': args.Z_width ,
'singleCB_a': singleCB_a,
'singleCB_n': singleCB_n,
#'doubleCB_a1': doubleCB_a1,
#'doubleCB_n1': doubleCB_n1,
#'doubleCB_a2': doubleCB_a2,
#'doubleCB_n2': doubleCB_n2
}

#initialize to-be-saved fitted parameter 
fitResult = {'sigmaCB':0, 'sigmaDCB':0}

myFile = TFile.Open(inputPath+inputFile,'READ')
myTree = myFile.Get(treeName)

#TProof.Open("")
#c = TChain("myTree")
#c.Draw(">>myList", cut, "entrylist")

#select part of tree to be used
myTree.Draw(">>myList", cut, "entrylist")
entryList = gDirectory.Get("myList")
myTree.SetEntryList(entryList)

#plot and fit massZ, get fitted sigma
makePlot_1D_fit.MakeFitPlotFromTree(myTree, plotParaConfig, fitResult)

#print fitResult
selector = TSelector.GetSelector("MySelector.C")
#tag = str(massZErr_rel_min) + '_' + str(massZErr_rel_max)
fs = args.fs
#call('cp LUT_' + fs + '.root tmpLUTs/LUT_' + fs + '_' + tag + '.root', shell=True)
selector.SetTag(fs)
#selector.SetPtErrCorrection(args.fs, pTErrCorrections[0], pTErrCorrections[1], pTErrCorrections[2], pTErrCorrections[3])
myTree.Process(selector)

### should make following lines more clean ...
sigma_m2l = [fitResult['sigmaCB'], fitResult['sigmaCB_err'],\
             selector.massZErr_sum/selector.nEvents,\
             selector.massZErr_sum_corr/selector.nEvents]#,\
#                                 selector.massZErr_sum_rel/selector.nEvents,\
#                                 selector.massZErr_sum_rel_corr/selector.nEvents]

print ''
print sigma_m2l
sigma_m2l = [str(sigma_m2l[i]) for i in range(len(sigma_m2l))]

with open(args.outtxtName,'a') as myfile:
#     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + sigma_m2l[2] + ' ' + sigma_m2l[3] + ' ' + sigma_m2l[4] + '\n')
     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + sigma_m2l[2] + ' ' + sigma_m2l[3] + '\n')

