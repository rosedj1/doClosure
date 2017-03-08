from ROOT import *
from tdrStyle import *
setTDRStyle()

from array import array

data_mu = [line.strip() for line in open("sigma_m2mu.txt", 'r')]
data_e = [line.strip() for line in open("sigma_m2e.txt", 'r')]

data_mu = [i.split() for i in data_mu]
data_e = [i.split() for i in data_e]

print data_mu
print data_e

#pred_mu = [0.747298,0.837003,0.934823,1.01137,1.08321,1.17708,1.30189,1.46387,1.76328,3.07576]
#meas_mu = [0.726384,0.87706,1.01431,1.07363,1.12321,1.2071,1.29659,1.44269,1.67882,2.43216]
#pred_e = [1.05847,1.28379,1.47105,1.65256,1.82611,2.00131,2.19655,2.45457,2.88506,1.77383]
#meas_e = [0.976698,1.23757,1.4779,1.71872,1.89627,2.05417,2.31513,2.62558,2.86667,1.84733]

x_mu,y_mu,x_e,y_e = array('f'),array('f'),array('f'),array('f')
x_mu_err,y_mu_err,x_e_err,y_e_err = array('f'),array('f'),array('f'),array('f')

for i in range(len(data_mu)):
    x_mu.append(float(data_mu[i][3]))
    x_mu_err.append(0)
    y_mu.append(float(data_mu[i][0]))
    y_mu_err.append(float(data_mu[i][1]))
    x_e.append(float(data_e[i][3]))
    x_e_err.append(0)
    y_e.append(float(data_e[i][0]))
    y_e_err.append(float(data_e[i][1]))

gr_mu = TGraphErrors(10, x_mu, y_mu, x_mu_err, y_mu_err)
gr_e = TGraphErrors(10, x_e, y_e, x_e_err, y_e_err)

c1 = TCanvas('c1', '', 800, 800)

dummy = TH1D("dummy","dummy",1,0,5)
dummy.SetMinimum(0.0)
dummy.SetMaximum(5)
dummy.SetLineColor(0)
dummy.SetMarkerColor(0)
dummy.SetLineWidth(0)
dummy.SetMarkerSize(0)
dummy.GetXaxis().SetTitle("Predicted #sigma_{2l}(GeV)")
dummy.GetYaxis().SetTitle("Measured #sigma_{2l}(GeV)")
dummy.Draw()


gr_mu.Draw('pe0 same')
gr_e.Draw('pe0 same')

gr_mu.SetMarkerColor(4)
gr_e.SetMarkerColor(2)

gr_mu.SetMarkerStyle(25)
gr_e.SetMarkerStyle(20)

gr_mu.SetMarkerSize(1.3)
gr_e.SetMarkerSize(1.3)

maxReso = 5
unc = 1.2

lineBoundDown = TLine(0, 0, maxReso, maxReso/unc)
lineBoundUp   = TLine(0, 0, maxReso/unc, maxReso)
lineBoundDiagonal = TLine(0, 0, maxReso, maxReso)
lineBoundUp.SetLineStyle(kDashed)
lineBoundUp.Draw()
lineBoundDown.SetLineStyle(kDashed)
lineBoundDown.Draw()
lineBoundDiagonal.Draw()

legend = TLegend(0.2,0.7,0.5,0.85)
legend.AddEntry(gr_e, "Z#rightarrow e^{+}e^{-} Data", "p")
legend.AddEntry(gr_mu, "Z#rightarrow #mu^{+}#mu^{-} Data", "p")
legend.SetTextSize(0.05)
legend.SetLineWidth(0)
legend.SetFillColor(0)
legend.SetBorderSize(0)
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

c1.SaveAs('/home/mhl/public_html/2017/20170308_plotsForApproval/closure.png')
c1.SaveAs('/home/mhl/public_html/2017/20170308_plotsForApproval/closure.pdf')

