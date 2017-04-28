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

idLep = 13
if args.fs == "2e":
   idLep = 11

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

myTree.AddFriend("passedEvents", friendTree)
myTree.Draw(">>myList", cut, "entrylist")
entryList = gDirectory.Get("myList")
myTree.SetEntryList(entryList)

makePlot_1D_fit.MakeFitPlotFromTree(myTree, plotParaConfig, fitResult)

sigma_m2l = [fitResult['para'], fitResult['para_err']]
sigma_m2l = [str(sigma_m2l[i]) for i in range(len(sigma_m2l))]

with open(args.outtxtName,'a') as myfile:
     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + str(cut_min) + ' ' + str(cut_max) + '\n')
