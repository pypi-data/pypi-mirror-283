import numpy as _np
import zentropy.transforms as _transforms
import zentropy.utils as _utils
import zentropy.estimators.continuous as _continuous
import zentropy.estimators.discrete as _discrete



def entropy(data,discrete_vars=[],cvars=[],base=2,k=3,r=None,discrete_method="schurmann"):
    data, df_discrete_vars, df_cont_vars = _utils.check_dataframe(data)
    if cvars:
        return mutual_information(data,data.columns,discrete_vars=discrete_vars,cvars=cvars,base=base,k=k,r=r)
    
    if not(discrete_vars):
        discrete_vars = [c for c in data.columns if (c in df_discrete_vars)]
        cont_vars = [c for c in data.columns if (c in df_cont_vars)]
    else:
        discrete_vars = [c for c in data.columns if (c in discrete_vars)]
        cont_vars = [c for c in data.columns if not(c in discrete_vars)]
    if discrete_vars and cont_vars:
        groupings = data.groupby(discrete_vars)
        surprisals = groupings.apply(
            lambda df: _continuous.entropy_from_points(
                df[cont_vars],
                k=k,
                r=(r[data.index.get_indexer(df.index)] if hasattr(r,"__len__") else r),
                base=base
            )
        ).to_numpy()
        counts = data.value_counts(discrete_vars).to_numpy()
        return _discrete.entropy_from_counts(counts,base=base,method=discrete_method) + (surprisals*counts).sum()/counts.sum()
    elif discrete_vars:
        return _discrete.entropy_from_counts(data.value_counts(discrete_vars),method=discrete_method,base=base)
    else:
        return _continuous.entropy_from_points(data,k=k,r=r,base=base)

def information_profile(data,*atoms,discrete_vars=[],batch_index=None,base=2,k=3,r=None,discrete_method="schurmann"):
    data, df_discrete_vars, df_cont_vars = _utils.check_dataframe(data)

    ...

def mutual_information(data,*mutual_vars,cvars=[],discrete_vars=[],batch_index=None,base=2,k=3,r=None,discrete_method="schurmann"):
    data, df_discrete_vars, df_cont_vars = _utils.check_dataframe(data)
    all_vars = list(mutual_vars)+cvars
    vars = list(set(_utils.reduce_to_list(all_vars)))
    if batch_index:
        return data.groupby(level=batch_index)[vars].apply(
            lambda df:mutual_information(
                df,
                *mutual_vars,
                cvars=cvars,
                discrete_vars=discrete_vars,
                base=base,k=k,r=r,
                discrete_method=discrete_method
        ))
    if not(discrete_vars):
        discrete_vars = [c for c in vars if (c in df_discrete_vars)]
        cont_vars = [c for c in vars if (c in df_cont_vars)]
    else:
        discrete_vars = [c for c in vars if (c in discrete_vars)]
        cont_vars = [c for c in vars if not(c in discrete_vars)]

    if cont_vars:
        if discrete_vars and r is None:
            groupings = data.groupby(discrete_vars)
            indices = groupings.apply(lambda df:df.index)
            r_groups = groupings.apply(
                lambda df: _transforms.get_knn_distance(df[cont_vars],k=k,)
            )
            r = _np.zeros([data.shape[0]])
            for g in r_groups.index:
                r[data.index.get_indexer(indices[g])] = r_groups[g]
        elif r is None:
            r = _transforms.get_knn_distance(data[cont_vars],k=k,)
    n_vars = len(all_vars)
    combo_index = _utils.combination_index(mutual_vars,all_vars)
    coefficients = _utils.entropy_to_atoms_matrix(n_vars)[combo_index]
    pos_coefficients = (coefficients != 0)
    entropy_vars = [list(_np.array(all_vars,dtype=object)[a]) for a in _utils.atoms_to_variables_matrix(n_vars)[pos_coefficients].astype(bool)]
    entropies = _np.array([entropy(data[_utils.reduce_to_list(varlist)],base=base,discrete_vars=discrete_vars,discrete_method=discrete_method,r=r) for varlist in entropy_vars])
    return entropies.dot(coefficients[pos_coefficients])

def total_correlation(data,*mutual_vars,cvars=[],discrete_vars=[],base=2,k=3,r=None):
    total_ent =  mutual_information(data,mutual_vars,cvars=cvars,discrete_vars=discrete_vars,base=base,k=k,r=r)
    marginal_ents = [mutual_information(data,mvar,cvars=cvars,discrete_vars=discrete_vars,base=base,k=k,r=r) for mvar in mutual_vars]
    return sum(marginal_ents) - total_ent