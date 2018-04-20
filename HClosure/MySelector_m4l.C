#define MySelector_m4l_cxx
// The class definition in MySelector_m4l.C.h has been generated automatically
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
// root> T->Process("MySelector_m4l.C.C")
// root> T->Process("MySelector_m4l.C.C","some options")
// root> T->Process("MySelector_m4l.C.C+")
//


#include "MySelector_m4l.h"
#include <TH2.h>
#include <TStyle.h>

void MySelector_m4l::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
}

void MySelector_m4l::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

}

Bool_t MySelector_m4l::Process(Long64_t entry)
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

   TLorentzVector lep1, lep2, lep3, lep4;
   lep1.SetPtEtaPhiM(*pTL1,double(*etaL1),double(*phiL1),*mL1);
   lep2.SetPtEtaPhiM(*pTL2,double(*etaL2),double(*phiL2),*mL2);
   lep3.SetPtEtaPhiM(*pTL3,double(*etaL3),double(*phiL3),*mL3);
   lep4.SetPtEtaPhiM(*pTL4,double(*etaL4),double(*phiL4),*mL4);

   TLorentzVector lep1p, lep2p, lep3p, lep4p;
   lep1p.SetPtEtaPhiM(*pTL1+*pTErrL1,double(*etaL1),double(*phiL1),*mL1);
   lep2p.SetPtEtaPhiM(*pTL2+*pTErrL2,double(*etaL2),double(*phiL2),*mL2);
   lep3p.SetPtEtaPhiM(*pTL3+*pTErrL3,double(*etaL3),double(*phiL3),*mL3);
   lep4p.SetPtEtaPhiM(*pTL4+*pTErrL4,double(*etaL4),double(*phiL4),*mL4);

   double dm1 = (lep1p+lep2+lep3+lep4).M()-(lep1+lep2+lep3+lep4).M();
   double dm2 = (lep1+lep2p+lep3+lep4).M()-(lep1+lep2+lep3+lep4).M();
   double dm3 = (lep1+lep2+lep3p+lep4).M()-(lep1+lep2+lep3+lep4).M();
   double dm4 = (lep1+lep2+lep3+lep4p).M()-(lep1+lep2+lep3+lep4).M();

   double mass4lErr_cal = TMath::Sqrt(dm1*dm1+dm2*dm2+dm3*dm3+dm4*dm4);

   nEvents++;
   mass4lErr_uncorr_sum += mass4lErr_cal;
   mass4lErr_corr_sum += *mass4lErr;
   mass4lErrREFIT_corr_sum += *mass4lErrREFIT;

   return kTRUE;
}

void MySelector_m4l::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

}

void MySelector_m4l::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

   cout << "nEvents: " << nEvents << endl;
   cout << "mass4l_uncorr: " << mass4lErr_uncorr_sum/nEvents << endl;
   cout << "mass4l_corr: " << mass4lErr_corr_sum/nEvents << endl;
   cout << "mass4lREFIT_corr: " << mass4lErrREFIT_corr_sum/nEvents << endl;
  
}
