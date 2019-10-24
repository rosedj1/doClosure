#!/bin/bash
################################################################################
# PURPOSE:  Make closure plots for Drell-Yan events. 
# SYNTAX:   Check the code in 'makeGraph(_jake).sh' which calls this script.
# NOTES:    A closure plot shows how well the measured sigma of a m_ll plot
#           agrees with the predicted sigma.
#           This code simply makes a plot using data stored in sigma_m2mu.txt.
# AUTHOR:   Hualin Mei, modified by Jake Rosenzweig
# DATE:     2019-08-19
# UPDATED:  2019-10-24
################################################################################
#_______________________________________________________________________________
# User Parameters
#_______________________________________________________________________________
# Automatic Stuff

from ROOT import *
from array import array
import sys
import argparse
import numpy as np

from tdrStyle import *
setTDRStyle()

def ParseOption():
    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--intxt', dest='intxt', type=str, help='')  # 
    parser.add_argument('--plotpath', dest='plotpath', type=str, help='')
    parser.add_argument('--plotname', dest='plotname', type=str, help='')
    parser.add_argument('--measurement', dest='measurement', type=str, help='')
    parser.add_argument('--doREFIT', dest='doREFIT', action='store_true', default=False, help='doREFIT')
    args = parser.parse_args()
    return args

args=ParseOption()

sigma_fit = []
sigma_fitErr = []
sigma_pred = []
sigma_pred_corr = []

data = [line.strip() for line in open(args.intxt, 'r')]
print "data:\n",data,"\n"

# The first line in args.intxt is blank. Therefore, start at element 1.
for i in range(1, len(data)):
    dataperline = data[i].split(' ')
    sigma_fit.append(float(dataperline[0]))
    sigma_fitErr.append(float(dataperline[1]))
    sigma_pred.append(float(dataperline[2]))
    if args.doREFIT:
       sigma_pred_corr.append(float(dataperline[4]))
    else:
       sigma_pred_corr.append(float(dataperline[3]))

# Prepare and fill x and y arrays.
x1, x2, y  = array('f'), array('f'), array('f')
xErr,yErr = array('f'), array('f')

for i in range(len(sigma_fit)):
    y.append(sigma_fit[i])
    yErr.append(sigma_fitErr[i])
    x1.append(sigma_pred[i])
    x2.append(sigma_pred_corr[i])
    xErr.append(0)

ave = []
print "Jake! I believe 'measure' means 1-sigma_pred_corr/sigma_fit"
print 'uncorr, corr, measure'
for i in range(len(x1)):
  print x1[i], x2[i], y[i], 1-x2[i]/y[i]
  ave.append(abs(1-x2[i]/y[i]))
print "average:",np.average(ave)

# Make the closure plots.
gr1 = TGraphErrors(len(y),x1,y,xErr,yErr)
gr2 = TGraphErrors(len(y),x2,y,xErr,yErr)

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
#lineBoundDiagonal = TLine(0, 0, 10,10)#5,5)
lineBoundDiagonal.SetLineStyle(kDashed)
lineBoundDiagonal.Draw()
lineBoundDiagonal_up = TLine(0, 0, 5/1.2,5)
#lineBoundDiagonal_up = TLine(0, 0, 10/1.2,10)#5/1.2,5)
lineBoundDiagonal_up.SetLineStyle(kDashed)
lineBoundDiagonal_up.Draw()
lineBoundDiagonal_down = TLine(0, 0, 5,5/1.2)
#lineBoundDiagonal_down = TLine(0, 0, 10,10/1.2)#5,5/1.2)
lineBoundDiagonal_down.SetLineStyle(kDashed)
lineBoundDiagonal_down.Draw()

if not args.doREFIT:
   gr1.Draw('pe0')
gr2.Draw('pe0 same')

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
c1.SaveAs(args.plotpath+args.plotname.replace('.png','.pdf'))

