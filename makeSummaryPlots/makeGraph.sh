#python makeGraph.py --intxt "sigma_m2e.txt" --plotpath "/home/mhl/public_html/2016/20161122_mass/fitmassZ/" --plotname "closureZ_2e.png" --measurement "m_{2l}"
#python makeGraph.py --intxt "sigma_m2mu.txt" --plotpath "/home/mhl/public_html/2016/20161124_mass/test/" --plotname "closureZ_2mu.png" --measurement "m_{2l}"

python makeGraph.py --intxt "sigma_m4mu_reco.txt" --plotpath "/home/mhl/public_html/2016/20161124_mass/testH/" --plotname "closureH_4mu_corr_reco.png" --measurement "m_{4l}" 
python makeGraph.py --intxt "sigma_m4mu_refit.txt" --plotpath "/home/mhl/public_html/2016/20161124_mass/testH/" --plotname "closureH_4mu_corr_refit.png" --measurement "m_{4l}" --doREFIT

#python makeGraph.py --intxt "sigma_m4e.txt" --plotpath "/home/mhl/public_html/2016/20161023_mass/" --plotname "closureZ_4e_corr_reco_refit.png" --measurement "m_{4l}"
#python makeGraph.py --intxt "sigma_m2e2mu.txt" --plotpath "/home/mhl/public_html/2016/20161023_mass/" --plotname "closureZ_2e2mu_corr_reco_refit.png" --measurement "m_{4l}"

