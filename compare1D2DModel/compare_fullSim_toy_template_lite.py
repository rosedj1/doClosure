from ROOT import *
from array import array
from tdrStyle import *
setTDRStyle()
import sys
ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
ROOT.gSystem.Load("$CMSSW_BASE/lib/slc6_amd64_gcc481/libHiggsAnalysisCombinedLimit.so")
ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
ROOT.gSystem.AddIncludePath("-Iinclude/")

def GetHistFromTree(fullSimPath, fullSimTree, varFullSimName, rooVar, rooVarName, binInfo, cut, w):
    f_fullSim = TFile(fullSimPath + fullSimTree, 'READ')
    tree = f_fullSim.Get("passedEvents")
    weight = "1"
    histName_fullSim = (fullSimTree.split(".")[0]) + "_fullSim"
    hist_fullSim = TH1F(histName_fullSim, histName_fullSim, binInfo[0], binInfo[1], binInfo[2])
    tree.Project(hist_fullSim.GetName(), varFullSimName, weight+"*"+cut )
#    hist_fullSim.SetDirectory(0) #keep TH1F after function finish (https://root.cern.ch/phpBB3/viewtopic.php?t=17640)
    rooVar = w.var(rooVarName)    
    dataHist_fullSim = RooDataHist('dataHist_fullSim', 'dataHist_fullSim', RooArgList(rooVar), hist_fullSim, 1)
    getattr(w,'import')(hist_fullSim, 'hist_fullSim')
    getattr(w,'import')(dataHist_fullSim)
    print tree.GetEntries(), hist_fullSim.GetEntries(), cut
#    sys.exit()

def GetHistFromToy(toyPath, toy, varName, binInfo, norm, w):
    f_toy = TFile(toyPath + toy,'READ')
    w_toy = f_toy.Get("w")
    d_toy = w_toy.data("toy_total")
    rooVar = w.var(varName)
    hist_toy = RooAbsData.createHistogram(d_toy,'toy',rooVar,RooFit.Binning(binInfo[0], binInfo[1], binInfo[2]))
#normalize it accoriding to dataHist_fullSim
    hist_toy.Scale(1/hist_toy.Integral()*norm)
    dataHist_toy = RooDataHist('dataHist_toy', 'dataHist_toy', RooArgList(rooVar), hist_toy, 1)
    getattr(w,'import')(dataHist_toy)

def GetTemplate(templatePath, template, pdfName, w):
    f_template = TFile(templatePath + template, 'READ')
    w_template = f_template.Get('w')
    pdf = w_template.pdf(pdfName)
    getattr(w,'import')(pdf) 

def PrepareFrameForPlot(w, path, fileName, varName, binInfo, cut):

###
#    w.factory('DoubleCB::doubleCB(CMS_zz4l_mass[125, 105, 140], \
#                                  meanDCB[124,120,130], sigmaDCB[0.1,0,10], \
#                                  alphaDCB[1.1,0,50], nDCB[10,0,50], alpha2[1.1,0,50], n2[10,0,50])')

    w.factory('DoubleCB::doubleCB(CMS_zz4l_mass[125, 105, 140], \
                                  meanDCB[124.765], sigmaDCB[1.064], \
                                  alphaDCB[1.287], nDCB[1.96], alpha2[1.89], n2[2.78])')
    w.factory('Gaussian::gauss(CMS_zz4l_massErr[100,0,0.1], meanGauss[0.01, 0, 0.05], sigmaGauss[0.01,0,0.05])')
    w.factory('Landau::landau(CMS_zz4l_massErr, meanLandau[0.01,0.005,0.05], sigmaLandau[0.01, 0,0.05])')
    w.factory('SUM:gauss_plus_landau(f1[0,1]*landau,gauss)')
###

#get path
    fullSimPath = path['fullSim']
    toyPath = path['toy']
    templatePath = path['template']
#get fileName
    fullSimTree = fileName['fullSim']
    toy = fileName['toy']
    template = fileName['template']
#get var name
    rooVarName = varName['rooVarName']
    varFullSimName = varName['varFullSimName']
    pdfName = varName['pdfName']
#put rooVar in workspace
    rooVar = RooRealVar(rooVarName, rooVarName, binInfo[1], binInfo[2])
    getattr(w,'import')(rooVar)
#get data from fullSim
    w.Print()
    GetHistFromTree(fullSimPath, fullSimTree, varFullSimName, rooVar, rooVarName, binInfo, cut, w)
    dataHist_fullSim = w.data("dataHist_fullSim")
#get data from toy
    norm = dataHist_fullSim.sumEntries()
    GetHistFromToy(toyPath, toy, rooVarName, binInfo, norm, w)
    dataHist_toy = w.data("dataHist_toy")
#get pdf from template
    GetTemplate(templatePath, template, pdfName, w)
    model = w.pdf(pdfName)
#x axis
    rooVarFrame = rooVar.frame()
#plot on frame
    dataHist_fullSim.plotOn(rooVarFrame, RooFit.MarkerStyle(20), RooFit.MarkerColor(1), RooFit.Name("FullSim"))
    model.plotOn(rooVarFrame, RooFit.LineColor(2), RooFit.LineWidth(2), RooFit.Name("PDF"))
#    dataHist_toy.plotOn(rooVarFrame, RooFit.MarkerStyle(21), RooFit.MarkerColor(4), RooFit.Name("Toy"))

###
    w.Print()
#    w.pdf("doubleCB").fitTo(dataHist_fullSim)
    w.pdf("gauss_plus_landau").fitTo(dataHist_fullSim)
#    w.pdf("doubleCB").plotOn(rooVarFrame, RooFit.LineColor(4), RooFit.LineWidth(2) )
#    w.pdf("gauss_plus_landau").plotOn(rooVarFrame, RooFit.LineColor(4), RooFit.LineWidth(2) )
#    w.pdf("gauss_plus_landau").paramOn(rooVarFrame, RooFit.Layout(0.17, 0.3, 0.9), RooFit.Format("NE", RooFit.FixedPrecision(2)))
###
    getattr(w, 'import')(rooVarFrame, "rooVarFrame")
#    w.Print()

def MakeComparePlot_1D(w, binInfo, xTitle, yTitle, saveName):
    #canvas and frame
    c1 = TCanvas("c1", "c1", 800, 800)
    c1.SetGrid()
#    c1.SetLogy()
    dummy = TH1D("dummy","dummy",1,binInfo[1],binInfo[2])
    dummy.SetMinimum(0)
    yMax = w.genobj('hist_fullSim').GetMaximum()*1.5
    dummy.SetMaximum(yMax)
    dummy.SetLineColor(0)
    dummy.SetMarkerColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.GetYaxis().SetTitle(yTitle)
    dummy.GetYaxis().SetTitleOffset(1.42)
    dummy.GetXaxis().SetTitle(xTitle)
    dummy.Draw()
    #plot
    rooVarFrame = w.genobj("rooVarFrame")
    rooVarFrame.Draw('same')
    #legend
    legend = ROOT.TLegend(0.76,0.35,0.9,0.5)
    legend.AddEntry(rooVarFrame.findObject("FullSim"), 'FullSim', 'pe1')
#    legend.AddEntry(rooVarFrame.findObject("Toy"), 'Toy', 'pe1')
    legend.AddEntry(rooVarFrame.findObject("PDF"), 'Model', 'l')
    legend.SetTextSize(0.03)
    legend.SetLineWidth(2)
    legend.SetFillColor(0)
    legend.SetBorderSize(1)
    legend.Draw('SAME')
    c1.SaveAs("/home/mhl/public_html/2017/20170203_Hmass_4e/"+saveName+".png")

#fullSimPath = "/cms/data/store/user/t2/users/mhl/"
#fullSimPath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/Mass_2015MC/Fit_PereventMerr/"
fullSimPath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/liteUFHZZ4LAnalyzer/Ntuples/"
toyPath = "/raid/raid9/mhl/HZZ4L_Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP3_mergedToys_BkgSmear1pct4mu_FixShape_FixZX/"

#templatePath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/Mass_2015MC/CreateDatacards_Moriond2016_JES_v0_dev_ZJetsOn_10fb_1_ggHOnly_relativeError_getEBEusingFittedBWMeanSigma/cards_sm13_1Debe_refit_2p7fb_CB/HCG/125/"
#templatePath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/Mass_2015MC/CreateDatacards_Moriond2016_JES_v0_dev_ZJetsOn_10fb_1_ggHOnly_relativeError_getEBEusingFittedBWMeanSigma/cards_sm13_1Debe_reco_2p7fb_CB/HCG/125/"

#templatePath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/Mass_2015MC/CreateDatacards_Moriond2016_JES_v0_dev_ZJetsOn_10fb_1_ggHOnly_relativeError_test/cards_sm13_1D_refit_2p7fb_CB/HCG/125/"

templatePath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/doMeasurement/CreateDatacards_Moriond17_eOnly_20170201/cards_sm13_1Debe_refit_2p7fb_CB/HCG/125/"
#templatePath = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/doMeasurement/CreateDatacards_test_allFinalStates_v1/cards_sm13_1Debe_reco_2p7fb_CB/HCG/125/"

#fullSimTree = "ggH_2015MC_mH125.root"
fullSimTree = "ggH125_2016MC.root"
toy = "hzz4l_4muS_13TeV_1D_refit_withToys.input.root"
template = "hzz4l_4eS_13TeV.input.root"

rooVarName = "CMS_zz4l_massErr"
#varFullSimName = "mass4l"
#varFullSimName = "mass4lREFIT"
#pdfName = "ggH_hzz"
#rooVarName = "CMS_zz4l_massErr"
varFullSimName = "mass4lErrREFIT/mass4lREFIT"
#varFullSimName = "mass4lErr/mass4l"
pdfName = "pdfErrS_2"

cut = "passedFullSelection && finalState == 2 && mass4l > 105 && mass4l < 140"

xTitle = varFullSimName#"mass4lREFIT"
yTitle = ""
saveName = "compare_mass4lErr_model_4e_refit"
#saveName = "compare_mass4lErr_model_2e2mu_reco"

path = {'fullSim': fullSimPath, 'toy': toyPath, 'template': templatePath}
fileName = {'fullSim': fullSimTree, 'toy': toy, 'template': template}
varName = {'rooVarName': rooVarName, 'varFullSimName':varFullSimName, 'pdfName':pdfName}

binInfo = [50, 0.00, 0.1]

w = RooWorkspace("w")
PrepareFrameForPlot(w, path, fileName, varName, binInfo, cut)
MakeComparePlot_1D(w, binInfo, xTitle, yTitle, saveName)

