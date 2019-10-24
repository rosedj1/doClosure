#fs=$1
#plotpath=$2
#
#if [[ $1 == *"refit"* ]]
#then
#  python makeGraph.py --intxt "sigma_m"$1".txt" --plotpath $2 --plotname "closure_"$fs".png" --measurement "m_{"$1"}" --doREFIT;
#else
#  python makeGraph.py --intxt "sigma_m"$1".txt" --plotpath $2 --plotname "closure_"$fs".png" --measurement "m_{"$1"}";
#fi

#python makeGraph.py --intxt "sigma_m2e.txt" --plotpath "/home/mhl/public_html/2016/20161130_mass/fitmassZ/" --plotname "closureZ_2e.png" --measurement "m_{2l}"
#python makeGraph.py --intxt "sigma_m2mu.txt" --plotpath "/home/mhl/public_html/2016/20161124_mass/test/" --plotname "closureZ_2mu.png" --measurement "m_{2l}"
#python makeGraph.py --intxt "sigma_m4mu_reco.txt" --plotpath "/home/mhl/public_html/2016/20161125_mass/fitmassH/" --plotname "closureH_4mu_corr_reco.png" --measurement "m_{4l}" 
#python makeGraph.py --intxt "sigma_m4mu_refit.txt" --plotpath "/home/mhl/public_html/2016/20161124_mass/testH/" --plotname "closureH_4mu_corr_refit.png" --measurement "m_{4l}" --doREFIT
#python makeGraph.py --intxt "sigma_m4e_reco.txt" --plotpath "/home/mhl/public_html/2016/20161125_mass/fitmassH/" --plotname "closureH_4e_corr_reco.png" --measurement "m_{4l}"
#python makeGraph.py --intxt "sigma_m2e2mu_reco.txt" --plotpath "/home/mhl/public_html/2016/20161125_mass/fitmassH/" --plotname "closureH_2e2mu_corr_reco.png" --measurement "m_{4l}"
#python makeGraph.py --intxt "sigma_m4e_refit.txt" --plotpath "/home/mhl/public_html/2016/20161125_mass/fitmassH/" --plotname "closureH_4e_corr_refit.png" --measurement "m_{4l}" --doREFIT
#python makeGraph.py --intxt "sigma_m2e2mu_refit.txt" --plotpath "/home/mhl/public_html/2016/20161125_mass/fitmassH/" --plotname "closureH_2e2mu_corr_refit.png" --measurement "m_{4l}" --doREFIT

python makeGraph.py --intxt "sigma_m2e.txt" --plotpath "/home/rosedj1/public_html/Higgs/HiggsMassMeas/2018_MC_MG5_mll_Closure_Plots/" --plotname "closureZ_2e_jaketest.png" --measurement "m_{2l}"
