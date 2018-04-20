from ROOT import *
import makePlot_1D_fit
from subprocess import call
import sys
#RooMsgService.instance().Print() 
#RooMsgService.instance().getStream(1).removeTopic(RooFit.ObjectHandling)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.DataHandling)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.Eval)
#RooMsgService.instance().getStream(1).removeTopic(RooFit.Caching)
#RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--min', dest='min_cut', type=float, help='min for cut')
    parser.add_argument('--max', dest='max_cut', type=float, help='max for cut')
    parser.add_argument('--inpath', dest='inpath', type=str, help='')
    parser.add_argument('--filename', dest='filename', type=str, help='')
    parser.add_argument('--plotpath', dest='plotpath', type=str, help='')
    parser.add_argument('--outtxtName', dest='outtxtName', type=str, help='')
    parser.add_argument('--fs', dest='fs', type=str, help='')
    parser.add_argument('--zWidth', dest='Z_width', type=float, help='Z width in MC or pdg value')
    parser.add_argument('--plotBinInfo', dest='binInfo', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--singleCB_tail',dest='singleCB_tail', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--doubleCB_tail',dest='doubleCB_tail', nargs='+', help='', type=float)#, required=True)
#    parser.add_argument('--pTErrCorrections', dest='pTErrCorrections', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--minBasecut', dest='min_basecut', type=float, help='base cut min')
    parser.add_argument('--maxBasecut', dest='max_basecut', type=float, help='base cut max')
    parser.add_argument('--isData', dest='isData', action='store_true', default=False, help='isData')
    parser.add_argument('--cutVar', dest='cutVar', type=str, help='')

    args = parser.parse_args()
    return args

args=ParseOption()

basecut_min = args.min_basecut
basecut_max = args.max_basecut
cut_min = args.min_cut 
cut_max = args.max_cut 
inputPath = args.inpath 
inputFile = args.filename
treeName = 'passedEvents'
savePath = args.plotpath 
cutVar = args.cutVar
saveName = cutVar + '_' + str(cut_min) + '_' + str(cut_max) + '_' + args.fs
binInfo = args.binInfo
singleCB_a = args.singleCB_tail[0]
singleCB_n = args.singleCB_tail[1]
#doubleCB_a1 = args.doubleCB_tail[0]
#doubleCB_n1 = args.doubleCB_tail[1]
#doubleCB_a2 = args.doubleCB_tail[2]
#doubleCB_n2 = args.doubleCB_tail[3]
#pTErrCorrections = args.pTErrCorrections

idLep = 13
if args.fs == "2e":
   idLep = 11
#etaLow = 0
#etaHigh = 0.9

#randomCut1 = "id1 == " + str(idLep)
#randomCut2 = "id2 == " + str(idLep)
#randomCut1 = "((pT1-int(pT1))+(eta2-int(eta2)))>((pT2-int(pT2))+(eta2-int(eta2)))"
#randomCut2 = "((pT1-int(pT1))+(eta2-int(eta2)))<((pT2-int(pT2))+(eta2-int(eta2)))"
#randomCut1 = "(pT1 < pT2)"
#randomCut2 = "(pT1 > pT2)"
randomCut1 = "(randomNum < 0.5)"
randomCut2 = "(randomNum > 0.5)"

#in different pt bin
'''
cut = "genzm > " + str(binInfo[1]) + " && genzm < " + str(binInfo[2]) + " && \
       ((" + randomCut1 + " && abs(genLep_eta1) > " + str(basecut_min) + " && abs(genLep_eta1) < " + str(basecut_max) + " && \
         genLep_pt1 > " + str(cut_min) +  " && genLep_pt1 < " + str(cut_max) +  " ) || \
        (" + randomCut2 + " && abs(genLep_eta2) > " + str(basecut_min) + " && abs(genLep_eta2) < " + str(basecut_max) + " && \
         genLep_pt2 > " + str(cut_min) +  " && genLep_pt2 < " + str(cut_max) + ") )"

cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
       ((" + randomCut1 + " && abs(eta1) > " + str(basecut_min) + " && abs(eta1) < " + str(basecut_max) + " && \
         pT1 > " + str(cut_min) +  " && pT1 < " + str(cut_max) +  " ) || \
        (" + randomCut2 + " && abs(eta2) > " + str(basecut_min) + " && abs(eta2) < " + str(basecut_max) + " && \
         pT2 > " + str(cut_min) +  " && pT2 < " + str(cut_max) + ") )"
cut = "genzm > " + str(binInfo[1]) + " && genzm < " + str(binInfo[2]) + " && \
       ((" + randomCut1 + " && abs(genLep_pt1) > " + str(basecut_min) + " && abs(genLep_pt1) < " + str(basecut_max) + " && \
         genLep_eta1 > " + str(cut_min) +  " && genLep_eta1 < " + str(cut_max) +  " ) || \
        (" + randomCut2 + " && abs(genLep_pt2) > " + str(basecut_min) + " && abs(genLep_pt2) < " + str(basecut_max) + " && \
         genLep_eta2 > " + str(cut_min) +  " && genLep_eta2 < " + str(cut_max) + ") )"
cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
       ((" + randomCut1 + " && abs(pT1) > " + str(basecut_min) + " && abs(pT1) < " + str(basecut_max) + " && \
         eta1 > " + str(cut_min) +  " && eta1 < " + str(cut_max) +  " ) || \
        (" + randomCut2 + " && abs(pT2) > " + str(basecut_min) + " && abs(pT2) < " + str(basecut_max) + " && \
         eta2 > " + str(cut_min) +  " && eta2 < " + str(cut_max) + ") )"
cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
       pTZ > " + str(cut_min) +  " && pTZ < " + str(cut_max) 
'''

cut = "pTGENL4 > " + str(cut_min) + " && pTGENL4 < " + str(cut_max) + " && finalState == 1 && mass4l > 70 && mass4l < 105 && passedFullSelection"
#cut = "genLep_pt2 > " + str(cut_min) + " && genLep_pt2 < " + str(cut_max) + " && massZ > 80 && massZ < 100"# && passedFullSelection"

#cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
#       (" + randomCut1 + " && abs(eta1) > " + str(basecut_min) + " && abs(eta1) < " + str(basecut_max) + " && \
#         (genLep_pt1 + genLep_pt2)/2> " + str(cut_min) +  " && (genLep_pt1+genLep_pt2)/2 < " + str(cut_max) +  " ) "


#in different absolute eta bin

'''
cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
       ((id1 == " + str(idLep) + " && pT1 > " + str(etaLow) + " && pT1 < " + str(etaHigh) + " && \
         abs(eta1) > " + str(massZErr_rel_min) +  " && abs(eta1) < " + str(massZErr_rel_max) +  " ) || \
        (id2 == " + str(idLep) + " && pT2 > " + str(etaLow) + " && pT2 < " + str(etaHigh) + " && \
         abs(eta2) > " + str(massZErr_rel_min) +  " && abs(eta2) < " + str(massZErr_rel_max) + ") )"
# 

cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
       ((" + randomCut1 + " && pT1 > " + str(etaLow) + " && pT1 < " + str(etaHigh) + " && \
         (eta1) > " + str(massZErr_rel_min) +  " && (eta1) < " + str(massZErr_rel_max) +  " ) || \
        (" + randomCut2 + " && pT2 > " + str(etaLow) + " && pT2 < " + str(etaHigh) + " && \
         (eta2) > " + str(massZErr_rel_min) +  " && (eta2) < " + str(massZErr_rel_max) + ") )"

#corrected m2l error
cut = "massZ > " + str(binInfo[1]) + " && massZ < " + str(binInfo[2]) + " && \
         massZErr_corr/massZ > " + str(massZErr_rel_min) +  " && massZErr_corr/massZ < " + str(massZErr_rel_max) 

plotParaConfig = \
{\
'binInfo': binInfo,
'vars1': ['genzm'],
'cuts1': ['1'], #
'weight1': ['1'],
'xTitle': 'genzm',
'yTitle': '',
'savePath': savePath,
'saveName': saveName, #
'latexNote1': str(cut_min) + ' < ' + cutVar + ' < ' + str(cut_max),
'pdfName': 'doubleCB',
#'pdfName': 'BWxDCB',
'z_width': args.Z_width ,
'singleCB_a': singleCB_a,
'singleCB_n': singleCB_n,
}
'''
plotParaConfig = \
{\
'binInfo': binInfo,
'vars1': ['(pTL4-pTGENL4)/pTGENL4'],
#'vars1': ['(pT2-genLep_pt2)/genLep_pt2'],
'cuts1': ['1'], #
'weight1': ['1'],
'xTitle': '(pT_{Reco}-pT_{Gen})/pT_{Gen}',
'yTitle': '',
'savePath': savePath, 
'saveName': saveName, #
'latexNote1': str(cut_min) + ' < ' + cutVar + ' < ' + str(cut_max),
'pdfName': 'doubleCB',
#'pdfName': 'BWxDCB',
'z_width': args.Z_width ,
'singleCB_a': singleCB_a,
'singleCB_n': singleCB_n,
}

#initialize to-be-saved fitted parameter 
fitResult = {'sigmaCB':0, 'sigmaDCB':0}

myFile = TFile.Open(inputPath+inputFile,'READ')
myTree = myFile.Get(treeName)

friendTree = "newtree_" + args.fs 
if args.isData:
   friendTree += "_data.root"
else:
   friendTree += "_mc.root"

#myFriend = TFile.Open(friendTree,'read')
#myTree1 = myFriend.Get(treeName)
#print friendTree
#myTree1.Print()
#sys.exit()   
myTree.AddFriend("passedEvents", friendTree)
#myTree.Scan("massErr:massErr_corr")
#sys.exit()
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
#selector = TSelector.GetSelector("MySelector.C")
#tag = str(massZErr_rel_min) + '_' + str(massZErr_rel_max)
fs = args.fs
#call('cp LUT_' + fs + '.root tmpLUTs/LUT_' + fs + '_' + tag + '.root', shell=True)
#selector.SetTag(fs)
#selector.SetPtErrCorrection(args.fs, pTErrCorrections[0], pTErrCorrections[1], pTErrCorrections[2], pTErrCorrections[3])
#myTree.Process(selector)

### should make following lines more clean ...
sigma_m2l = [fitResult['para'], fitResult['para_err']]
#             selector.massZErr_sum_rel/selector.nEvents,\
#             selector.massZErr_sum_rel_corr/selector.nEvents]
#             selector.massZErr_sum/selector.nEvents,\
#             selector.massZErr_sum_corr/selector.nEvents]#,\

print ''
print sigma_m2l
sigma_m2l = [str(sigma_m2l[i]) for i in range(len(sigma_m2l))]

with open(args.outtxtName,'a') as myfile:
#     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + sigma_m2l[2] + ' ' + sigma_m2l[3] + ' ' + sigma_m2l[4] + '\n')
     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + str(cut_min) + ' ' + str(cut_max) + '\n')

