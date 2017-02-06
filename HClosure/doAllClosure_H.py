from subprocess import call
import time 

def doAllClosure(fs, filename, plotpath, doubleCB_tail, doREFIT):


    if fs == '4mu':
       mass4lErr_bins = [0,0.007]
       nDiv = 8
       for i in range(nDiv):
           mass4lErr_bins.append(mass4lErr_bins[-1]+(0.02-0.007)/nDiv)
       mass4lErr_bins.append(1)
    else:
       mass4lErr_bins = [0,0.009]
       nDiv = 8#6
       for i in range(nDiv):
           mass4lErr_bins.append(mass4lErr_bins[-1]+(0.02-0.009)/nDiv)
       mass4lErr_bins.append(1)


#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/Mass_ICHEP2016/Fit_PereventMerr/'
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

filename = 'ggH125_2016MC.root'
plotpath = '/home/mhl/public_html/2017/20170205_muonPtErrCorr/fitmassH/'

doubleCB_tail_4mu_reco = '1.345 1.881 2.436 1.520' # a1,n1,a2,n2
doubleCB_tail_4mu_refit = '1.319 1.992 2.329 1.970' 
doubleCB_tail_4e_reco = '0.9354 6.581 2.025 3.274'
#doubleCB_tail_4e_reco = '0.819 8.33 1.56 4.61' 
doubleCB_tail_4e_refit = '1.04 5.35 1.89 4.095'
doubleCB_tail_2e2mu_reco = '1.057 3.965 2.290 1.882'
doubleCB_tail_2e2mu_refit = '1.185 3.144 1.973 2.795'

call('rm ../makeSummaryPlots/*txtpara*txt', shell=True)

#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_reco, False)
#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_refit, True)
#doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_reco, False)
doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_refit, True)
#doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_reco, False)
#doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_refit, True)

