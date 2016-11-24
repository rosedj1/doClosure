from ROOT import *
from array import array
import sys

from tdrStyle import *
setTDRStyle()

import numpy as np

import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--intxt', dest='intxt', type=str, help='')
    parser.add_argument('--plotpath', dest='plotpath', type=str, help='')
    parser.add_argument('--plotname', dest='plotname', type=str, help='')
    parser.add_argument('--measurement', dest='measurement', type=str, help='')
    parser.add_argument('--doREFIT', dest='doREFIT', action='store_true', default=False, help='doREFIT')

    args = parser.parse_args()
    return args

args=ParseOption()

sigma2l_fit = []
sigma2l_pred = []
sigma2l_pred_corr = []

data = [line.strip() for line in open(args.intxt, 'r')]
for i in range(1, len(data)):

    dataperline = data[i].split(' ')
    sigma2l_fit.append(float(dataperline[0]))
    sigma2l_pred.append(float(dataperline[1]))
    if args.doREFIT:
       sigma2l_pred_corr.append(float(dataperline[3]))
    else:
       sigma2l_pred_corr.append(float(dataperline[2]))


y, x1, x2 = array('f'), array('f'), array('f')

for i in range(len(sigma2l_fit)):
    y.append(sigma2l_fit[i])
    x1.append(sigma2l_pred[i])
    x2.append(sigma2l_pred_corr[i])

ave = []
for i in range(len(x1)):
  print x2[i], x1[i], y[i], 1-x2[i]/y[i]
  ave.append(1-x2[i]/y[i])
print np.average(ave)


gr1 = TGraph(len(y),x1,y)
gr2 = TGraph(len(y),x2,y)

c1 = TCanvas('c1', '', 800, 800)

dummy = TH1D("dummy","dummy",1,0,5)
dummy.SetMinimum(0)
dummy.SetMaximum(5)
dummy.SetLineColor(0)
dummy.SetMarkerColor(0)
dummy.SetLineWidth(0)
dummy.SetMarkerSize(0)
dummy.GetXaxis().SetTitle('Predicted #sigma_{'+args.measurement+'}')
#dummy.GetYaxis().SetTitleOffset(1.3)
dummy.GetYaxis().SetTitle('Measured #sigma_{'+args.measurement+'}')
dummy.Draw()

lineBoundDiagonal = TLine(0, 0, 5,5)
lineBoundDiagonal.SetLineStyle(kDashed)
lineBoundDiagonal.Draw()
lineBoundDiagonal_up = TLine(0, 0, 5/1.2,5)
lineBoundDiagonal_up.SetLineStyle(kDashed)
lineBoundDiagonal_up.Draw()
lineBoundDiagonal_down = TLine(0, 0, 5,5/1.2)
lineBoundDiagonal_down.SetLineStyle(kDashed)
lineBoundDiagonal_down.Draw()

if not args.doREFIT:
   gr1.Draw('p')
gr2.Draw('p same')

gr1.SetMarkerStyle(2)
gr2.SetMarkerStyle(2)
gr1.SetMarkerColor(1)
gr2.SetMarkerColor(2)

legend = ROOT.TLegend(0.2,0.75,0.45,0.9)
if not args.doREFIT:
   legend.AddEntry(gr1, 'unCorr', 'p')
   legend.AddEntry(gr2, 'Corr', 'p')
#legend.AddEntry(gr1, 'reco Corr', 'p')
else:
   legend.AddEntry(gr2, 'refit Corr', 'p')
legend.SetTextSize(0.03)
legend.SetLineWidth(2)
legend.SetFillColor(0)
legend.SetBorderSize(1)
legend.Draw('SAME')

#c1.SaveAs('/home/mhl/public_html/2016/20161020_mass/fitmassZ/closureZ.png')
c1.SaveAs(args.plotpath+args.plotname)

