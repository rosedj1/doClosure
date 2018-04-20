import numpy
import optparse
from ROOT import *
from tdrStyle import *
setTDRStyle()

def parseOptions():
    global observalbesTags, modelTags, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    parser.add_option('--i1', dest='input1', type='string', help='input file name')
    parser.add_option('--i2', dest='input2', type='string', help='input file name')
    parser.add_option('--doUp', dest='doUp', action='store_true', default=False)
    global opt, args
    (opt, args) = parser.parse_args()

def GetInterval(fileName1, fileName2):
    mass1 = [line.strip() for line in open(fileName1)]
    mass1 = [float(x) for x in mass1]
    mass2 = [line.strip() for line in open(fileName2)]
    mass2 = [float(x) for x in mass2]
    if not len(mass1) == len(mass2):
       raise RuntimeError('not same length')
    f1 = TH1F('f1','', 15, 0.505, 0.55)
    f2 = TH1F('f1','', 15, 0.53, 0.55)
    for i in range(len(mass1)):
        f1.Fill(mass1[i])
        f2.Fill(mass2[i])
    median_1 = round(numpy.percentile(numpy.array(mass1),50), 3)
    down_1 = round(numpy.percentile(numpy.array(mass1),16), 3)
    up_1 = round(numpy.percentile(numpy.array(mass1),84), 3)
    median_2 = round(numpy.percentile(numpy.array(mass2),50), 3)
    down_2 = round(numpy.percentile(numpy.array(mass2),16), 3)
    up_2 = round(numpy.percentile(numpy.array(mass2),84), 3)
    
    c1 = TCanvas("c1", '', 800, 800)
    c1.SetRightMargin(0.05)

    dummy = TH1D("dummy","dummy",1,0.5,0.56)
    dummy.SetMinimum(0.0)
    dummy.SetMaximum(30)
    dummy.SetLineColor(0)
    dummy.SetMarkerColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.GetYaxis().SetTitle("Events")
    if not opt.doUp:
       dummy.GetXaxis().SetTitle("uncertainty down")
    else:
       dummy.GetXaxis().SetTitle("uncertainty up")
    dummy.GetXaxis().SetLabelOffset(0.015)
    dummy.Draw()

    f1.Sumw2()
    f2.Sumw2()

    f1.Draw('pe1 same')
    f2.Draw('pe1 same')
    f1.SetMarkerStyle(20)
    f2.SetMarkerStyle(20)
    f2.SetMarkerColor(2)

    legendFrom68 = str(median_1) + ' -' + str(median_1-down_1) + '/+' + str(up_1-median_1)
    legendFromCombine = str(median_2) + ' -' + str(median_2-down_2) + '/+' + str(up_2-median_2)

    legend = TLegend(.17,.75,.5,.85)
    legend.AddEntry(f2, 'uncertainty from combine: ' + legendFromCombine , "pe1")
    legend.AddEntry(f1, 'uncertainty from 68% interval: ' + legendFrom68, "pe1")
    legend.SetTextSize(0.035)
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw("same")

    if not opt.doUp:
      c1.SaveAs('/home/mhl/public_html/2016/20161003_mass/unc_down.png')
    else:
      c1.SaveAs('/home/mhl/public_html/2016/20161003_mass/unc_up.png')

global opt, args
parseOptions()

path='../inputTXT/v3_20161003_3000fb/'
GetInterval(path+opt.input1, path+opt.input2)

#GetInterval("up_68.txt", "up_combine.txt")
#GetInterval("down_68.txt", "down_combine.txt")

