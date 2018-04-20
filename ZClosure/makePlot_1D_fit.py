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
    #pdfName = paraConfig['pdfName']
    #w = paraConfig['workspace']
    pdf = paraConfig['pdf']

#    Z_width = paraConfig['z_width'] 
#    singleCB_a = paraConfig['singleCB_a']
#    singleCB_n = paraConfig['singleCB_n']
#    doubleCB_a1 = paraConfig['doubleCB_a1']
#    doubleCB_n1 = paraConfig['doubleCB_n1']
#    doubleCB_a2 = paraConfig['doubleCB_a2']
#    doubleCB_n2 = paraConfig['doubleCB_n2']

    #f1 = TFile(rootPath1 + rootfile1, 'READ')
    #t1 = f1.Get(tree1)
    
    hists1 = [ TH1F('hist1_'+str(i),'', int(binInfo[0]), binInfo[1], binInfo[2]) for i in range(len(vars1)) ]
    
    HIST1 = TH1F('HIST1', '', int(binInfo[0]), binInfo[1], binInfo[2])
    
    for i in range(len(vars1)):
        tree.Project(hists1[i].GetName(), vars1[i], weight1[i]+"*"+cuts1[i])
        if i == 0:
           HIST1 = hists1[0].Clone()
        else:
           HIST1.Add(hists1[i])
    
    '''
    w = RooWorkspace('w')
    
    xmin = binInfo[1]
    xmax = binInfo[2]
     
    w.factory('Gaussian::gauss(x[' + str(xmin) + ',' + str(xmax) + '],meanGauss[0,-1,1],sigmaGauss[0.01,0,0.015])')
    #w.factory('BreitWigner::bw(x[' + str(xmin) + ',' + str(xmax) + '],meanBW[91.19],sigmaBW['+str(Z_width)+'])')#meanBW[91.2, 90, 92],sigmaBW[2.4,2,3])')
    w.factory('BreitWigner::bw(x[' + str(xmin) + ',' + str(xmax) + '],meanBW[91.1876],sigmaBW[2.44])')
    w.factory('DoubleCB::doubleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
                                 meanDCB[0,-1,1], sigmaDCB[0.01,0,10], \
                                 alphaDCB[1.1,0,50], nDCB[1,0,50], alpha2[1.1,0,50], n2[1,0,50])')
    
    w.factory('DoubleCB::doubleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
                                 meanDCB[90,80,100], sigmaDCB[1,0,10], \
                                 alphaDCB[1.1,0,50], nDCB[1,0,50], alpha2[1.1,0,50], n2[1,0,50])')
     
    #w.factory('DoubleCB::doubleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
    #                          meanDCB[0,-5,5], sigmaDCB[1, 0, 5], \
    #                          alphaDCB[1,0,20], nDCB[50,0,100], alpha2[1,0,20], n2[50,0,100])')
    #                          alphaDCB['+str(doubleCB_a1)+'], nDCB[1,0,50], alpha2['+str(doubleCB_a2)+'], n2[1,0,50])')
    #                          alphaDCB[1,0,10], nDCB['+str(doubleCB_n1)+'], alpha2[1,0,10], n2['+str(doubleCB_n2)+'])')
    #                          alphaDCB['+str(doubleCB_a1)+'], nDCB['+str(doubleCB_n1)+'], alpha2['+str(doubleCB_a2)+'], n2['+str(doubleCB_n2)+'])')
    #                          alphaDCB[1,0,10], nDCB[1,0,10], alpha2[1,0,10], n2[1,0,50])')

    #w.factory('CBShape::singleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
    #                            meanCB[0, -1.5, 1.5], sigmaCB[0.5,0.1,10], alphaCB['+str(singleCB_a)+'], nCB['+str(singleCB_n)+'])')
    #w.factory('CBShape::singleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
    #                            meanCB[0,-1.5,1.5], sigmaCB[1,0.1,10], alphaCB[1,0,10], nCB[1,0,100])')
    w.factory('CBShape::singleCB(x[' + str(xmin) + ',' + str(xmax) + '], \
                                meanCB[90,80,100], sigmaCB[1,0,3], alphaCB[1,0,10], nCB[1,0,100])')

    w.factory('Polynomial::poly3(x,{a0[1, -10,10],a1[0.1, -10,10],a2[0.1, -10,10],a3[1, -10,10]})')

    #w.factory("Exponential::bkg(x, tau[-0.03])")#tau[0.1,-1,1])")
    w.factory("Exponential::bkg(x, tau[0,-10,10])")

    w.factory("Exponential::exp(expr('a3*a3*a3*x+a2*a2*x+a1*x+a0', x,a0,a1,a2,a3),a[-1, -2, 0])")
    

    w.factory('FCONV::BWxCB(x,bw,singleCB)')
    w.factory('FCONV::BWxDCB(x,bw,doubleCB)')

    w.factory('SUM:BWplusEXP(f1[0,1]*bw, exp)')
    w.factory('SUM:BWplusPOLY3(f1[0,1]*bw, poly3)')

    #w.factory('SUM:model(fsig[0.9,0.7,1]*BWxCB, bkg)')
    w.factory('SUM:model(fsig[0.9,0.7,0.999]*BWxDCB, bkg)')
    '''


    dataHist1 = RooDataHist('dataHist1', 'dataHist1', RooArgList(w.var('x')), HIST1, 1)
    #pdf = w.pdf(pdfName)
    fFit = pdf.fitTo(dataHist1)#, RooFit.PrintLevel(-1))
    
    xframe = w.var('x').frame(RooFit.Title(xTitle))
    
    dataHist1.plotOn(xframe, RooFit.MarkerStyle(20), RooFit.MarkerColor(1))
    pdf.plotOn(xframe, RooFit.LineColor(4), RooFit.LineWidth(2))
    pdf.plotOn(xframe, RooFit.LineColor(2), RooFit.LineWidth(2),RooFit.Components("bkg"), RooFit.LineStyle(kDashed))
    pdf.paramOn(xframe, RooFit.Layout(0.17, 0.4, 0.9), RooFit.Format("NE", RooFit.FixedPrecision(4)))

    c1 = TCanvas("c1", "c1", 800, 800)
#    c1.SetLogy()    
    dummy = TH1D("dummy","dummy",1,xmin,xmax)
    dummy.SetMinimum(0.1)
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
    latex.DrawLatex(0.3, 0.15, latexNote1)
    c1.SaveAs(savePath+saveName+'.png')
    c1.SaveAs(savePath+saveName+'.pdf')

    #more optimal way is to save all variables in workspace in dictionary and pass to ouside
#    fitResult['sigmaCB'] = w.var('sigmaCB').getVal()/(91.2+w.var('meanCB').getVal())
#    fitResult['sigmaDCB'] = w.var('sigmaDCB').getVal()
#    fitResult['sigmaCB_err'] = w.var('sigmaCB').getError()/(91.2+w.var('meanCB').getVal())

#    fitResult['sigmaCB'] = w.var('meanCB').getVal() + 91.19
#    fitResult['sigmaCB_err'] = w.var('meanCB').getError()
#    fitResult['sigmaCB'] = w.var('meanDCB').getVal() + 91.19
#    fitResult['sigmaCB_err'] = w.var('meanDCB').getError()
#    fitResult['para'] = w.var('meanBW').getVal() 
#    fitResult['para_err'] = w.var('meanBW').getError()
    fitResult['para'] = w.var('meanDCB').getVal() 
    fitResult['para_err'] = w.var('meanDCB').getError()


   
