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
       nDiv = 6
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

filename = 'test.root'
plotpath = '/home/mhl/public_html/2016/20161213_mass/scratch/'

doubleCB_tail_4mu_reco = '1.2547 2.1116 1.8509 3.0920' # a1,n1,a2,n2
doubleCB_tail_4mu_refit = '1.2741 2.02 1.99 2.71' 
doubleCB_tail_4e_reco = '0.8629 5.3039 1.4398 6.1962' # a1,n1,a2,n2
doubleCB_tail_4e_refit = '0.85930 4.4827 1.4451 6.1654'
doubleCB_tail_2e2mu_reco = '0.9515 3.4081 1.4387 4.8701'
doubleCB_tail_2e2mu_refit = '0.99078 2.9022 1.4538 4.8895'

call('rm ../makeSummaryPlots/*txtpara*txt', shell=True)

#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_reco, False)
#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_refit, True)
#doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_reco, False)
doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_refit, True)
#doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_reco, False)
#doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_refit, True)

