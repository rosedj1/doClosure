//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Oct 21 15:08:20 2016 by ROOT version 6.06/01
// from TTree passedEvents/passedEvents
// found on file: /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/Ana_ZZ4L/Ntuples/mH_125.root
//////////////////////////////////////////////////////////

#ifndef MySelector_m4l_h
#define MySelector_m4l_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

// Headers needed by this particular selector


class MySelector_m4l : public TSelector {
public :
   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain = 0;   //!pointer to the analyzed TTree or TChain

   // Readers to access the data (delete the ones you do not need).
/*
   TTreeReaderValue<ULong64_t> Run = {fReader, "Run"};
   TTreeReaderValue<ULong64_t> Event = {fReader, "Event"};
   TTreeReaderValue<ULong64_t> LumiSect = {fReader, "LumiSect"};
   TTreeReaderValue<Int_t> nVtx = {fReader, "nVtx"};
   TTreeReaderValue<Bool_t> passedTrig = {fReader, "passedTrig"};
*/
   TTreeReaderValue<Bool_t> passedFullSelection = {fReader, "passedFullSelection"};
/*  TTreeReaderValue<Bool_t> passedFiducialSelection = {fReader, "passedFiducialSelection"};
   TTreeReaderValue<Bool_t> passedZ4lSelection = {fReader, "passedZ4lSelection"};
   TTreeReaderValue<Bool_t> passedZXCRSelection = {fReader, "passedZXCRSelection"};
   TTreeReaderValue<Int_t> nZXCRFailedLeptons = {fReader, "nZXCRFailedLeptons"};
*/
   TTreeReaderValue<Int_t> finalState = {fReader, "finalState"};
/*   TTreeReaderValue<Float_t> GENMH = {fReader, "GENMH"};
   TTreeReaderValue<Float_t> GENmass4l = {fReader, "GENmass4l"};
   TTreeReaderValue<Float_t> dataMCWeight = {fReader, "dataMCWeight"};
   TTreeReaderValue<Float_t> k_qqZZ_qcd_M = {fReader, "k_qqZZ_qcd_M"};
   TTreeReaderValue<Float_t> k_qqZZ_ewk = {fReader, "k_qqZZ_ewk"};
   TTreeReaderValue<Float_t> k_ggZZ = {fReader, "k_ggZZ"};
*/
   TTreeReaderValue<Float_t> pTL1 = {fReader, "pTL1"};
   TTreeReaderValue<Float_t> pTL2 = {fReader, "pTL2"};
   TTreeReaderValue<Float_t> pTL3 = {fReader, "pTL3"};
   TTreeReaderValue<Float_t> pTL4 = {fReader, "pTL4"};
   TTreeReaderValue<Int_t> idL1 = {fReader, "idL1"};
   TTreeReaderValue<Int_t> idL2 = {fReader, "idL2"};
   TTreeReaderValue<Int_t> idL3 = {fReader, "idL3"};
   TTreeReaderValue<Int_t> idL4 = {fReader, "idL4"};
   TTreeReaderValue<Float_t> etaL1 = {fReader, "etaL1"};
   TTreeReaderValue<Float_t> etaL2 = {fReader, "etaL2"};
   TTreeReaderValue<Float_t> etaL3 = {fReader, "etaL3"};
   TTreeReaderValue<Float_t> etaL4 = {fReader, "etaL4"};
   TTreeReaderValue<Float_t> phiL1 = {fReader, "phiL1"};
   TTreeReaderValue<Float_t> phiL2 = {fReader, "phiL2"};
   TTreeReaderValue<Float_t> phiL3 = {fReader, "phiL3"};
   TTreeReaderValue<Float_t> phiL4 = {fReader, "phiL4"};
   TTreeReaderValue<Float_t> mL1 = {fReader, "mL1"};
   TTreeReaderValue<Float_t> mL2 = {fReader, "mL2"};
   TTreeReaderValue<Float_t> mL3 = {fReader, "mL3"};
   TTreeReaderValue<Float_t> mL4 = {fReader, "mL4"};
   TTreeReaderValue<Float_t> pTErrL1 = {fReader, "pTErrL1"};
   TTreeReaderValue<Float_t> pTErrL2 = {fReader, "pTErrL2"};
   TTreeReaderValue<Float_t> pTErrL3 = {fReader, "pTErrL3"};
   TTreeReaderValue<Float_t> pTErrL4 = {fReader, "pTErrL4"};
   TTreeReaderValue<Float_t> mass4l = {fReader, "mass4l"};
   TTreeReaderValue<Float_t> mass4lErr = {fReader, "mass4lErr"};
   TTreeReaderValue<Float_t> mass4lREFIT = {fReader, "mass4lREFIT"};
   TTreeReaderValue<Float_t> mass4lErrREFIT = {fReader, "mass4lErrREFIT"};
   TTreeReaderValue<Float_t> mass4mu = {fReader, "mass4mu"};
   TTreeReaderValue<Float_t> mass4e = {fReader, "mass4e"};
   TTreeReaderValue<Float_t> mass2e2mu = {fReader, "mass2e2mu"};
/*
   TTreeReaderValue<Float_t> pT4l = {fReader, "pT4l"};
   TTreeReaderValue<Float_t> massZ1 = {fReader, "massZ1"};
   TTreeReaderValue<Float_t> massZ2 = {fReader, "massZ2"};
   TTreeReaderValue<Int_t> njets_pt30_eta4p7 = {fReader, "njets_pt30_eta4p7"};
   TTreeReaderValue<Double_t> pTj1 = {fReader, "pTj1"};
   TTreeReaderValue<Double_t> etaj1 = {fReader, "etaj1"};
   TTreeReaderValue<Double_t> pTj2 = {fReader, "pTj2"};
   TTreeReaderValue<Double_t> etaj2 = {fReader, "etaj2"};
   TTreeReaderValue<Double_t> D_bkg_kin = {fReader, "D_bkg_kin"};
   TTreeReaderValue<Double_t> D_bkg = {fReader, "D_bkg"};
   TTreeReaderValue<Double_t> Dgg10_VAMCFM = {fReader, "Dgg10_VAMCFM"};
   TTreeReaderValue<Double_t> D_g4 = {fReader, "D_g4"};
   TTreeReaderValue<Double_t> Djet_VAJHU = {fReader, "Djet_VAJHU"};
   TTreeReaderValue<Double_t> D_VBF1j_VAJHU = {fReader, "D_VBF1j_VAJHU"};
   TTreeReaderValue<Double_t> D_WHh_VAJHU = {fReader, "D_WHh_VAJHU"};
   TTreeReaderValue<Double_t> D_ZHh_VAJHU = {fReader, "D_ZHh_VAJHU"};
   TTreeReaderValue<Double_t> D_VBF2j = {fReader, "D_VBF2j"};
   TTreeReaderValue<Double_t> D_VBF1j = {fReader, "D_VBF1j"};
   TTreeReaderValue<Double_t> D_WHh = {fReader, "D_WHh"};
   TTreeReaderValue<Double_t> D_ZHh = {fReader, "D_ZHh"};
*/

   int nEvents;
   double mass4lErr_uncorr_sum;
   double mass4lErr_corr_sum;
   double mass4lErrREFIT_corr_sum;

   MySelector_m4l(TTree * /*tree*/ =0):
     nEvents(0), mass4lErr_uncorr_sum(0), mass4lErr_corr_sum(0), mass4lErrREFIT_corr_sum(0) { }
   virtual ~MySelector_m4l() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   ClassDef(MySelector_m4l,0);

};

#endif

#ifdef MySelector_m4l_cxx
void MySelector_m4l::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t MySelector_m4l::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}


#endif // #ifdef MySelector_m4l_cxx
