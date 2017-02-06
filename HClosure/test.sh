plotpath="/home/mhl/public_html/2017/20170205_muonPtErrCorr/fitmassH/"

cd ../makeSummaryPlots;
./makeGraph.sh 4mu_reco $plotpath
./makeGraph.sh 4mu_refit $plotpath
./makeGraph.sh 4e_reco $plotpath
./makeGraph.sh 4e_refit $plotpath
./makeGraph.sh 2e2mu_reco $plotpath
./makeGraph.sh 2e2mu_refit $plotpath
cd -
