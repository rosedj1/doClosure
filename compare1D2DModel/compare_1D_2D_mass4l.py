from ROOT import *
from array import array
from tdrStyle import *
setTDRStyle()
import sys
ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
ROOT.gSystem.Load("$CMSSW_BASE/lib/slc6_amd64_gcc481/libHiggsAnalysisCombinedLimit.so")
ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
ROOT.gSystem.AddIncludePath("-Iinclude/")

import argparse

def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--path', dest='path', type=str, default=False)
    parser.add_argument('--saveDir', dest='saveDir', type=str, default=False)

    args = parser.parse_args()
    return args

args=ParseOption()

binInfo = [100, 105,140]
CMS_zz4l_mass = RooRealVar('CMS_zz4l_mass','CMS_zz4l_mass',104,140)
CMS_zz4l_massErr = RooRealVar('CMS_zz4l_massErr','CMS_zz4l_massErr',0,0.1)
#w = RooWorkspace("w")

for m4lType in ['refit', 'reco']:
    for fs in ['4e','2e2mu','4mu']:
#for m4lType in ['reco']:
#    for fs in ['2e2mu']:

        path = args.path

        pdfPath1 = path + 'cards_sm13_1D_'+m4lType+'_2p7fb_CB/HCG/125/'
        pdfPath2 = path + 'cards_sm13_1Debe_'+m4lType+'_2p7fb_CB/HCG/125/'

        template1 = 'hzz4l_'+fs+'S_13TeV.input.root'
        template2 = 'hzz4l_'+fs+'S_13TeV.input.root'
        pdfName = 'ggH_hzz'
        pdfName_new_1 = 'ggH_hzz_1D'
        pdfName_new_2 = 'ggH_hzz_2D'
        #get pdf from workspace
        f1 = TFile(pdfPath1 + template1, 'READ')
        w1 = f1.Get('w')
        m4lpdf1D = w1.pdf(pdfName)

        f2 = TFile(pdfPath2 + template2, 'READ')
        w2 = f2.Get('w')
        m4lpdf2D = w2.pdf(pdfName)
        #make frame and plots
        mass4lFrame = CMS_zz4l_mass.frame()

        m4ldata1D = m4lpdf1D.generate(RooArgSet(CMS_zz4l_mass), 100000)
        hist_m4l1D = RooAbsData.createHistogram(m4ldata1D,'m4ldata1D',CMS_zz4l_mass,RooFit.Binning(binInfo[0], binInfo[1], binInfo[2]))
        m4ldata2D = m4lpdf2D.generate(RooArgSet(CMS_zz4l_mass,CMS_zz4l_massErr), 100000)
        hist_m4l2D = RooAbsData.createHistogram(m4ldata2D,'m4ldata2D',CMS_zz4l_mass,RooFit.Binning(binInfo[0], binInfo[1], binInfo[2]))

        m4ldata2D.plotOn(mass4lFrame, RooFit.MarkerStyle(20), RooFit.MarkerColor(4), RooFit.MarkerSize(1))
        m4lpdf2D.plotOn(mass4lFrame, RooFit.LineWidth(2), RooFit.LineColor(4), RooFit.Name("m4l_2D_to_1D"))

        m4ldata1D.plotOn(mass4lFrame, RooFit.MarkerStyle(20), RooFit.MarkerColor(1), RooFit.MarkerSize(1))
        m4lpdf1D.plotOn(mass4lFrame, RooFit.LineWidth(2), RooFit.LineColor(1), RooFit.Name("m4l_1D"))

   
        ###########
        '''
        fsDict = {"4mu":'1', "4e":'2', "2e2mu":'3'}
        uncDict = {"4mu":0.01, "4e":0.3, "2e2mu":0.05}
#        uncDict = {"4mu":0.2, "4e":0.2, "2e2mu":0.2}

#        w2.var("CMS_zz4l_sigma_e_sig").setVal(uncDict[fs]*1)
        w2.var("CMS_zz4l_n_sig_"+fsDict[fs]+"_13").setVal(uncDict[fs]*1)
        m4ldata2D_1sigma_plus = m4lpdf2D.generate(RooArgSet(CMS_zz4l_mass,CMS_zz4l_massErr),100000)
        hist_m4l2D_1sigma_plus = RooAbsData.createHistogram(m4ldata2D_1sigma_plus,'m4ldata2D_1sigma_plus',CMS_zz4l_mass,RooFit.Binning(binInfo[0], binInfo[1], binInfo[2]))
#        m4ldata2D_1sigma_plus.plotOn(mass4lFrame, RooFit.MarkerStyle(20), RooFit.MarkerColor(2), RooFit.MarkerSize(1))
#        m4lpdf2D.plotOn(mass4lFrame, RooFit.LineWidth(2), RooFit.LineColor(2), RooFit.Name("m4l_2D_to_1D_1sigma_plus"))

#        w2.var("CMS_zz4l_sigma_e_sig").setVal(uncDict[fs]*-1)
        w2.var("CMS_zz4l_n_sig_"+fsDict[fs]+"_13").setVal(uncDict[fs]*-1)
        m4ldata2D_1sigma_minus = m4lpdf2D.generate(RooArgSet(CMS_zz4l_mass,CMS_zz4l_massErr), 100000)
        hist_m4l2D_1sigma_minus = RooAbsData.createHistogram(m4ldata2D_1sigma_minus,'m4ldata2D_1sigma_minus',CMS_zz4l_mass,RooFit.Binning(binInfo[0], binInfo[1], binInfo[2]))
#        m4ldata2D_1sigma_minus.plotOn(mass4lFrame, RooFit.MarkerStyle(20), RooFit.MarkerColor(5), RooFit.MarkerSize(1))
#        m4lpdf2D.plotOn(mass4lFrame, RooFit.LineWidth(2), RooFit.LineColor(5), RooFit.Name("m4l_2D_to_1D_1sigma_minus"))
        '''
        ###########

        w.factory('DoubleCB::doubleCB(CMS_zz4l_mass, \
                             meanDCB[125,120,130], sigmaDCB[1,0,10], \
                             alphaDCB[1.1,0,50], nDCB[1,0,50], alpha2[1.1,0,50], n2[1,0,50])')
#        w.Print()

        dcb = w.pdf("doubleCB")

        dcb.fitTo(m4ldata1D)
#        dcb.plotOn(mass4lFrame, RooFit.LineColor(2), RooFit.LineWidth(2))
        dcb.paramOn(mass4lFrame, RooFit.Layout(0.17, 0.4, 0.9), RooFit.Format("NE", RooFit.FixedPrecision(4)))
        dcb.fitTo(m4ldata2D)
#        dcb.plotOn(mass4lFrame, RooFit.LineColor(5), RooFit.LineWidth(2))
        dcb.paramOn(mass4lFrame, RooFit.Layout(0.17, 0.4, 0.5), RooFit.Format("NE", RooFit.FixedPrecision(4)))

###
        c1 = TCanvas('c1', '', 800, 800)
        #overlap plots in upper pad
        pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0)
        pad1.SetGridx()
        pad1.Draw()
        pad1.cd()
        mass4lFrame.Draw()
        #set axis of upper pad
#        mass4lFrame.GetYaxis().SetLabelSize(0.)
#        axis = TGaxis( 105, 0, 105, hist_m4l1D.GetMaximum()*1.5, 0, hist_m4l1D.GetMaximum(), 510, "")
#        axis.Draw()
        #legend
        legend = ROOT.TLegend(0.7,0.75,0.95,0.9)
        legend.AddEntry(mass4lFrame.findObject("m4l_1D"), '1D model', 'l')
        legend.AddEntry(mass4lFrame.findObject("m4l_2D_to_1D"), '2D model projected to 1D', 'l')
        legend.SetTextSize(0.03)
        legend.SetLineWidth(2)
        legend.SetFillColor(0)
        legend.SetBorderSize(1)
        legend.Draw('SAME')

        #ratio plot in lower pad
        c1.cd()
        pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.2)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        #make ratio plot
        ratio = hist_m4l1D.Clone("ratio")
        ratio.SetMinimum(0.4)
        ratio.SetMaximum(1.6)
        ratio.Sumw2()
        ratio.SetStats(0)
        ratio.Divide(hist_m4l2D)
        ratio.SetMarkerStyle(20)
        ratio.Draw('e1p')
        ratio.SetTitle("")
        ratio.GetYaxis().SetTitle("ratio 1D/2D ")
        ratio.GetXaxis().SetTitle("mass4l(GeV)")
        ratio.GetYaxis().SetTitleSize(30)
        ratio.GetYaxis().SetTitleFont(43)
        ratio.GetYaxis().SetTitleOffset(1.75)
        ratio.GetYaxis().SetLabelFont(43) 
        ratio.GetYaxis().SetLabelSize(25)
        ratio.GetXaxis().SetTitleSize(30)
        ratio.GetXaxis().SetTitleFont(43)
        ratio.GetXaxis().SetTitleOffset(4.)
        ratio.GetXaxis().SetLabelFont(43)
        ratio.GetXaxis().SetLabelSize(25)

        '''
        ratio_1sigma_plus = hist_m4l1D.Clone("ratio_1sigma_plus")
        ratio_1sigma_plus.Divide(hist_m4l2D_1sigma_plus)
        ratio_1sigma_plus.Draw('same')
        ratio_1sigma_plus.SetLineColor(2)
        ratio_1sigma_minus = hist_m4l1D.Clone("ratio_1sigma_minus")
        ratio_1sigma_minus.Divide(hist_m4l2D_1sigma_minus)
        ratio_1sigma_minus.Draw('same')
        ratio_1sigma_minus.SetLineColor(4)
        '''

        c1.SaveAs(args.saveDir + "m4l_1D_2D_compare_"+m4lType+"_"+fs+".png")
        c1.SaveAs(args.saveDir + "m4l_1D_2D_compare_"+m4lType+"_"+fs+".pdf")
        c1.SaveAs("m4l_1D_2D_compare_"+m4lType+"_"+fs+".png")
        c1.SaveAs("m4l_1D_2D_compare_"+m4lType+"_"+fs+".pdf")

