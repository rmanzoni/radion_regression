# radion_regression
BDT regression for di-Higgs → bb ττ


```
# read, flatten and merge the different signal trees
# this produces two trees with the same number of events, one for training and one for testing

ipython prepare_tree.py

# run the regression
ipython tmva_4body_mass_regression.py  

# apply the regression to the test tree and produce an 'enhanced' tree containing the outcome of the regression (which is the radion mass)
ipython reader.py  

# check the results
root -l signals_training_enriched.root

# draw both kinfit and BDT radion mass for a given mass point
tree->Draw("mass_kf", "gen_mass==600")
tree->Draw("resonant_mass", "gen_mass==600", "SAMES")

# check residuals
tree->Draw("resonant_mass-gen_mass", "gen_mass==600")
```

