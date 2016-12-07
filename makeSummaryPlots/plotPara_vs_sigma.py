from ROOT import *
from array import array
from tdrStyle import *
setTDRStyle()

def makePlot(fileName, index, paraName,m4lType):
    info = [line.strip().split() for line in open(fileName)]
    x,xErr,y,yErr = array('f'),array('f'),array('f'),array('f')
    for j in range(len(info)/2):
        i = 2*j
        x.append((float(info[i][0])+float(info[i][1]))/2)
        xErr.append((float(info[i][1])-float(info[i][0]))/2)
        y.append(float(info[i][index]))  
        yErr.append(float(info[i+1][index]))
    gr = TGraphErrors(len(x),x,y,xErr,yErr)
    gr.SetMarkerStyle(20)
    gr.GetXaxis().SetTitle("#sigma_{4l}/m_{4l}")
    gr.GetYaxis().SetTitle(paraName)
    c = TCanvas('c','',800,800)
    dummy = TH1D("dummy","dummy",1,0,0.03)
    if 'n' in paraName:
        yMax = 10
        dummy.SetMinimum(0)
    if 'alpha' in paraName:
        yMax = 3
    dummy.SetMaximum(yMax)
    dummy.SetLineColor(0)
    dummy.SetMarkerColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.GetXaxis().SetTitle("#sigma_{4l}/m_{4l}")
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetYaxis().SetTitle(paraName)
    dummy.Draw()

    gr.Fit('pol1')
    gr.Draw('p same')

    c.SaveAs('/home/mhl/public_html/2016/20161207_mass/scratch_fitmassH/' + paraName + '_' + m4lType + '.png')

makePlot("sigma_m2e2mu_reco.txtpara.txt", 2, 'alphaL', '2e2mu_reco')
makePlot("sigma_m2e2mu_reco.txtpara.txt", 3, 'nL', '2e2mu_reco')
makePlot("sigma_m2e2mu_reco.txtpara.txt", 4, 'alphaR', '2e2mu_reco')
makePlot("sigma_m2e2mu_reco.txtpara.txt", 5, 'nR', '2e2mu_reco')

makePlot("sigma_m2e2mu_refit.txtpara.txt", 2, 'alphaL', '2e2mu_refit')
makePlot("sigma_m2e2mu_refit.txtpara.txt", 3, 'nL', '2e2mu_refit')
makePlot("sigma_m2e2mu_refit.txtpara.txt", 4, 'alphaR', '2e2mu_refit')
makePlot("sigma_m2e2mu_refit.txtpara.txt", 5, 'nR', '2e2mu_refit')

#makePlot("sigma_m4e_reco.txtpara.txt", 2, 'alphaL', '4e_reco')
#makePlot("sigma_m4e_reco.txtpara.txt", 3, 'nL', '4e_reco')
#makePlot("sigma_m4e_reco.txtpara.txt", 4, 'alphaR', '4e_reco')
#makePlot("sigma_m4e_reco.txtpara.txt", 5, 'nR', '4e_reco')

#makePlot("sigma_m4e_refit.txtpara.txt", 2, 'alphaL', '4e_refit')
#makePlot("sigma_m4e_refit.txtpara.txt", 3, 'nL', '4e_refit')
#makePlot("sigma_m4e_refit.txtpara.txt", 4, 'alphaR', '4e_refit')
#makePlot("sigma_m4e_refit.txtpara.txt", 5, 'nR', '4e_refit')


