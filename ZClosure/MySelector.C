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

