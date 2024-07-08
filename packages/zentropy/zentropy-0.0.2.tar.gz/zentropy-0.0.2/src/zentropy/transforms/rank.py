import numpy as _np 
from zentropy.utils import rotate_array as _rotate_array, unrotate_array as _unrotate_array

def rank(xs,axis=-1):
    if axis < 0:
        axis = xs.ndim + axis
    xs_rot = _rotate_array(xs,axis)
    inds = _np.argsort(xs_rot,axis=-1)
    x_ranks = _np.empty_like(xs_rot)
    _np.put_along_axis(x_ranks,inds,_np.arange(xs_rot.shape[-1]),-1)
    return _unrotate_array(x_ranks,axis)