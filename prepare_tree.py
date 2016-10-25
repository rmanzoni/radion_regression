import ROOT
import copy
import itertools
from array import array
from operator import itemgetter


def find_bjets(jet_collection, csv_vector, min_pt=20., max_eta=2.4):
	bjets = []
	for i, jet in enumerate(jet_collection):
		if jet.Pt() >= min_pt and abs(jet.Eta()) <= max_eta:
			bjets.append([jet, csv_vector[i], i])
	ntagged = len([bb for bb in bjets if bb[1]>0.605])
	return bjets, ntagged


def getKinFitIndex(indexes, nbjets):
    imin = min(indexes)
    imax = max(indexes)
    #if nbjets < 2 or imin == imax or imin >= nbjets or imax >= nbjets:
    #    import pdb ; pdb.set_trace()
    return imax - 1 + imin * (2 * nbjets - 3 - imin) / 2


chain = ROOT.TChain('muTau')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_250.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_260.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_270.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_280.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_320.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_340.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_450.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_500.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_550.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_600.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_650.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_700.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_750.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_800.root')
chain.Add('/afs/cern.ch/work/f/fbrivio/public/per_Ric/TT_studies/signals/out_signal_900.root')

ntuple_training = ROOT.TNtuple('tree','tree',
    'run'\
    ':lumi'\
    ':evt'\
    ':pt_mu'\
    ':eta_mu'\
    ':phi_mu'\
    ':mass_mu'\
    ':pt_tau'\
    ':eta_tau'\
    ':phi_tau'\
    ':mass_tau'\
    ':pt_bj1'\
    ':eta_bj1'\
    ':phi_bj1'\
    ':mass_bj1'\
    ':pt_bj2'\
    ':eta_bj2'\
    ':phi_bj2'\
    ':mass_bj2'\
    ':pt_jj'\
    ':eta_jj'\
    ':phi_jj'\
    ':mass_jj'\
    ':pt_sv'\
    ':eta_sv'\
    ':phi_sv'\
    ':mass_sv'\
    ':mass_kf'\
    ':chi2_kf'\
    ':prob_kf'\
    ':conv_kf'\
    ':dr_bb'\
    ':dr_bbsv'\
    ':phi_met'\
    ':pt_met'\
    ':gen_mass'\
)

ntuple_test = copy.deepcopy(ntuple_training)

tot_events = chain.GetEntries()

for i, ev in enumerate(chain):

    if i%1000==0: 
        print '====> processing %d/%d events, %.1f%s' %(i, tot_events, 100.*float(i)/float(tot_events), ' %')
    
#     if i>5000: 
#         break
    
    bj1 = ROOT.TLorentzVector()
    bj2 = ROOT.TLorentzVector()
    jj  = bj1 + bj2
    

    bjets, ntagged = find_bjets(ev.jets_p4, ev.jets_csv)
    bjets.sort(key=itemgetter(1), reverse=True)

    if len(bjets) > 0: 
        bj1.SetPtEtaPhiM(bjets[0][0].pt(), bjets[0][0].eta(), bjets[0][0].phi(), bjets[0][0].mass())
        bj1_index = bjets[0][2]
    if len(bjets) > 1: 
        bj2.SetPtEtaPhiM(bjets[1][0].pt(), bjets[1][0].eta(), bjets[1][0].phi(), bjets[1][0].mass())
        bj2_index = bjets[1][2]

    if len(bjets) > 1: jj = bj1 + bj2
    
    ii = getKinFitIndex( (bj1_index, bj2_index), ntagged)
    
    try:
        kinFit_m           = ev.kinFit_m          [ii]
        kinFit_chi2        = ev.kinFit_chi2       [ii]
        kinFit_probability = ev.kinFit_probability[ii]
        kinFit_convergence = ev.kinFit_convergence[ii]
    except:
        kinFit_m           = 0.
        kinFit_chi2        = 0.
        kinFit_probability = 0.
        kinFit_convergence = -1.
        
    tofill = array(
        'f',
        [
         ev.run,
         ev.lumi,
         ev.evt,

         ev.p4_1.pt(),
         ev.p4_1.eta(),
         ev.p4_1.phi(),
         ev.p4_1.mass(),

         ev.p4_2.pt(),
         ev.p4_2.eta(),
         ev.p4_2.phi(),
         ev.p4_2.mass(),

         bj1.Pt(),
         bj1.Eta(),
         bj1.Phi(),
         bj1.M(),

         bj2.Pt(),
         bj2.Eta(),
         bj2.Phi(),
         bj2.M(),

         jj.Pt(),
         jj.Eta(),
         jj.Phi(),
         jj.M(),

         ev.SVfit_p4.pt(),
         ev.SVfit_p4.eta(),
         ev.SVfit_p4.phi(),
         ev.SVfit_p4.mass(),

         kinFit_m          ,
         kinFit_chi2       ,
         kinFit_probability,
         kinFit_convergence,
         
         ev.dR_bb,
         ev.dR_bbsv,
         
         ev.pfMET_p4.phi(),
         ev.pfMET_p4.pt(),
         
         ev.gen_mass,
        ]
    )

    if i%2==0: 
        #print 'pari'
        ntuple_test.Fill(tofill)
    else:
        #print 'dispari'
        ntuple_training.Fill(tofill)


f1 = ROOT.TFile('signals_training.root', 'recreate')
f1.cd()
ntuple_training.Write()
f1.Close()        

f2 = ROOT.TFile('signals_test.root', 'recreate')
f2.cd()
ntuple_test.Write()
f2.Close()        






