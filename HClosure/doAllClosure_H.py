from subprocess import call
import time 

def doAllClosure(fs, filename, plotpath, doubleCB_tail, doREFIT):

    mass4lErr_bins = [0.005, 0.007]
    nDiv = 8
    for i in range(nDiv):
        mass4lErr_bins.append(mass4lErr_bins[-1]+(0.015-0.007)/nDiv)
    mass4lErr_bins.append(0.05)

    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/liteUFHZZ4LAnalyzer/Ntuples/'
    outtxtName = '../makeSummaryPlots/sigma_m'+fs #'.txt'
    if not doREFIT:
       outtxtName += '_reco.txt'
    else:
       outtxtName += '_refit.txt'


    call('echo " " > ' + outtxtName, shell=True)

    for i in range(len(mass4lErr_bins)-1):

        cmd = 'python doClosure_m4l.py --min '+str(mass4lErr_bins[i])+' --max '+str(mass4lErr_bins[i+1]) \
            + ' --inpath ' + inputpath \
            + ' --filename ' + filename \
            + ' --plotpath ' + plotpath \
            + ' --doubleCB_tail ' + doubleCB_tail 

        if doREFIT:
           cmd += ' --doREFIT '

        cmd += ' --outtxtName ' + outtxtName + ' --channel '+fs+' &'

        print cmd
        call(cmd, shell=True)

filename = 'test_tripleGauss_symErrHESSE_corrMuPtScale_ebeFrommZReco_60_120.root'
plotpath = '/home/mhl/public_html/2016/20161124_mass/testH/'

doubleCB_tail_4mu_reco = '1.3224 2.0017 1.6838 8.1150' # a1,n1,a2,n2
doubleCB_tail_4mu_refit = '1.3347 1.8904 1.6481 10.741' 

doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_reco, False)
doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_refit, True)

