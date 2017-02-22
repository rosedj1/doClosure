import ROOT, sys, os, string, re
from ROOT import *
from array import array
   
from tdrStyle import *
setTDRStyle()
ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit.so')
    
#from paraConfigurations import *
    
import argparse
def ParseOption():
    
    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('-t', dest='tag', type=str, help='for each plot')
    args = parser.parse_args()
    return args
    
    args=ParseOption()
    

def MakeFitPlotFromTree(tree, paraConfig, fitResult):

#    tag = args.tag
#    tag = 'massZ_test'
#    paraConfig = paraConfigs[tag]
    
    #rootPath1 = paraConfig['rootPath1']
    #rootfile1 = paraConfig['rootfile1']
    #tree1 = paraConfig['tree1']
    binInfo = paraConfig['binInfo']
    vars1 = paraConfig['vars1']
    cuts1 = paraConfig['cuts1']
    weight1 = paraConfig['weight1']
    xTitle = paraConfig['xTitle']
    yTitle = paraConfig['yTitle']
    savePath = paraConfig['savePath']
    saveName = paraConfig['saveName']
    latexNote1 = paraConfig['latexNote1']
    pdfName = paraConfig['pdfName']
    doubleCB_a1 = paraConfig['doubleCB_a1']
    doubleCB_n1 = paraConfig['doubleCB_n1']
    doubleCB_a2 = paraConfig['doubleCB_a2']
    doubleCB_n2 = paraConfig['doubleCB_n2']
    floatTail = paraConfig['floatTail']
    
    #f1 = TFile(rootPath1 + rootfile1, 'READ')
    #t1 = f1.Get(tree1)
    
    hists1 = [ TH1F('hist1_'+str(i),'', binInfo[0], binInfo[1], binInfo[2]) for i in range(len(vars1)) ]
    
    HIST1 = TH1F('HIST1', '', binInfo[0], binInfo[1], binInfo[2])
    
    for i in range(len(vars1)):
        tree.Project(hists1[i].GetName(), vars1[i], weight1[i]+"*"+cuts1[i])
        if i == 0:
           HIST1 = hists1[0].Clone()
        else:
           HIST1.Add(hists1[i])
    
    w = RooWorkspace('w')
    
    xmin = binInfo[1]
    xmax = binInfo[2]
    
    w.factory('Gaussian::gauss(x[' + str(xmin) + ',' + str(xmax) + '],meanGauss[0,-1,1],sigmaGauss[0.01,0,0.015])')
    w.factory('BreitWigner::bw(x[' + str(xmin) + ',' + str(xmax) + '],meanBW[91.187],sigmaBW[2.4952])')#meanBW[91.2, 90, 92],sigmaBW[2.4,2,3])')
#    w.factory('BreitWigner::bw(x[' + str(xmin) + ',' + str(xmax) + '],meanBW[91.2, 90, 92],sigmaBW[2.4,2,3])')


    if floatTail:
       tmpWidth = paraConfig['doubleCB_width']
       w.factory('DoubleCB::doubleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
                                     meanDCB[125,120,130], sigmaDCB['+str(tmpWidth)+'], \
                                     alphaDCB[1,0,50], nDCB[1,0,50], alpha2[1,0,50], n2[1,0,50])')
    else:
       w.factory('DoubleCB::doubleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
                                     meanDCB[125,120,130], sigmaDCB[1,0,10], \
                                     alphaDCB['+str(doubleCB_a1)+'], nDCB['+str(doubleCB_n1)+'], alpha2['+str(doubleCB_a2)+'], n2['+str(doubleCB_n2)+'])')


#2016MC
#4e reco                               alphaDCB[0.895], nDCB[8.383], alpha2[2.238], n2[2.848])')
#4e refit                              alphaDCB[0.9629], nDCB[6.489], alpha2[2.067], n2[2.408])')

#2015MC
# 4 point of 4e refit                                 alphaDCB[1.112], nDCB[3.984], alpha2[2.338], n2[2.15])')
# 3 point of 4e refit                                 alphaDCB[0.9876], nDCB[4.394], alpha2[2.022], n2[3.256])')
# 3 point of 4e reco                                 alphaDCB[0.95], nDCB[4.23], alpha2[2.189], n2[3.04])')
# 2 point of 4mu reco                                 alphaDCB[1.315], nDCB[1.834], alpha2[2.53], n2[1.288])')
# 2 point of 2e2mu reco inclusive                                 alphaDCB[1.187], nDCB[2.369], alpha2[2.577], n2[1.258])')
# 2 point of 2e2mu refit inclusive                                alphaDCB[1.237], nDCB[2.482], alpha2[2.363], n2[1.873])')


#                                 alphaDCB['+str(doubleCB_a1)+'], nDCB['+str(doubleCB_n1)+'], alpha2['+str(doubleCB_a2)+'], n2['+str(doubleCB_n2)+'])')
#                                 alphaDCB[1,0,10], nDCB['+str(doubleCB_n1)+'], alpha2[1,0,10], n2['+str(doubleCB_n2)+'])')
#                                  alphaDCB[1,0,50], nDCB['+str(doubleCB_n1)+'], alpha2[1,0,50], n2['+str(doubleCB_n2)+'])')
#                                  alphaDCB['+str(doubleCB_a1)+'], nDCB['+str(doubleCB_n1)+'], alpha2['+str(doubleCB_a2)+'], n2['+str(doubleCB_n2)+'])')
#                                  alphaDCB[1,0,50], nDCB[1,0,50], alpha2[1,0,50], n2[1,0,50])')
 

    w.factory('CBShape::singleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
                                meanCB[0,-1.5,1.5], sigmaCB[0.1,0,10], alphaCB[5,1,10], nCB[5,0,30])')

    w.factory('Polynomial::poly3(x,{a0[1, -10,10],a1[0.1, -10,10],a2[0.1, -10,10],a3[1, -10,10]})')

    w.factory("Exponential::bkg(expr('a2*a2*x+a1*x', x,a1,a2), tau[0.1,-1,1])")
    w.factory("Exponential::exp(expr('a3*a3*a3*x+a2*a2*x+a1*x+a0', x,a0,a1,a2,a3),a[-1, -2, 0])")
    
    w.var('x').setBins(1000, 'fft')
    w.factory('FCONV::BWxCB(x,bw,singleCB)')
    w.factory('FCONV::BWxDCB(x,bw,doubleCB)')

    w.factory('SUM:BWplusEXP(f1[0,1]*bw, exp)')
    w.factory('SUM:BWplusPOLY3(f1[0,1]*bw, poly3)')

    w.factory('SUM:model(fsig[0.9,0.7,1]*BWxCB, bkg)')
    
    dataHist1 = RooDataHist('dataHist1', 'dataHist1', RooArgList(w.var('x')), HIST1, 1)
    pdf = w.pdf(pdfName)
    fFit = pdf.fitTo(dataHist1,RooFit.Save(kTRUE))#, RooFit.PrintLevel(-1))

    xframe = w.var('x').frame(RooFit.Title(xTitle))
    
    dataHist1.plotOn(xframe, RooFit.MarkerStyle(20), RooFit.MarkerColor(1))
    pdf.plotOn(xframe, RooFit.LineColor(4), RooFit.LineWidth(2) )
    pdf.paramOn(xframe, RooFit.Layout(0.17, 0.4, 0.9), RooFit.Format("NE", RooFit.FixedPrecision(4)))

#    fitResult['sigma'] = w.var('sigmaCB').getVal()
    
    c1 = TCanvas("c1", "c1", 800, 800)

#    c1.SetLogy()    
    dummy = TH1D("dummy","dummy",1,binInfo[1],binInfo[2])
    dummy.SetMinimum(0)
    yMax1 = HIST1.GetMaximum()*1.5
    yMax = yMax1
    dummy.SetMaximum(yMax)
    dummy.SetLineColor(0)
    dummy.SetMarkerColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.GetYaxis().SetTitle(yTitle)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitle(xTitle)
    dummy.Draw()
    
    xframe.Draw('same')
    chi2 = xframe.chiSquare(fFit.floatParsFinal().getSize())
    dof =  fFit.floatParsFinal().getSize()
    
    legend = TLegend(0.15,0.9,0.42,0.95)
    #legend.AddEntry(HIST2, legend2, 'l')
    legend.SetTextSize(0.03)
    legend.SetLineWidth(2)
    legend.SetFillColor(0)
    legend.SetBorderSize(1)
    #legend.Draw('SAME')
    
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.65*c1.GetTopMargin())
    latex.SetTextFont(42)
    latex.SetTextAlign(11)
    latex.DrawLatex(0.18, 0.45, latexNote1)
    latex.DrawLatex(0.6, 0.3, "#chi^{2}/DOF = %.3f" %(chi2/dof))

    c1.SaveAs(savePath+saveName+'.png')
    c1.SaveAs(savePath+saveName+'.pdf')

    #more optimal way is to save all variables in workspace in dictionary and pass to ouside
    fitResult['sigmaCB'] = w.var('sigmaCB').getVal()
    fitResult['sigmaDCB'] = w.var('sigmaDCB').getVal()
    fitResult['sigmaDCB_err'] = w.var('sigmaDCB').getError()
    fitResult['alphaDCB'] = w.var('alphaDCB').getVal()
    fitResult['alphaDCB_err'] = w.var('alphaDCB').getError()
    fitResult['nDCB'] = w.var('nDCB').getVal()
    fitResult['nDCB_err'] = w.var('nDCB').getError()
    fitResult['alpha2'] = w.var('alpha2').getVal()
    fitResult['alpha2_err'] = w.var('alpha2').getError()
    fitResult['n2'] = w.var('n2').getVal()
    fitResult['n2_err'] = w.var('n2').getError()
    fitResult['meanDCB'] = w.var('meanDCB').getVal()
    fitResult['meanDCB_err'] = w.var('meanDCB').getError()

