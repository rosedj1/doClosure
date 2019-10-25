from subprocess import call
from PyUtils.fileUtils import copyFile, makeDirs
from closurefunctions import doAllClosure

plotBinInfo = '100 60 120'    # [num bins?, massZ lower bound, massZ upper bound].

# mZ CB fit plots for each pT err bin are stored here:
plotpath = '/home/rosedj1/public_html/Higgs/HiggsMassMeas/Plots_2018_MC_Zclosure_diffbinning/'
copyFile("/home/rosedj1/","index.php",plotpath)

#singleCB_tail_mu = '1.583 1.086' #first is alpha, second is n of singleCB
#singleCB_tail_e = '1.1443 2.5964' #first is alpha, second is n of singleCB
#doubleCB_tail_e = '1 2.13 1.262 50'

# I don't think these params are used!
#singleCB_tail_mu = '1.583 1.086' #first is alpha, second is n of singleCB
singleCB_tail_e = '1.201 3.433' #first is alpha, second is n of singleCB

# pTErrCorrections (Lambda) are stored in LUTs! So these values below are useless?
pTErrCorrections_mu = '1.251 1.292 1.117 1'    # Commented out in doClosure_mZ.py. Problem?
pTErrCorrections_e = '1.245 1.140 1.077 1.178' # Commented out in doClosure_mZ.py. Problem?

ZWidth = 2.49

#doAllClosure('2mu', plotpath, ZWidth, plotBinInfo, singleCB_tail_mu, pTErrCorrections_mu) # MAKE SURE ALL PARAMETERS ARE mu
doAllClosure('2e', plotpath, ZWidth, plotBinInfo, singleCB_tail_e, pTErrCorrections_e)  # MAKE SURE ALL PARAMETERS ARE e
#doAllClosure('2e', plotpath, ZWidth, plotBinInfo, doubleCB_tail_e, pTErrCorrections_e)
