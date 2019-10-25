#!/bin/bash
################################################################################
# PURPOSE: 
# SYNTAX:  
# NOTES:   
# AUTHOR:  
# DATE:    
# UPDATED: 
################################################################################
#_______________________________________________________________________________
# User Parameters
#_______________________________________________________________________________
# Automatic Stuff

# plotpath='/home/rosedj1/public_html/Higgs/HiggsMassMeas/Plots_2018_MC_Zclosure_goodlambdas/'
sigma_txtfile=''
suffix_string=''
extraname='test'
relpterr_binstart=0
relpterr_binstop=0.03
binwidth=0.01
num_closureplots_bins="4 8 16"
#num_closureplots_bins="2 4 6 8 10 12 14 16 18 20 25 30"

# FIXME: Must move file naming and binning out of closurefunctions.py.

#   for num in ${num_closureplots_bins}; do
#       cp doAllClosure_mZ.py 
#   #    sed -i "s|SUFFIX|${suffix_string}|"
#       sed -i "s|NAME|${extraname}|" <somefile>
#       sed -i "s|NDIV|${num}|" <somefile>
#       python doAllClosure_mZ.py

python doAllClosure_mZ.py 
#python doAllClosure_mZ.py > fit_output_mZ_relpTerrbinning.txt
cd ../makeSummaryPlots/
./makeGraph_jake.sh  # must give sigma_txtfile
