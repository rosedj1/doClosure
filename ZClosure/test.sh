plotpath="/home/mhl/public_html/2017/20170111_2015data_ptErrCorr_mu_0_0p9_1p8_2p2_2p4/"

cd ../makeSummaryPlots;
#./makeGraph.sh 2e $plotpath
./makeGraph.sh 2mu $plotpath

#./makeGraph.sh 4mu_reco $plotpath
#./makeGraph.sh 4mu_refit $plotpath
#./makeGraph.sh 4e_reco $plotpath
#./makeGraph.sh 4e_refit $plotpath
#./makeGraph.sh 2e2mu_reco $plotpath
#./makeGraph.sh 2e2mu_refit $plotpath
cd -
