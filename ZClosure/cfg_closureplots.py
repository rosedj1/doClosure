#!/usr/bin/ python2
###############################################################################
# PURPOSE: This is a configuration file which:
#     (1) Makes CB fits using Z->ll events in various ranges of sigma_CB.
#     (2) Makes txt file with CB_fit sigmas.
# SYNTAX: python <script.py>
# NOTES:   
# AUTHOR: Jake Rosenzweig 
# DATE:   2019-10-25
# UPDATED: 
###############################################################################
from PyUtils.fileUtils import copyFile, makeDirs
from subprocess import call
import numpy
import os
#from doClosure import doClosure_mZ
from closurefunctions import makeCBfitandsigmatxt
#______________________________________________________________________________
# USER PARAMETERS
fs = '2e'
inputdatafile = '/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/2018_MC_MG5_DY_30percentoffiles_m2e.root'

outpath_sigmatxt = '/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/doClosure/makeSummaryPlots/Sigma_CBfit_txtfiles/sigma_m2e_Test2python.txt'
outdir_plotmZCBfit = '/home/rosedj1/public_html/Higgs/HiggsMassMeas/Plots_2018_MC_Zclosure_CBplots_DELETEME/'

mZ_bininfo = '100 60 120'    # [num bins?, massZ lower bound, massZ upper bound].
closureplot_binmin = 0.0    # Along rel mass uncertainty axis.
closureplot_binmax = 0.05
nbins = 20    # Should also be the number of CB fit plots you get.
ZWIDTH = 2.49

#_______________________________________________________________________________
# AUTOMATIC STUFF
# Create output dir and cp index.php into it.
copyFile("/home/rosedj1/","index.php",outdir_plotmZCBfit)
closureplot_binrange = numpy.linspace(closureplot_binmin, closureplot_binmax, nbins+1)

# Make sure final state and file match!
dirtofile, filename = os.path.split(inputdatafile)

if fs not in filename:
    raise RuntimeError("""
        WARNING: Final states in inputfile and the one you chose don't match.
        Did you specify the correct fs?
        """)
#___________________________________________________________________________
if __name__ == "__main__":
    makeCBfitandsigmatxt(inputdatafile, fs, outdir_plotmZCBfit, outpath_sigmatxt, ZWIDTH, mZ_bininfo, closureplot_binrange, quiet=False)  

# FIXME: Class Implementation
#     cballfit_list = [CBallFit() for ]
#     class CBallFit():
#         def __init__(self):
#             self.
#     
