import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess

# Perform LOWESS regression on GC content and coverage

def perform_lowess(gc_contents, coverages, frac):
    
    """
    The function `perform_lowess` performs LOWESS regression on GC content and coverage data to
    calculate a weighted coverage value.
    
    :param gc_contents: It seems like you were about to provide some information about the `gc_contents`
    parameter. Could you please provide the values or data that you want to use for `gc_contents` in the
    `perform_lowess` function?
    :param coverages: It seems like you were about to provide some information about the `coverages`
    parameter. Could you please provide the values or data that you want to use for the `coverages`
    parameter in the `perform_lowess` function?
    :return: The function `perform_lowess` returns the weighted coverage calculated using LOWESS
    regression on the provided GC contents and coverages.
    """
    gc_contents = np.array(gc_contents)
    coverages = np.array(coverages)
    sorted_indices = np.argsort(gc_contents)
    sorted_gc_contents = gc_contents[sorted_indices]
    sorted_coverages = coverages[sorted_indices]
    smoothed_coverages = lowess(
        sorted_coverages, sorted_gc_contents, frac=frac, return_sorted=False
    )
    if len(smoothed_coverages) > 0:
        weighted_coverage = np.nanmean(smoothed_coverages)
    else:
        weighted_coverage = 0

    return weighted_coverage
