#!/home1/ankur.barsode/anaconda3/envs/cgwhl/bin/python
'''
Injection with cogwheel
using the factorized 2-2 mode aligned spins version
gives posteriors within ~5 minutes

Run as
$ python cogwheel_fqas.py inj_data.samples idx
where the PE is run for parameters given by
pd.read_csv('inj_data.samples' , sep=' ', header=0)[idx:idx+1]
'''

import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

path_to_cogwheel = '/home1/ankur.barsode/cogwheel'
import sys
sys.path.append(path_to_cogwheel)

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

from cogwheel import data, gw_prior, likelihood, waveform, sampling
from cogwheel.posterior import Posterior
from bilby.gw import utils # for finding signal duration

# by Mukesh
class PSD:
    def __init__(self, asd_filename, prepend_points = [], append_points = [], is_psd=False, fmin=None, fmax=None):
        self.f_vals, self.asd_vals = np.loadtxt(asd_filename, unpack = True)
        # remove infinities
        max_asd = np.max(self.asd_vals[~np.isinf(self.asd_vals)])
        self.asd_vals[np.isinf(self.asd_vals)] = max_asd
        # keep data within fmin to fmax
        del_idx = np.where((self.f_vals < fmin) + (self.f_vals > fmax))
        self.f_vals = np.delete(self.f_vals, del_idx)
        self.asd_vals = np.delete(self.asd_vals, del_idx)
        self.prepend_points = prepend_points
        self.append_points = append_points
        if is_psd:
            self.asd_vals = np.sqrt(self.asd_vals)
            self.prepend_points = np.sqrt(prepend_points)
            self.append_points = np.sqrt(append_points)

        for point in self.prepend_points:
            self.f_vals = np.concatenate([np.array([point[0]]), self.f_vals])
            self.asd_vals = np.concatenate([np.array([point[1]]), self.asd_vals])

        for point in self.append_points:
            self.f_vals = np.concatenate([self.f_vals, np.array([point[0]])])
            self.asd_vals = np.concatenate([self.asd_vals, np.array([point[1]])])

        self.asd = interp1d(self.f_vals, self.asd_vals, bounds_error=False, fill_value=max_asd)

inj_filename = sys.argv[1]
idx = int(sys.argv[2])
event_name = 'fqas_%d' % idx
parentdir = '.'

df = pd.read_csv(inj_filename , sep=' ', header=0)[idx:idx+1]
inj_params = {key:float(df[key]) for key in df.keys()}
f_min = 20.0
f_max = 2048.0
duration = max([4, utils.calculate_time_to_merger(f_min, inj_params['m1'], inj_params['m2'], chi=0, safety=1.5)])
q = inj_params['m2'] / inj_params['m1']
mchirp_guess = inj_params['m1'] * q**0.6 / (1+q)**0.2 * (0.9 + 0.2 * np.random.random())
approximant = 'IMRPhenomXAS'

H1_asd_fname = '../asd_aligo_O4high.txt'
L1_asd_fname = '../asd_aligo_O4high.txt'
V1_asd_fname = '../asd_avirgo_O4high_NEW.txt'

asd_H1 = PSD(H1_asd_fname, fmin=f_min, fmax=f_max).asd
asd_L1 = PSD(L1_asd_fname, fmin=f_min, fmax=f_max).asd
asd_V1 = PSD(V1_asd_fname, fmin=f_min, fmax=f_max).asd

event_data = data.EventData.gaussian_noise(event_name,
                                           duration=duration,
                                           detector_names="HLV",
                                           asd_funcs=[asd_H1, asd_L1, asd_V1],
                                           tgps=0.0,
                                           fmin=f_min, fmax=f_max)

event_data.inject_signal(par_dic=inj_params, approximant=approximant)

# Plot spectrogram
event_data.specgram((-0.1, 0.1))
plt.savefig('specgrams/%s_%d_specgram.png' % (inj_filename.split('.')[0], idx))
#plt.show()

post = Posterior.from_event(event_data, mchirp_guess, approximant=approximant,
                            prior_class=gw_prior.IntrinsicAlignedSpinLVCPrior,
                            likelihood_class=likelihood.MarginalizedExtrinsicLikelihoodQAS,
                            prior_kwargs={'symmetrize_lnq': True,
                                          'f_ref': inj_params['f_ref'], \
                                          'd_luminosity_max': 1.5e4, 'dt0':0.1})

print(post.prior.get_init_dict())

post.likelihood.lnlike(post.likelihood.par_dic_0)

'''
pym = sampling.PyMultiNest(post)
pym.run_kwargs['n_live_points'] = 1000
sampler = pym
rundir = sampler.get_rundir(parentdir)
sampler.run(rundir)
'''
sampler = sampling.Dynesty(post)
sampler.run_kwargs['nlive'] = 1000
rundir = sampler.get_rundir(parentdir)
sampler.run(rundir)

print('PE finished for %s %d\n\tRundir: %s' % (inj_filename, idx, rundir))
