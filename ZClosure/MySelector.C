#define MySelector_cxx
// The class definition in MySelector.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("MySelector.C")
// root> T->Process("MySelector.C","some options")
// root> T->Process("MySelector.C+")
//


#include "MySelector.h"
#include <TH2.h>
#include <TStyle.h>
#include <math.h>
#include <TFile.h>
void MySelector::SetTag(TString fs) {fs_=fs;}


double MySelector::ApplyCorr(double pT, double eta, double pTErr, int ecalDriven, TString fs) {

 double scale = 1;

 if (ecalDriven) {

    if (abs(eta) < 1 && pTErr/pT < 0.03 ) scale = pTCorr(pT,eta,fs,0); // LUT_1 is for |eta| < 1 && pTErr/pT < 0.03
    if (abs(eta) < 1 && pTErr/pT > 0.03 ) scale =1.02;
    if (abs(eta) >= 1 && pTErr/pT < 0.07 ) scale = pTCorr(pT,eta,fs,1); // LUT_2 is for |eta| > 1 && pTErr/pT < 0.06
    if (abs(eta) >= 1 && pTErr/pT > 0.07 ) scale = 0.67;

    } else {

           scale = pTCorr(pT,eta,fs,2); //LUT_3 is for non ecal driven electron

           }

    return scale;
}

double MySelector::pTCorr(double pT, double eta, TString fs, int tag){

 TH2F* LUT_ = LUTs_[tag];

 TAxis* x_pTaxis = LUT_->GetXaxis(); TAxis* y_etaaxis = LUT_->GetYaxis();
 double maxPt = x_pTaxis->GetXmax(); double minPt = x_pTaxis->GetXmin();

 int xbin = x_pTaxis->FindFixBin(pT);
 int ybin = y_etaaxis->FindFixBin(abs(eta));

 double scale = 1.0;
 if(pT>minPt && pT<maxPt){  scale = LUT_->GetBinContent(xbin,ybin);  }

// if(tag == 1 && pT>minPt && pT<maxPt) cout << "xbin: " << xbin << ", ybin: " << ybin << ", scale: " << LUT_->GetBinContent(xbin,ybin) << endl;
// if (tag==1) cout << LUT_->GetXaxis()->GetNbins() << ", " << LUT_->GetYaxis()->GetNbins() << endl;
 return scale;

}


void MySelector::SetPtErrCorrection(TString fs, double pTErrCorr_eta1, double pTErrCorr_eta2, double pTErrCorr_eta3, double pTErrCorr_eta4) {

     fs_ = fs;
     pTErrCorr_eta1_ = pTErrCorr_eta1;
     pTErrCorr_eta2_ = pTErrCorr_eta2;
     pTErrCorr_eta3_ = pTErrCorr_eta3;
     pTErrCorr_eta4_ = pTErrCorr_eta4;

}

void MySelector::SetPtErrCorrection(TString fs, vector<double> pTErrCorr) {

     fs_ = fs;
     pTErrCorr_ = pTErrCorr;

}

void MySelector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

   if (fs_ == "2e") {

      fLUT_1_ = TFile::Open("LUT_"+fs_+"_1.root");
      LUT_1_ = (TH2F*) fLUT_1_->Get(fs_);

      fLUT_2_ = TFile::Open("LUT_"+fs_+"_2.root");
      LUT_2_ = (TH2F*) fLUT_2_->Get(fs_);

      fLUT_3_ = TFile::Open("LUT_"+fs_+"_3.root");
      LUT_3_ = (TH2F*) fLUT_3_->Get(fs_);

      LUTs_[0] = LUT_1_;
      LUTs_[1] = LUT_2_;
      LUTs_[2] = LUT_3_;

      }

}

void MySelector::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

}

Bool_t MySelector::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetEntry(entry);

//   if (nEvents > 100) return kTRUE;

   TLorentzVector lep1, lep2;
   lep1.SetPtEtaPhiM(*pT1,double(*eta1),double(*phi1),*m1);
   lep2.SetPtEtaPhiM(*pT2,double(*eta2),double(*phi2),*m2);

   TLorentzVector lep1p, lep2p;
   lep1p.SetPtEtaPhiM(*pT1+*pterr1,double(*eta1),double(*phi1),*m1);
   lep2p.SetPtEtaPhiM(*pT2+*pterr2,double(*eta2),double(*phi2),*m2);

   double dm1 = (lep1p+lep2).M()-(lep1+lep2).M();
   double dm2 = (lep1+lep2p).M()-(lep1+lep2).M();
   double massZErr_cal = TMath::Sqrt(dm1*dm1+dm2*dm2);

   double pterr1_corr = *pterr1; double pterr2_corr = *pterr2;

/*
   if (fs_ == "2mu") {

      pterr1_corr *= pTCorr(*pT1, *eta1, fs_, tag_);
      pterr2_corr *= pTCorr(*pT2, *eta2, fs_, tag_);

      }

*/
   if (fs_ == "2e") {

      pterr1_corr *= ApplyCorr(*pT1, *eta1, *pterr1, *lep1_ecalDriven, fs_);   
      pterr2_corr *= ApplyCorr(*pT2, *eta2, *pterr2, *lep2_ecalDriven, fs_);                    

      }
   
/*
   if (*lep1_ecalDriven) {

      if ((*pterr1)/(*pT1) < 0.06) {

         pterr1_corr *= pTCorr(*pT1, *eta1, fs_, tag_);

         } else {pterr1_corr *= 0.94;}

      } else {

             if (abs(*eta1) < 1.44) pterr1_corr *= 2.44838;
             if (abs(*eta1) > 1.44 && abs(*eta1) < 1.6) pterr1_corr *= 4;
             if (abs(*eta1) > 1.6 && abs(*eta1) < 2) pterr1_corr *= 2.55443;
             if (abs(*eta1) > 2 && abs(*eta1) < 2.5) pterr1_corr *= 1.95906;

             }

   if (*lep2_ecalDriven) {

      if ((*pterr2)/(*pT2) < 0.06) {

         pterr2_corr *= pTCorr(*pT2, *eta2, fs_, tag_);

         } else {pterr2_corr *= 0.94;}

      } else {

             if (abs(*eta2) < 1.44) pterr2_corr *= 2.44838;
             if (abs(*eta1) > 1.44 && abs(*eta1) < 1.6) pterr1_corr *= 4;
             if (abs(*eta1) > 1.6 && abs(*eta1) < 2) pterr1_corr *= 2.55443;
             if (abs(*eta1) > 2 && abs(*eta1) < 2.5) pterr1_corr *= 1.95906;

             }

*/

/*   
// mu
   if (fs_ == "2mu") {

      if (abs(*eta1)<0.9) pterr1_corr *= pTErrCorr_eta1_;
      if (abs(*eta1)>=0.9 && abs(*eta1)<=1.8) pterr1_corr *= pTErrCorr_eta2_;
      if (abs(*eta1)>1.8) pterr1_corr *= pTErrCorr_eta3_;

      if (abs(*eta2)<0.9) pterr2_corr *= pTErrCorr_eta1_;
      if (abs(*eta2)>=0.9 && abs(*eta2)<=1.8) pterr2_corr *= pTErrCorr_eta2_;
      if (abs(*eta2)>1.8) pterr2_corr *= pTErrCorr_eta3_;

      }

//e
   if (fs_ == "2e") {

      if (abs(*eta1)<1) pterr1_corr *= pTErrCorr_eta1_;
      if (abs(*eta1)>=1 && abs(*eta1)<=1.44) pterr1_corr *= pTErrCorr_eta2_;
      if (abs(*eta1)>=1.57 && abs(*eta1)<=2) pterr1_corr *= pTErrCorr_eta3_;
      if (abs(*eta1)>2) pterr1_corr *= pTErrCorr_eta4_;

      if (abs(*eta2)<1) pterr2_corr *= pTErrCorr_eta1_;
      if (abs(*eta2)>=1 && abs(*eta2)<=1.44) pterr2_corr *= pTErrCorr_eta2_;
      if (abs(*eta2)>=1.57 && abs(*eta2)<=2) pterr2_corr *= pTErrCorr_eta3_;
      if (abs(*eta2)>2) pterr2_corr *= pTErrCorr_eta4_;

      }
*/
   lep1p.SetPtEtaPhiM(*pT1+pterr1_corr,double(*eta1),double(*phi1),*m1);
   lep2p.SetPtEtaPhiM(*pT2+pterr2_corr,double(*eta2),double(*phi2),*m2);

   double dm1corr = (lep1p+lep2).M()-(lep1+lep2).M();
   double dm2corr = (lep1+lep2p).M()-(lep1+lep2).M();
   double massZErr_cal_corr = TMath::Sqrt(dm1corr*dm1corr+dm2corr*dm2corr);

   nEvents++;
   massZErr_sum += (*massZErr);
   massZErr_sum_rel += (*massZErr)/(*massZ);
   massZErr_sum_corr += massZErr_cal_corr;
   massZErr_sum_rel_corr += massZErr_cal_corr/(*massZ);

//   cout << massZErr_cal << ", " << (*massZErr) << endl;
   return kTRUE;
}

void MySelector::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

}

void MySelector::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

   cout << "nEvents: " << nEvents << endl;
   cout << "massZErr_ave: " << massZErr_sum/nEvents << endl;
   cout << "massZErr_rel_ave: " << massZErr_sum_rel/nEvents << endl;
   cout << "massZErr_ave_corr: " << massZErr_sum_corr/nEvents << endl;
   cout << "massZErr_rel_ave_corr: " << massZErr_sum_rel_corr/nEvents << endl;
}

/* used defined methods */

