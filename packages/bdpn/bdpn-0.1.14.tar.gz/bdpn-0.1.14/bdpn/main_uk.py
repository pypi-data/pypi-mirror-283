import numpy as np

from bdpn import bd_model

from bdpn.bdpn_model import preprocess_forest, loglikelihood
from bdpn.tree_manager import read_forest, get_T

forest = read_forest('/home/azhukova/projects/bdpn/hiv_b_uk/data/forest.2012_2015.0.nwk')
preprocess_forest(forest)
T = get_T(T=None, forest=forest)
lk_bdpn = loglikelihood(forest, rho=0.58, la=0.68889114, psi=0.54633669, upsilon=0, phi=1, T=T)
print(lk_bdpn)
print('---------------------')
lk_bd = bd_model.loglikelihood(forest, rho=0.58, la=0.68889114, psi=0.54633669, T=T)
print(lk_bd)