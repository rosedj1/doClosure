from ROOT import *
from array import array
import math
from tdrStyle import *
setTDRStyle()

def MakeGraph(txtfile1, txtfile2):

    data1 = [line.strip().split() for line in open(txtfile1, 'r')]
    data2 = [line.strip().split() for line in open(txtfile2, 'r')]

    x,y,xErr,yErr = array('f'),array('f'),array('f'),array('f')

    corr = []

    for i in range(len(data1)):

        tmp_x = (float(data1[i][2]) + float(data1[i][3]) )/2
        tmp_y = ((float(data1[i][0]) - float(data2[i][0]))/91.19)
        tmp_xerr = (float(data1[i][3]) - float(data1[i][2]) )/2
        tmp_yerr = math.sqrt(float(data1[i][1])**2 + float(data2[i][1])**2)/91.19

        '''
        x.append( (float(data1[i][2]) + float(data1[i][3]) )/2 )
        xErr.append((float(data1[i][3]) - float(data1[i][2]) )/2)
        y.append( (float(data1[i][0]) - float(data2[i][0]))/91.19 )
        yErr.append(math.sqrt(float(data1[i][1])**2 + float(data2[i][1])**2)/91.19 )
        '''
 
        x.append(tmp_x)
        y.append(tmp_y)
        xErr.append(tmp_xerr)
        yErr.append(tmp_yerr)

#        print tmp_x-tmp_xerr,tmp_x+tmp_xerr,tmp_y-tmp_yerr,tmp_y+tmp_yerr,tmp_y*100
        corr.append(round(tmp_y*100,4) )

    gr = TGraphErrors(len(x),x,y,xErr,yErr)

    print corr

    return gr

#gr1 = MakeGraph("data_2mu_5_100.txt", "mc_2mu_5_100.txt")
#gr1 = MakeGraph("data_2mu_0.0_2.4.txt", "mc_2mu_0.0_2.4.txt")
#gr1 = MakeGraph("data_2mu_0_0.1.txt", "mc_2mu_0_0.1.txt")
#gr2 = MakeGraph("data_2e_7_100.txt", "mc_2e_7_100.txt")
#gr2 = MakeGraph("data_2e_0.0_2.5.txt", "mc_2e_0.0_2.5.txt")
#gr2 = MakeGraph("data_2e_0_0.1.txt", "mc_2e_0_0.1.txt")

#gr1 = MakeGraph("data_2mu_0.0_0.9.txt", "mc_2mu_0.0_0.9.txt")
#gr2 = MakeGraph("data_2mu_0.9_1.4.txt", "mc_2mu_0.9_1.4.txt")
#gr3 = MakeGraph("data_2mu_1.4_2.4.txt", "mc_2mu_1.4_2.4.txt")
gr1 = MakeGraph("data_2e_0.0_0.8.txt", "mc_2e_0.0_0.8.txt")
gr2 = MakeGraph("data_2e_0.8_1.5.txt", "mc_2e_0.8_1.5.txt")
gr3 = MakeGraph("data_2e_1.5_2.5.txt", "mc_2e_1.5_2.5.txt")

#legendName1 = "Z, |#eta| 0.0-0.9"
#legendName2 = "Z, |#eta| 0.9-1.4"
#legendName3 = "Z, |#eta| 1.4-2.5"
legendName1 = "Z, |#eta| 0.0-0.8"
legendName2 = "Z, |#eta| 0.8-1.5"
legendName3 = "Z, |#eta| 1.5-2.5"

xMin = 0
#xMax = 2.5
xMax = 100
yMin = -0.004
yMax = 0.004
#xTitle = "|#eta|"
#xTitle = "#sigma_{m_{2l}}/m_{2l}"
xTitle = "Electron p_{T}(GeV)"
yTitle = "(m_{data}^{peak}-m_{MC}^{peak})/m_{PDG}"
unc = 0.0004
savename = "lepScale_vs_pt_eta_e.png"



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
#lineBoundDiagonal_up.Draw()
#lineBoundDiagonal_dn.Draw()
lineBound = TLine(xMin, 0, xMax, 0)
lineBound.SetLineStyle(kDashed)
lineBound.Draw()


gr1.Draw("same pe")
gr1.SetMarkerStyle(25)
gr2.Draw("same pe")
gr2.SetMarkerStyle(25)
gr3.Draw("same pe")
gr3.SetMarkerStyle(25)

gr2.SetMarkerColor(1)
gr1.SetMarkerColor(4)
gr3.SetMarkerColor(2)
gr2.SetMarkerSize(1.3)
gr1.SetMarkerSize(1.3)
gr3.SetMarkerSize(1.3)


legend = TLegend(0.65,0.15,0.8,0.4)
legend.AddEntry(gr1, legendName1, "pe")
legend.AddEntry(gr2, legendName2, "ep")
legend.AddEntry(gr3, legendName3, "ep")
legend.SetTextSize(0.03)
legend.SetLineWidth(0)
legend.SetFillColor(0)
legend.SetBorderSize(1)
legend.Draw()

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.5*c1.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right                                                                     
latex2.DrawLatex(0.90, 0.95,"35.9 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.8*c1.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right                                                                     
latex2.DrawLatex(0.19, 0.95, "CMS")
latex2.SetTextSize(0.6*c1.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.32, 0.95, "Preliminary")
latex2.SetTextFont(42)
latex2.SetTextSize(0.45*c1.GetTopMargin())


c1.SaveAs("/home/mhl/public_html/2017/20170313_checkLepScale/"+savename)
c1.SaveAs("/home/mhl/public_html/2017/20170313_checkLepScale/"+savename.replace("png","pdf"))

