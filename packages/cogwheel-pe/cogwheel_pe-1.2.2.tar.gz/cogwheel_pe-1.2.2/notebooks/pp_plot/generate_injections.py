import os
os.environ["OMP_NUM_THREADS"] = "1"

import sys
import multiprocessing
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from . import config
from .injection_prior import InjectionPrior
sys.path.append(config.COGWHEEL_PATH)

from cogwheel import data
from cogwheel import likelihood
from cogwheel import waveform


N_CORES = multiprocessing.cpu_count()  # How many cores to use, edit if desired

event_data = data.EventData.gaussian_noise(
    '', 120, config.DETECTOR_NAMES, config.ASDS, 0)

waveform_generator = waveform.WaveformGenerator.from_event_data(
    event_data, 'IMRPhenomXPHM')


def _get_h_h(like, par_dic):
    return np.sum(like._get_dh_hh_no_asd_drift(par_dic)[1])


def _compute_h_h_1mpc(injections, pn_phase_tol, n_cores=N_CORES):
    """Compute ⟨ℎ∣ℎ⟩ at 1 Mpc, at fixed `pn_phase_tol`."""
    par_dic_0 = dict(injections.median(), d_luminosity=1, t_geocenter=0)

    like = likelihood.RelativeBinningLikelihood(
        event_data, waveform_generator, par_dic_0, pn_phase_tol=pn_phase_tol)

    par_dics = ({**row, 'd_luminosity': 1, 't_geocenter': 0}
                for _, row in injections.iterrows())

    with multiprocessing.Pool(n_cores) as pool:
        h_h_1mpc = pool.starmap(_get_h_h,
                                ((like, par_dic) for par_dic in par_dics))
    return h_h_1mpc


def compute_h_h_1mpc(injections, rtol=1e-3, verbose=True):
    """
    Compute ⟨ℎ∣ℎ⟩ at 1 Mpc, ensuring a relative accuracy of `rtol`.

    Parameters
    ----------
    injections: pd.DataFrame
        Samples including all parameters except for time and distance.

    rtol: float
        Relative tolerance in ⟨ℎ∣ℎ⟩ computation.

    Return
    ------
    h_h_1mpc, relative_error: float arrays, same length as `injections`.
    """
    pn_phase_tol = .01
    h_h_1mpc = _compute_h_h_1mpc(injections, pn_phase_tol)
    h_h_1mpc_lowres = np.empty_like(h_h_1mpc)
    recompute = np.ones(len(injections), bool)
    while any(recompute):
        pn_phase_tol /= 2
        h_h_1mpc_lowres[recompute] = h_h_1mpc[recompute]
        h_h_1mpc[recompute] = _compute_h_h_1mpc(injections[recompute],
                                                pn_phase_tol)
        relative_error = np.abs(h_h_1mpc / h_h_1mpc_lowres - 1)

        if verbose:
            print(f'n = {np.count_nonzero(recompute)}'
                  f'pn_phase_tol = {pn_phase_tol}',
                  f'⟨ℎ∣ℎ⟩ relative error = {relative_error.max():.2g}')

        recompute = relative_error > rtol

    return h_h_1mpc


def test_h_h_distribution(injections_above_threshold):
    """Plot test that distribution of ⟨ℎ∣ℎ⟩ is as expected."""
    h_h_distribution = stats.pareto(b=1.5, scale=config.H_H_MIN)

    plt.figure()
    x = np.geomspace(config.H_H_MIN,
                     1.2 * injections_above_threshold['h_h'].max(),
                     100)

    # Predicted distribution
    plt.plot(x, h_h_distribution.pdf(x), c='C1', label='Prediction')

    # Monte Carlo of what distribution should look like with these many samples
    for i in range(20):
        plt.hist(h_h_distribution.rvs(size=len(injections_above_threshold)),
                 bins=x, density=True, histtype='step', alpha=.3,
                 label='Monte Carlo' if i == 0 else None)

    # Actual outcome
    plt.hist(injections_above_threshold['h_h'],
             bins=x, density=True, label='Outcome')

    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(rf'$\langle h \mid h \rangle_{{>{config.H_H_MIN}}}$')
    plt.ylabel('PDF')
    plt.title(rf'$N_{{\rm samples}} = {len(injections_above_threshold)}$')


def _gen_injections_above_threshold(mchirp_range, n_total_injections):
    """
    Generate a batch of injections that pass the ⟨ℎ∣ℎ⟩ threshold.
    The number of injections that will pass the threshold is
    unknown in advance.
    """
    injection_prior = InjectionPrior(mchirp_range=mchirp_range,
                                     detector_pair='H',
                                     tgps=0.,
                                     f_ref=50)
    injections = injection_prior.generate_random_samples(n_total_injections)
    h_h_1mpc = compute_h_h_1mpc(injections)

    # Choose physical units for distance, so that the loudest signal
    # placed at d_ref barely makes the threshold
    d_ref = np.sqrt(np.max(h_h_1mpc) / config.H_H_MIN)

    injections['d_luminosity'] = injections['dimensionless_distance'] * d_ref
    del injections['dimensionless_volume']
    del injections['dimensionless_distance']

    injections['h_h'] = h_h_1mpc / injections['d_luminosity']**2
    injections_above_threshold = injections[injections['h_h'] > config.H_H_MIN
                                           ].reset_index(drop=True)
    return injections_above_threshold


def gen_injections_above_threshold(mchirp_range):
    injections_above_threshold = pd.DataFrame()
    batch_size = 10 * config.MIN_N_INJECTIONS_ABOVE_THRESHOLD

    while (len(injections_above_threshold)
           < config.MIN_N_INJECTIONS_ABOVE_THRESHOLD):
        injections_above_threshold = pd.concat(
            (injections_above_threshold,
             _gen_injections_above_threshold(mchirp_range, batch_size)))

    return injections_above_threshold