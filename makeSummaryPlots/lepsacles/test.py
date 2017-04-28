from ROOT import *
from array import array
import math
from tdrStyle import *
setTDRStyle()

def MakeGraph(txtfile1):

    data1 = [line.strip().split() for line in open(txtfile1, 'r')]

    x,y,xErr,yErr = array('f'),array('f'),array('f'),array('f')

    for i in range(len(data1)):

        x.append( (float(data1[i][2]) + float(data1[i][3]) )/2 )
        xErr.append((float(data1[i][3]) - float(data1[i][2]) )/2)
        y.append( float(data1[i][0]) )
        yErr.append( float(data1[i][1])**2 )

    gr = TGraphErrors(len(x),x,y,xErr,yErr)

    return gr

#txt1 = "mc_2mu_0.0_2.4_gen.txt"
#txt2 = "mc_2mu_0.0_2.4_reco.txt"
#txt1 = "mc_2mu_0.0_100.0_gen.txt"
#txt2 = "mc_2mu_0.0_100.0_reco.txt"
txt1 = "H4L_4thMu.txt"
txt2 = "Z4L_4thMu.txt"
txt3 = "Z2L_2ndMu.txt"
savename = "/home/mhl/public_html/2017/20170427_checkZPeak/muonPt"
#legendName1 = "gen"
#legendName2 = "reco"
legendName1 = "H #rightarrow 4L (4th muon)"
legendName2 = "Z #rightarrow 4L (4th muon)"
legendName3 = "Z #rightarrow 2L (2nd muon)"
xMin = 5
xMax = 20
yMin = -0.001
yMax = 0.001
xTitle = "pT_{#mu}^{gen}"
yTitle = "(pT_{Reco}-pT_{Gen})/pT_{Gen}"

gr1 = MakeGraph(txt1)
gr2 = MakeGraph(txt2)
gr3 = MakeGraph(txt3)

c = TCanvas("c","",800,800)
c.SetLeftMargin(0.20)
dummy = TH1D("dummy","dummy",1,xMin,xMax)
dummy.SetMinimum(yMin)
dummy.SetMaximum(yMax)
dummy.SetLineColor(0)
dummy.SetMarkerColor(0)
dummy.SetLineWidth(0)
dummy.SetMarkerSize(0)
dummy.GetXaxis().SetTitle(xTitle)
dummy.GetYaxis().SetTitleOffset(2)
dummy.GetYaxis().SetTitle(yTitle)
dummy.Draw()

gr1.Draw("p same")
gr2.Draw("p same")
gr3.Draw("p same")

gr1.SetMarkerColor(1)
gr2.SetMarkerColor(2)
gr3.SetMarkerColor(4)

gr1.SetMarkerStyle(20)
gr2.SetMarkerStyle(20)
gr3.SetMarkerStyle(20)

legend = TLegend(0.65,0.75,0.8,0.95)
legend.AddEntry(gr1, legendName1, "ep")
legend.AddEntry(gr2, legendName2, "ep")
legend.AddEntry(gr3, legendName3, "ep")
legend.SetTextSize(0.03)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetBorderSize(1)
legend.Draw()

c.SaveAs(savename + ".png")
c.SaveAs(savename + ".pdf")
