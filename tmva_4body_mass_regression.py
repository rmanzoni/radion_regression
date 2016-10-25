import ROOT
from ROOT import TMVA


# Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI
ROOT.gROOT.SetMacroPath( './' )
ROOT.gROOT.Macro       ( './TMVAlogon.C' )    
ROOT.gROOT.LoadMacro   ( './TMVAGui.C' )

outfname = 'TMVAReg.root'
f_out = ROOT.TFile.Open( outfname, 'recreate' )

# Create the factory object. Later you can choose the methods
# whose performance you'd like to investigate. The factory will
# then run the performance analysis for you.
#
# The first argument is the base of the name of all the
# weightfiles in the directory weight/ 
#
# The second argument is the output file for the training results
# All TMVA output can be suppressed by removing the '!' (not) in 
# front of the 'Silent' argument in the option string
factory = TMVA.Factory( 'TMVARegression', f_out, '!V:!Silent:Color:DrawProgressBar' )

# Set verbosity
factory.SetVerbose( True )


# Define the input variables that shall be used for the classifier training
# note that you may also use variable expressions, such as: '3*var1/var2*abs(var3)'
# [all types of expressions that can also be parsed by TTree::Draw( 'expression' )]
# factory.AddVariable( 'mvaMET_p4.pt()' , 'F' ) # why no MVA MET?
# factory.AddVariable( 'mvaMET_p4.phi()', 'F' ) # why no MVA MET?


factory.AddVariable( 'pt_mu'    , 'F' )
factory.AddVariable( 'eta_mu'   , 'F' )
factory.AddVariable( 'phi_mu'   , 'F' )
# factory.AddVariable( 'mass_mu'  , 'F' )

factory.AddVariable( 'pt_tau'   , 'F' )
factory.AddVariable( 'eta_tau'  , 'F' )
factory.AddVariable( 'phi_tau'  , 'F' )
factory.AddVariable( 'mass_tau' , 'F' )

factory.AddVariable( 'pt_bj1'   , 'F' )
factory.AddVariable( 'eta_bj1'  , 'F' )
factory.AddVariable( 'phi_bj1'  , 'F' )
factory.AddVariable( 'mass_bj1' , 'F' )

factory.AddVariable( 'pt_bj2'   , 'F' )
factory.AddVariable( 'eta_bj2'  , 'F' )
factory.AddVariable( 'phi_bj2'  , 'F' )
factory.AddVariable( 'mass_bj2' , 'F' )

factory.AddVariable( 'pt_jj'    , 'F' )
factory.AddVariable( 'eta_jj'   , 'F' )
factory.AddVariable( 'phi_jj'   , 'F' )
factory.AddVariable( 'mass_jj'  , 'F' )

factory.AddVariable( 'pt_sv'    , 'F' )
factory.AddVariable( 'eta_sv'   , 'F' )
factory.AddVariable( 'phi_sv'   , 'F' )
factory.AddVariable( 'mass_sv'  , 'F' )

factory.AddVariable( 'mass_kf'  , 'F' )
factory.AddVariable( 'chi2_kf'  , 'F' )
factory.AddVariable( 'prob_kf'  , 'F' )
factory.AddVariable( 'conv_kf'  , 'F' )

factory.AddVariable( 'dr_bb'    , 'F' )
factory.AddVariable( 'dr_bbsv'  , 'F' )

factory.AddVariable( 'phi_met'  , 'F' )
factory.AddVariable( 'pt_met'   , 'F' )
  

# Add the variable carrying the regression target
factory.AddTarget( 'gen_mass' )

# Open input file
f_in  = ROOT.TFile.Open('signals_training.root')
# Register the regression tree
regTree = f_in.Get( 'tree' )
# global event weights per tree (see below for setting event-wise weights
regWeight  = 1.

# You can add an arbitrary number of regression trees
factory.AddRegressionTree(regTree, regWeight)

# Apply additional cuts on the signal and background sample. 
# example for cut: mycut = TCut( 'abs(var1)<0.5 && abs(var2-0.5)<1' )

mycut = ROOT.TCut(
''
) 


# tell the factory to use all remaining events in the trees after training for testing:
factory.PrepareTrainingAndTestTree( 
    mycut, 
    ':'.join([
        'nTrain_Regression=0',
        'nTest_Regression=1000',
        'SplitMode=Random',
        'NormMode=NumEvents',
        '!V'
    ]) 
)


factory.BookMethod(
    TMVA.Types.kBDT, 
    'BDTG',
    ':'.join([
        'H',
        'V',
        'NTrees=100',
        'BoostType=Grad',
        'Shrinkage=0.2',
        'UseBaggedBoost',
        'BaggedSampleFraction=0.5',
        'nCuts=1000',
        'MaxDepth=4',
        'MinNodeSize=0.10',
    ])
)

# ---- Now you can tell the factory to train, test, and evaluate the MVAs

# Train MVAs using the set of training events
factory.TrainAllMethods()

# ---- Evaluate all MVAs using the set of test events
factory.TestAllMethods()

# ----- Evaluate and compare performance of all configured MVAs
factory.EvaluateAllMethods()

# --------------------------------------------------------------

# Save the output
f_out.Close()
   
# open the GUI for the result macros    
# ROOT.gROOT.ProcessLine( "TMVAGui(\"%s\")" % outfname )
TMVA.TMVARegGui(outfname)
# keep the ROOT thread running
ROOT.gApplication.Run() 