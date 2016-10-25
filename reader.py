import ROOT
import array

reader = ROOT.TMVA.Reader()

pt_mu    = array.array('f',[0])
eta_mu   = array.array('f',[0])
phi_mu   = array.array('f',[0])
# mass_m   = array.array('f',[0])

pt_tau   = array.array('f',[0])
eta_tau  = array.array('f',[0])
phi_tau  = array.array('f',[0])
mass_tau = array.array('f',[0])

pt_bj1   = array.array('f',[0])
eta_bj1  = array.array('f',[0])
phi_bj1  = array.array('f',[0])
mass_bj1 = array.array('f',[0])

pt_bj2   = array.array('f',[0])
eta_bj2  = array.array('f',[0])
phi_bj2  = array.array('f',[0])
mass_bj2 = array.array('f',[0])

pt_jj    = array.array('f',[0])
eta_jj   = array.array('f',[0])
phi_jj   = array.array('f',[0])
mass_jj  = array.array('f',[0])

pt_sv    = array.array('f',[0])
eta_sv   = array.array('f',[0])
phi_sv   = array.array('f',[0])
mass_sv  = array.array('f',[0])

mass_kf  = array.array('f',[0])
chi2_kf  = array.array('f',[0])
prob_kf  = array.array('f',[0])
conv_kf  = array.array('f',[0])

dr_bb    = array.array('f',[0])
dr_bbsv  = array.array('f',[0])

phi_met  = array.array('f',[0])
pt_met   = array.array('f',[0])

reader.AddVariable( 'pt_mu'    , pt_mu    )
reader.AddVariable( 'eta_mu'   , eta_mu   )
reader.AddVariable( 'phi_mu'   , phi_mu   )
# reader.AddVariable( 'mass_mu'  , mass_m   )

reader.AddVariable( 'pt_tau'   , pt_tau   )
reader.AddVariable( 'eta_tau'  , eta_tau  )
reader.AddVariable( 'phi_tau'  , phi_tau  )
reader.AddVariable( 'mass_tau' , mass_tau )

reader.AddVariable( 'pt_bj1'   , pt_bj1   )
reader.AddVariable( 'eta_bj1'  , eta_bj1  )
reader.AddVariable( 'phi_bj1'  , phi_bj1  )
reader.AddVariable( 'mass_bj1' , mass_bj1 )

reader.AddVariable( 'pt_bj2'   , pt_bj2   )
reader.AddVariable( 'eta_bj2'  , eta_bj2  )
reader.AddVariable( 'phi_bj2'  , phi_bj2  )
reader.AddVariable( 'mass_bj2' , mass_bj2 )

reader.AddVariable( 'pt_jj'    , pt_jj    )
reader.AddVariable( 'eta_jj'   , eta_jj   )
reader.AddVariable( 'phi_jj'   , phi_jj   )
reader.AddVariable( 'mass_jj'  , mass_jj  )

reader.AddVariable( 'pt_sv'    , pt_sv    )
reader.AddVariable( 'eta_sv'   , eta_sv   )
reader.AddVariable( 'phi_sv'   , phi_sv   )
reader.AddVariable( 'mass_sv'  , mass_sv  )

reader.AddVariable( 'mass_kf'  , mass_kf  )
reader.AddVariable( 'chi2_kf'  , chi2_kf  )
reader.AddVariable( 'prob_kf'  , prob_kf  )
reader.AddVariable( 'conv_kf'  , conv_kf  )

reader.AddVariable( 'dr_bb'    , dr_bb    )
reader.AddVariable( 'dr_bbsv'  , dr_bbsv  )

reader.AddVariable( 'phi_met'  , phi_met  )
reader.AddVariable( 'pt_met'   , pt_met   )


reader.BookMVA('BDTG','weights/TMVARegression_BDTG.weights.xml')


ntuple_enriched = ROOT.TNtuple('tree','tree',
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
    ':resonant_mass'\
)






f1 = ROOT.TFile.Open('signals_test.root', 'read')
t1 = f1.Get('tree')

tot_events = t1.GetEntries()

for i, ev in enumerate(t1):
    if i%1000==0: 
        print '====> processing %d/%d events, %.1f%s' %(i, tot_events, 100.*float(i)/float(tot_events), ' %')

    pt_mu   [0] = ev.pt_mu   
    eta_mu  [0] = ev.eta_mu  
    phi_mu  [0] = ev.phi_mu  

    pt_tau  [0] = ev.pt_tau  
    eta_tau [0] = ev.eta_tau 
    phi_tau [0] = ev.phi_tau 
    mass_tau[0] = ev.mass_tau

    pt_bj1  [0] = ev.pt_bj1  
    eta_bj1 [0] = ev.eta_bj1 
    phi_bj1 [0] = ev.phi_bj1 
    mass_bj1[0] = ev.mass_bj1

    pt_bj2  [0] = ev.pt_bj2  
    eta_bj2 [0] = ev.eta_bj2 
    phi_bj2 [0] = ev.phi_bj2 
    mass_bj2[0] = ev.mass_bj2

    pt_jj   [0] = ev.pt_jj   
    eta_jj  [0] = ev.eta_jj  
    phi_jj  [0] = ev.phi_jj  
    mass_jj [0] = ev.mass_jj 

    pt_sv   [0] = ev.pt_sv   
    eta_sv  [0] = ev.eta_sv  
    phi_sv  [0] = ev.phi_sv  
    mass_sv [0] = ev.mass_sv 

    mass_kf [0] = ev.mass_kf 
    chi2_kf [0] = ev.chi2_kf 
    prob_kf [0] = ev.prob_kf 
    conv_kf [0] = ev.conv_kf 

    dr_bb   [0] = ev.dr_bb   
    dr_bbsv [0] = ev.dr_bbsv 

    phi_met [0] = ev.phi_met 
    pt_met  [0] = ev.pt_met  

    resonant_mass = reader.EvaluateRegression('BDTG')[0]

    #import pdb ; pdb.set_trace()
    
    tofill = array.array(
        'f',
        [
         ev.run,
         ev.lumi,
         ev.evt,

         ev.pt_mu   ,
         ev.eta_mu  ,
         ev.phi_mu  ,
         ev.mass_mu ,

         ev.pt_tau  ,
         ev.eta_tau ,
         ev.phi_tau ,
         ev.mass_tau,

         ev.pt_bj1  ,
         ev.eta_bj1 ,
         ev.phi_bj1 ,
         ev.mass_bj1,

         ev.pt_bj2  ,
         ev.eta_bj2 ,
         ev.phi_bj2 ,
         ev.mass_bj2,

         ev.pt_jj   ,
         ev.eta_jj  ,
         ev.phi_jj  ,
         ev.mass_jj ,

         ev.pt_sv   ,
         ev.eta_sv  ,
         ev.phi_sv  ,
         ev.mass_sv ,

         ev.mass_kf ,
         ev.chi2_kf ,
         ev.prob_kf ,
         ev.conv_kf ,

         ev.dr_bb   ,
         ev.dr_bbsv ,

         ev.phi_met ,
         ev.pt_met  ,

         ev.gen_mass,
         resonant_mass,
        ]
    )
  
    ntuple_enriched.Fill(tofill)


f1 = ROOT.TFile('signals_training_enriched.root', 'recreate')
f1.cd()
ntuple_enriched.Write()
f1.Close()        


