#python doClosure_mZ.py --min 0.007 --max 0.009 --inpath "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/HZZ4L_Mass/makeSlimTree/DY_2015MC_kalman_v4/" --filename "DYJetsToLL_M-50_kalman_v4_m2e.root" --plotpath "/home/mhl/public_html/2016/20161020_mass/fitmassZ/" --outtxtName "sigma_m2e.txt" --fs "2e"

#python doClosure_mZ.py --min 0.007 --max 0.009 --inpath "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/HZZ4L_Mass/makeSlimTree/DY_2015MC_kalman_v4/" --filename "DYJetsToLL_M-50_kalman_v4_m2mu.root" --plotpath "/home/mhl/public_html/2016/20161020_mass/fitmassZ/" --outtxtName "test.txt" --fs "2mu"

#python doClosure_m4l.py --min 0.6 --max 0.9 --inpath /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/Ana_ZZ4L/Ntuples/ --filename mH_125.root --plotpath /home/mhl/public_html/2016/20161022_mass/ --outtxtName sigma_m4mu.txt --channel 4mu

##################################
#_____ Jake's Closure Tests _____#
python doClosure_mZ.py --min 0.02 --max 7.2 --inpath "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/" --filename "2018_MC_MG5_DY_30percentoffiles_m2e.root" --plotpath "/home/rosedj1/public_html/Higgs/HiggsMassMeas/2018_MC_MG5_mll_Closure_Plots/" --outtxtName "sigma_m2e.txt" --fs "2e" --zWidth 2.49 --plotBinInfo ?? ? ??? --singleCB_tail ?? ? ??? --doubleCB_tail ?? ? ??? --pTErrCorrections ?? ? ???
