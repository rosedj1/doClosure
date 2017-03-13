from ROOT import *
from array import array
import math
from tdrStyle import *
setTDRStyle()

def MakeGraph(txtfile1, txtfile2):

    data1 = [line.strip().split() for line in open(txtfile1, 'r')]
    data2 = [line.strip().split() for line in open(txtfile2, 'r')]

    x,y,xErr,yErr = array('f'),array('f'),array('f'),array('f')

    for i in range(len(data1)):

        x.append( (float(data1[i][2]) + float(data1[i][3]) )/2 )
        xErr.append((float(data1[i][3]) - float(data1[i][2]) )/2)
        y.append( (float(data1[i][0]) - float(data2[i][0]))/91.19 )
        yErr.append(math.sqrt(float(data1[i][1])**2 + float(data2[i][1])**2)/91.19 )

    gr = TGraphErrors(len(x),x,y,xErr,yErr)

    return gr

##gr1 = MakeGraph("data_2mu_5_100.txt", "mc_2mu_5_100.txt")
gr1 = MakeGraph("data_2mu_0.0_2.4.txt", "mc_2mu_0.0_2.4.txt")
xMin = 0#-2.4
##xMax = 2.4
xMax = 100
yMin = -0.001
yMax = 0.001
#xTitle = "|#eta|"
xTitle = "p_{T}(GeV)"
yTitle = "m_{#mu#mu}(Data-MC)/True"
unc = 0.0004
savename = "mu_lepScale_vs_pt_testBinning_DCB_withBKG_randomCut.png"

#gr1 = MakeGraph("data_2e_7_100.txt", "mc_2e_7_100.txt")
##gr1 = MakeGraph("data_2e_0.0_2.5.txt", "mc_2e_0.0_2.5.txt")
#xMin = -2.5
#xMax = 2.5
##xMax = 100
#yMin = -0.003
#yMax = 0.003
#xTitle = "|#eta|"
##xTitle = "p_{T}(GeV)"
#yTitle = "m_{ee}(Data-MC)/True"
#unc = 0.003
#savename = "e_lepScale_vs_eta_testBinning_DCB_withBKG_randomCut.png"

c1 = TCanvas("c1","",800,800)
c1.SetLeftMargin(0.2)
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
lineBoundDiagonal_up = TLine(xMin, unc, xMax, unc)
lineBoundDiagonal_dn = TLine(xMin, -unc, xMax, -unc)
lineBoundDiagonal_up.SetLineStyle(kDashed)
lineBoundDiagonal_dn.SetLineStyle(kDashed)
lineBoundDiagonal_up.Draw()
lineBoundDiagonal_dn.Draw()

gr1.Draw("same pe")
gr1.SetMarkerStyle(20)

#savename = "mu_lepScale_vs_eta.png"
c1.SaveAs("/home/mhl/public_html/2017/20170312_checkLepScale/"+savename)
