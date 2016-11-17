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
    parser.add_argument('--min', dest='min_relM2lErr', type=float, help='min for relMassZErr')
    parser.add_argument('--max', dest='max_relM2lErr', type=float, help='max for relMassZErr')
    parser.add_argument('--inpath', dest='inpath', type=str, help='')
    parser.add_argument('--filename', dest='filename', type=str, help='')
    parser.add_argument('--plotpath', dest='plotpath', type=str, help='')
    parser.add_argument('--outtxtName', dest='outtxtName', type=str, help='')
    parser.add_argument('--fs', dest='fs', type=str, help='')

    args = parser.parse_args()
    return args

args=ParseOption()

massZErr_rel_min = args.min_relM2lErr #0.006
massZErr_rel_max = args.max_relM2lErr #0.008

### move to previous level, open tree only once???
inputPath = args.inpath #'/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/HZZ4L_Mass/makeSlimTree/DY_2015MC_kalman_v4/'
inputFile = args.filename #'DYJetsToLL_M-50_kalman_v4_m2mu.root'
treeName = 'passedEvents'

savePath = args.plotpath #'/home/mhl/public_html/2016/20161020_mass/fitmassZ/'
### move to previous level

#saveName = 'massZ_relmZErr_' + str(massZErr_rel_min).replace('.','p') + '_' + str(massZErr_rel_max).replace('.','p') + '_' + args.fs
saveName = 'massZ_relmZErr_' + str(massZErr_rel_min) + '_' + str(massZErr_rel_max) + '_' + args.fs

cut = "massZ > 80 && massZ < 100 && \
       massZErr/massZ > " + str(massZErr_rel_min) + " && \
       massZErr/massZ < " + str(massZErr_rel_max)
#       massZErr > " + str(massZErr_rel_min) + " && \
#       massZErr < " + str(massZErr_rel_max)
#       massZErr/massZ > " + str(massZErr_rel_min) + " && \
#       massZErr/massZ < " + str(massZErr_rel_max)

plotParaConfig = \
{\
'binInfo': [100, 80, 100],
'vars1': ['massZ'],
'cuts1': ['1'], #
'weight1': ['1'],
'xTitle': 'massZ',
'yTitle': '',
'savePath': savePath,
'saveName': saveName, #
'latexNote1': str(massZErr_rel_min) + ' < #sigma_{2l}/m_{2l} < ' + str(massZErr_rel_max),
'pdfName': 'model'
#'pdfName': 'BWxCB'
}

#initialize to-be-saved fitted parameter 
fitResult = {'sigmaCB':0}

myFile = TFile(inputPath+inputFile,'READ')
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

print fitResult
selector = TSelector.GetSelector("MySelector.C")
myTree.Process(selector)

### should make following lines more clean ...
sigma_m2l = [fitResult['sigmaCB'], selector.massZErr_sum/selector.nEvents,\
                                 selector.massZErr_sum_corr/selector.nEvents]#,\
#                                 selector.massZErr_sum_rel/selector.nEvents,\
#                                 selector.massZErr_sum_rel_corr/selector.nEvents]

print ''
print sigma_m2l
sigma_m2l = [str(sigma_m2l[i]) for i in range(len(sigma_m2l))]

with open(args.outtxtName,'a') as myfile:
#     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + sigma_m2l[2] + ' ' + sigma_m2l[3] + ' ' + sigma_m2l[4] + '\n')
     myfile.write(sigma_m2l[0] + ' ' + sigma_m2l[1] + ' ' + sigma_m2l[2] + '\n')

