from scipy.special import digamma as _digamma
import numpy as _np
import zentropy.transforms as _transforms

def surprisal_from_points(xs,ys=None,k=3,r=None,base=2,):
    if r is None:
        r = _transforms.get_knn_distance(xs,k,)
    elif hasattr(r,"__len__"):
        if len(r)!=xs.shape[0]:
            raise ValueError("Number of radii must be equal to number of samples if radius is not constant")
    else:
        r = _np.array([r]*xs.shape[0])

    if _np.any(r==0):
        raise ValueError("Distance to k-nearest neighbor is zero. Check the variable is not discrete.")

    n_neighbors = _transforms.count_proper_neighbors(xs,r,ys=ys,)
    return (_digamma(xs.shape[0]) - _digamma(n_neighbors+1) + xs.shape[1]*_np.log(r))/_np.log(base)

def entropy_from_points(xs,ys=None,k=3,r=None,base=2,):
    surprisals = surprisal_from_points(xs,ys=ys,k=k,r=r,base=base)
    return surprisals.mean()
        