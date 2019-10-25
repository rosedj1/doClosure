from subprocess import call
import os

def makeCBfitandsigmatxt(inputdatafile, fs, outdir_plotmZCBfit, outpath_sigmatxt, ZWIDTH, mZ_bininfo, closureplot_binrange, quiet=False):
    '''

    '''

    print "Running over file:", inputdatafile
    print "Creating sigma txt file:", outpath_sigmatxt

    filenamedir, filename = os.path.split(inputdatafile)
    filenamedir = filenamedir+'/'

    call('echo " " > ' + outpath_sigmatxt, shell=True)

    # Each iteration makes a CB fit plot.
    for k in range(len(closureplot_binrange)-1): 
        
        binlower = closureplot_binrange[k]
        binupper = closureplot_binrange[k+1]

        cmd = 'python doClosure_mZ.py' \
            + ' --min          ' + str(binlower) \
            + ' --max          ' + str(binupper) \
            + ' --inpath       ' + filenamedir \
            + ' --filename     ' + filename \
            + ' --plotpath     ' + outdir_plotmZCBfit \
            + ' --ZWIDTH       ' + str(ZWIDTH) \
            + ' --mZ_bininfo   ' + mZ_bininfo  \
            + ' --pathsigmatxt ' + outpath_sigmatxt \
            + ' --fs           ' + fs #+ ' &'
#            + ' --singleCB_tail ' + singleCB_tail \
#            + ' --pTErrCorrections ' + pTErrCorrections \

        if quiet:
            stdout_file = 'outputfromfit_' + filename.replace('.root','.txt')
            cmd += ' > ' + stdout_file
        # This is probably the way to get around multiple TSelector calls!
        # A new subshell is created with each iteration of the for loop.
        print "\nPassing command to shell:\n", cmd
        call(cmd, shell=True)

### Jake, past 2019-11-01, DELETE EVERYTHING BELOW!
#     def doAllClosure(fs, plotpath, Z_width, plotBinInfo, singleCB_tail, pTErrCorrections):
#     # e.g.          '2mu', '/home/...', 2.49, '300 60 120', '1.201 3.433', '1.251 1.292 1.117 1' 
#     
#         # THIS MAKES THE REL PT ERR BINS FOR THE CLOSURE PLOT.
#     #    massZErr_rel_bins = [0,0.009] # first two elements of list
#         massZErr_rel_bins = [0,0.009] # first two elements of list
#     
#         # Then add nDiv more equally-spaced bins. Just use np.linspace?
#     #    nDiv = 8
#         nDiv = 5
#         for i in range(nDiv):
#     #       massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.03-0.009)/nDiv)
#            massZErr_rel_bins.append(massZErr_rel_bins[-1]+(0.03-0.009)/nDiv)
#     
#     #    massZErr_rel_bins.append(0.04)
#     #    massZErr_rel_bins.append(0.1)
#     #    massZErr_rel_bins.append(1)
#         # massZErr list will have 12 elements (with nDiv=8, and 0.04 and 1 are appended):
#     #       [0
#     #       0.009
#     #       0.011625
#     #       0.01425
#     #       0.016875
#     #       0.0195
#     #       0.022125
#     #       0.02475
#     #       0.027375
#     #       0.03
#     #       0.04
#     #       1]
#     
#     #    massZErr_rel_bins = [0,1]
#     #    nDiv = 8
#     #    for i in range(nDiv):
#     #        massZErr_rel_bins.append(massZErr_rel_bins[-1]+(4.0-1.0)/nDiv)
#     #    massZErr_rel_bins.append(5)
#     
#         inputpath = '/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/'
#     #    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/'
#     #    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/'
#     #    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut/'
#     #    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/Data_2015D/'   
#     #_____ 2016MC _____#
#     #    inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2016MC_v1_20170222/'
#         #inputpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/Data_2016_v1_20170223/'
#     
#     #    filename = 'DoubleLepton_m'+fs+'.root'
#     #    filename = 'DYJetsToLL_M-50_kalman_v4_m'+fs+'.root'
#         filename = '2018_MC_MG5_DY_30percentoffiles_m'+fs+'.root'
#         outtxtName = '../makeSummaryPlots/sigma_m'+fs+'_TEST_20191025_1149.txt'
#     
#         print "Running over file:", inputpath+filename
#         print "Will create file:", outtxtName
#         call('echo " " > ' + outtxtName, shell=True)
#     
#         # 11 iterations: 0,1,2,...,10. So this would make 11 mZ CB fit plots.
#         for i in range(len(massZErr_rel_bins)-1): 
#     
#             cmd = 'python doClosure_mZ.py' \
#                 + ' --min ' + str(massZErr_rel_bins[i]) \
#                 + ' --max ' + str(massZErr_rel_bins[i+1]) \
#                 + ' --inpath ' + inputpath \
#                 + ' --filename ' + filename \
#                 + ' --plotpath ' + plotpath \
#                 + ' --zWidth ' + str(Z_width) \
#                 + ' --plotBinInfo ' + plotBinInfo  \
#                 + ' --singleCB_tail ' + singleCB_tail \
#                 + ' --pTErrCorrections ' + pTErrCorrections \
#                 + ' --outtxtName ' + outtxtName + ' --fs ' + fs #+ ' &'
#     
#             print "\nPassing command to shell:\n", cmd
#             call(cmd, shell=True)

#     # 11 iterations: 0,1,2,...,10. So this would make 11 mZ CB fit plots.
#         for i in range(len(closureplot_binrange)-1): 
#     
#             cmd = 'python doClosure_mZ.py' \
#                 + ' --min ' + str(closureplot_binrange[i]) \
#                 + ' --max ' + str(closureplot_binrange[i+1]) \
#                 + ' --inpath ' + inputdatadir \
#                 + ' --filename ' + filename \
#                 + ' --plotpath ' + plotpath \
#                 + ' --zWidth ' + str(Z_width) \
#                 + ' --plotbininfo ' + plotbininfo  \
#                 + ' --singleCB_tail ' + singleCB_tail \
#                 + ' --pTErrCorrections ' + pTErrCorrections \
#                 + ' --sigmatxt_name ' + sigmatxt_name + ' --fs ' + fs #+ ' &'
#     
#             print "\nPassing command to shell:\n", cmd
#             call(cmd, shell=True)
