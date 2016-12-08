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
plotpath = '/home/mhl/public_html/2016/20161207_mass/scratch_fitmassH/'

doubleCB_tail_4mu_reco = '1.2898 2.0380 1.8323 3.1842' # a1,n1,a2,n2
doubleCB_tail_4mu_refit = '1.3321 1.8954 1.9023 3.0074' 
doubleCB_tail_4e_reco = '0.8323 5.5658 1.3757 6.9056' # a1,n1,a2,n2
doubleCB_tail_4e_refit = '0.85705 4.5382 1.4509 6.01'
doubleCB_tail_2e2mu_reco = '0.90829 3.6011 1.3723 5.2865'
doubleCB_tail_2e2mu_refit = '0.99254 2.9679 1.4789 4.7435'

#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_reco, False)
#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_refit, True)
doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_reco, False)
doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_refit, True)
doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_reco, False)
doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_refit, True)

