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
    dataHist_toy.plotOn(rooVarFrame, RooFit.MarkerStyle(21), RooFit.MarkerColor(4), RooFit.Name("Toy"))
    getattr(w, 'import')(rooVarFrame, "rooVarFrame")
#    w.Print()

def MakeComparePlot_1D(w, binInfo, xTitle, yTitle, saveName):
    #canvas and frame
    c1 = TCanvas("c1", "c1", 800, 800)
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
    legend = ROOT.TLegend(0.2,0.75,0.45,0.9)
    legend.AddEntry(rooVarFrame.findObject("FullSim"), 'FullSim', 'pe1')
    legend.AddEntry(rooVarFrame.findObject("Toy"), 'Toy', 'pe1')
    legend.AddEntry(rooVarFrame.findObject("PDF"), 'Model', 'l')
    legend.SetTextSize(0.03)
    legend.SetLineWidth(2)
    legend.SetFillColor(0)
    legend.SetBorderSize(1)
    legend.Draw('SAME')
    c1.SaveAs("/home/mhl/public_html/2016/20160906_mass/"+saveName+".png")


fullSimPath = "/raid/raid9/mhl/HZZ4L_Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/inputTrees/"
toyPath = "/raid/raid9/mhl/HZZ4L_Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP3_mergedToys_BkgSmear1pct4mu_FixShape_FixZX/"
templatePath = toyPath

fullSimTreeName = {'sig': 'mH_125_', 'irrBkg': 'qqZZ_LowMassSkim_', 'redBkg': 'Data_2016_4lLowMassSkim_'}
toyName = {'sig': 'withSigToys', 'irrBkg':'withQQZZToys', 'redBkg':'withZXToys', 'mass4l':'1D', 'mass4lErr':'1Debe'}

tag_refit = {'reco': '', 'refit': 'REFIT'}
tag_varName = {'mass4l': '', 'mass4lErr': 'Err'}
fullSimNames = {'mass4l_reco':'mass4l', 'mass4l_refit':'mass4lREFIT', 'mass4lErr_reco':'mass4lErr/mass4l', 'mass4lErr_refit':'mass4lErrREFIT/mass4lREFIT'}
pdfsName = {'sig_mass4l':'ggH_hzz', 'irrBkg_mass4l': 'bkg_qqzz', 'redBkg_mass4l': 'bkg_zjets', \
           'sig_mass4lErr': 'pdfErrS_', 'irrBkg_mass4lErr': 'pdfErr_qqzz_', 'redBkg_mass4lErr': 'pdfErr_ggzz_'}

tag_pdf_fs = {'mass4l_4mu': '', 'mass4l_4e': '', 'mass4l_2e2mu': '', \
          'mass4lErr_4mu': '1', 'mass4lErr_4e': '2', 'mass4lErr_2e2mu': '3'}

binning = {'mass4l':[100, 105, 140], 'mass4lErr':[100, 0, 0.1]}
finalStateCut = {'4mu':"finalState == 1", "4e":"finalState == 2", "2e2mu":"finalState > 2"}
unit = {'mass4l':'(GeV)', 'mass4lErr':''}

cut_process = {'sig':'passedZ4lSelection', 'irrBkg':'passedZ4lSelection', 'redBkg':'passedZXCRSelection && nZXCRFailedLeptons==2'}

for fs in ['4mu', '4e', '2e2mu']:
    for process in ['sig', 'irrBkg', 'redBkg']:
        for var in ['mass4l', 'mass4lErr']:
            for mass4lType in ['reco', 'refit']:

                fullSimTree = fullSimTreeName[process] + fs + 'Skim.root'
                toy = 'hzz4l_' + fs + 'S_13TeV_' + toyName[var] + '_' + mass4lType + '_' + toyName[process] + '.input.root'
                template = toy

                varFullSimName = fullSimNames[var+'_'+mass4lType]
                pdfName = pdfsName[process+'_'+var] + tag_pdf_fs[var+'_'+fs]
                rooVarName = "CMS_zz4l_mass" + tag_varName[var]

                cut = "(" + finalStateCut[fs] + " && " + cut_process[process] + " && mass4l" + tag_refit[mass4lType] + " > 105 && mass4l" + tag_refit[mass4lType] + " < 140)"
#                cut = "(" + finalStateCut[fs] + " && passedFullSelection && mass4l" + tag_refit[mass4lType] + " > 105 && mass4l" + tag_refit[mass4lType] + " < 140)"

                binInfo = binning[var]

                xTitle = var + unit[var]
                yTitle = "Events/"+str((binInfo[2]-binInfo[1])/float(binInfo[0])) + unit[var]

                w = RooWorkspace("w")

                path = {'fullSim': fullSimPath, 'toy': toyPath, 'template': templatePath}
                fileName = {'fullSim': fullSimTree, 'toy': toy, 'template': template}
                varName = {'rooVarName': rooVarName, 'varFullSimName':varFullSimName, 'pdfName':pdfName}

                PrepareFrameForPlot(w, path, fileName, varName, binInfo, cut)
                saveName = var + '_' + mass4lType + '_' + process + '_' + fs
                MakeComparePlot_1D(w, binInfo, xTitle, yTitle, saveName)

