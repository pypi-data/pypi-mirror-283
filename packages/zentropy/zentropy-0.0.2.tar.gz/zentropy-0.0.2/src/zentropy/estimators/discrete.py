from scipy.special import digamma as _digamma, betainc as _betainc, beta as _beta
import numpy as _np
import zentropy.utils as _utils

def grassberger_function(xs):
    return _digamma(xs) + 0.5*(-1)**(xs % 2)*(_digamma((xs+1)/2)-_digamma(xs/2))

def schurmann_entropy(counts,base=2,p_estimate=0,eps=1e-8,axis=-1):
    counts = _utils.rotate_array(counts,axis=axis)

    N = counts.sum(axis=-1)
    n_psi_ns = _np.empty_like(counts)
    n_psi_ns[counts==0] = 0
    n_psi_ns[counts>0] = counts[counts>0]*_digamma(counts[counts>0])
    bias_correction = _betainc(N,eps,p_estimate)*_beta(N,eps)
    return (counts*(_digamma(N) + bias_correction) - n_psi_ns).sum(axis=-1)/(N*_np.log(base))

def mle_entropy(counts,base=2,axis=-1):
    counts = _utils.rotate_array(counts,axis=axis)

    N = counts.sum(axis=-1)
    n_log_ns = _np.empty_like(counts)
    n_log_ns[counts==0] = 0
    n_log_ns[counts>0] = counts[counts>0]*_np.log(counts[counts>0])
    return (counts*_np.log(N) - n_log_ns).sum(axis=-1)/(N*_np.log(base))

def miller_entropy(counts,base=2,axis=-1):
    counts = _utils.rotate_array(counts,axis=axis)

    N = counts.sum(axis=-1)
    return mle_entropy(counts,axis=-1,base=base) + (counts.shape[-1]-1)/(N*_np.log(base))

def grassberger_entropy(counts,base=2,axis=-1):
    counts = _utils.rotate_array(counts,axis=axis)

    N = counts.sum(axis=-1)
    n_G_ns = _np.empty_like(counts)
    n_G_ns[counts==0] = 0
    n_G_ns[counts>0] = counts[counts>0]*grassberger_function(counts[counts>0])
    return (counts*_np.log(N) - n_G_ns).sum(axis=-1)/(N*_np.log(base))

def entropy_from_counts(counts,method="schurmann",**method_kwargs):
    if method == "schurmann":
        return schurmann_entropy(counts,**method_kwargs)
    elif method == "grassberger":
        return grassberger_entropy(counts,**method_kwargs)
    elif method == "jackknife":
        return jackknife_counts(counts,mle_entropy,**method_kwargs)
    elif method == "mle":
        return mle_entropy(counts,**method_kwargs)
    elif method == "miller":
        return miller_entropy(counts,**method_kwargs)
    elif method is callable:
        return method(counts,**method_kwargs)

def jackknife_counts(counts,estimator,axis=-1,**estimator_kwargs):
    counts = _np.array(counts)
    n = counts.shape[axis]
    jackknife_counts = counts[None,...].repeat(n,axis=0)
    jackknife_estimates =  estimator(jackknife_counts,axis=axis if axis<0 else axis+1,**estimator_kwargs)
    full_estimate =  estimator(counts,axis=axis,**estimator_kwargs)
    return n*full_estimate - (n-1)*jackknife_estimates.mean(axis=0)