from subprocess import call
import time 

def doAllClosure(fs, filename, plotpath, doubleCB_tail, doREFIT, floatTail=False, doubleCB_width=1):


    if fs == '4mu':
       mass4lErr_bins = [0,0.007]
       nDiv = 8
       for i in range(nDiv):
           mass4lErr_bins.append(mass4lErr_bins[-1]+(0.02-0.007)/nDiv)
       mass4lErr_bins.append(1)
    else:
       mass4lErr_bins = [0,0.01]#0.009]
       nDiv = 8#6
       for i in range(nDiv):
           mass4lErr_bins.append(mass4lErr_bins[-1]+(0.02-0.01)/nDiv)
#           mass4lErr_bins.append(mass4lErr_bins[-1]+(0.025-0.01)/nDiv)
       mass4lErr_bins.append(1)


#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/Mass_ICHEP2016/Fit_PereventMerr/'
#    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/liteUFHZZ4LAnalyzer/Ntuples/'
    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/inputRoot/ggHSampleToMakeErrTemplate/'
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
        if floatTail:
           cmd += ' --floatTail '
   

        cmd += ' --outtxtName ' + outtxtName + ' --channel ' + fs + ' --doubleCB_width ' + str(doubleCB_width) + ' &'

        print cmd
        call(cmd, shell=True)

#filename = 'ggH125_2016MC.root'
filename = 'mH_125.root'
plotpath = '/home/mhl/public_html/2017/20170223_tailPara/'

doubleCB_tail_4mu_reco = '1.427 1.740 2.469 1.345' # a1,n1,a2,n2
doubleCB_tail_4mu_refit = '1.397 1.809 2.419 1.445' 
doubleCB_tail_4e_reco = '0.918 8.076 2.462 1.698'
doubleCB_tail_4e_refit = '0.8625 9.758 2.244 2.368'
doubleCB_tail_2e2mu_reco = '1.133 3.090 2.599 1.1'
#doubleCB_tail_2e2mu_refit = '1.084 3.363 2.495 1.341'
doubleCB_tail_2e2mu_refit = '1.26794459829 2.59459025239 2.58813373122 1.19529949092'
call('rm ../makeSummaryPlots/*txtpara*txt', shell=True)

#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_reco, False)
#doAllClosure('4mu', filename, plotpath, doubleCB_tail_4mu_refit, True)

#doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_reco, False)
#doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_reco, False)

#doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_refit, True, True, 1.78201770782)
#doAllClosure('4e', filename, plotpath, doubleCB_tail_4e_refit, True, False, 1)

#doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_reco, False)
doAllClosure('2e2mu', filename, plotpath, doubleCB_tail_2e2mu_refit, True)#, True, 1.3176831007)

