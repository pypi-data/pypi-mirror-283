import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
sys.path.append('..')

import matplotlib.pyplot as plt
import pandas as pd

from cogwheel import data
from cogwheel import gw_plotting
from cogwheel import posterior
from cogwheel import sampling
import cogwheel.waveform_models.xode

parentdir = 'xode'  # Parameter estimation runs will be saved here

# eventname = 'GW190412'
eventname = 'GW191109_010717'

mchirp_guess = data.EVENTS_METADATA['mchirp'][eventname]

post = posterior.Posterior.from_event(eventname,
                                      mchirp_guess,
                                      approximant='IMRPhenomXODE',
                                      prior_class='IntrinsicIASPrior')

pym = sampling.PyMultiNest(post, run_kwargs={'n_live_points': 1024})
rundir = pym.get_rundir(parentdir)
pym.run(rundir)  # Will take a bit

samples = pd.read_feather(rundir/sampling.SAMPLES_FILENAME)
gw_plotting.CornerPlot(samples[post.prior.sampled_params]).plot()
plt.savefig(rundir/f'{eventname}.pdf', bbox_inches='tight')
