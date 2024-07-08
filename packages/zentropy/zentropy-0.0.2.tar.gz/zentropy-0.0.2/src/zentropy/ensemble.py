import zentropy.utils as _utils
import zentropy.transforms as _transforms
import numpy as _np
import pandas as _pd
from zentropy.lib import fisher_yates_knn_permutation as _fisher_yates_knn_permutation

def generate_jitter(data,vars,scales=0,sampler=None,size=1000,jitter_index=None):
    data, _, _ = _utils.check_dataframe(data)
    data_as_numpy = data.to_numpy()[None,...].repeat(size,0)
    if sampler is None:
        rng = _np.random.default_rng()
        perturbations = rng.random(data_as_numpy[...,data.columns.get_indexer(vars)].shape)*2-1
    else:
        perturbations = sampler(data_as_numpy[...,data.columns.get_indexer(vars)].shape)
    data_as_numpy[...,data.columns.get_indexer(vars)] += perturbations*_np.array(scales)[None,None,:]
    data_as_df = _pd.concat([_pd.DataFrame(
        a,
        columns=data.columns,
        index=_pd.MultiIndex.from_product(
            [data.index,(i,)],
            names=[
                "index" if data.index.name is None else data.index.name,
                "jitter" if jitter_index is None else jitter_index
            ]
        )
    ) for i,a in enumerate(data_as_numpy)])
    return data_as_df.convert_dtypes()


def generate_permutations(data,*vars,discrete_vars=[],cvars=[],k=50,size=1000,conditional_method=_fisher_yates_knn_permutation,permutation_index=None):
    data, df_discrete_vars, df_cont_vars = _utils.check_dataframe(data)
    data_as_numpy = data.to_numpy()[None,...].repeat(size,0)
    if cvars:
        if not(vars):
            vars = data.columns
        else:
            vars = list(vars)

        if discrete_vars is None:
            discrete_cvars = [c for c in cvars if (c in df_discrete_vars)]
            cont_cvars = [c for c in cvars if (c in df_cont_vars)]
        else:
            discrete_cvars = [c for c in cvars if (c in discrete_vars)]
            cont_cvars = [c for c in cvars if not(c in discrete_vars)]
            
        if discrete_cvars:
            groupings = data.groupby(discrete_cvars)
            indices = groupings.apply(lambda df:df.index)
            permutations_groups = groupings.apply(
                lambda df: generate_permutations(df,*vars,cvars=cont_cvars,discrete_vars=discrete_vars,k=min(k,df.shape[0]),size=size,conditional_method=conditional_method)
            )
            for g in permutations_groups.index:
                data_as_numpy[:,indices[g]] = permutations_groups[g]
            return data_as_numpy
        else:
            neighbors_lists = _transforms.get_neighbors(data_as_numpy[0][:,data.columns.get_indexer(cvars)],k=k)
            neighbors = _np.array([[e for e in a] for a in neighbors_lists],dtype="int32")

            rng = _np.random.default_rng()
            inds_to_permute = _np.arange(data.shape[0])[None,...].repeat(size*len(vars),axis=0)
            shuffled_inds = rng.permuted(inds_to_permute,axis=1)
            new_locs = _np.argsort(shuffled_inds,axis=1)
            shuffled_neighbors = neighbors[shuffled_inds] # has shape (size*len(vars),data.shape[0],k)
            reindexed_shuffled_neighbors = new_locs[ 
                _np.arange(size*len(vars))[:,None,None],
                shuffled_neighbors
            ]
            # RSN[I,J,K] = NR[I,SN[I,J,K]]
            randomized_neighbors = rng.permuted(reindexed_shuffled_neighbors,axis=2)

            shuffled_conditional_permutations = conditional_method(randomized_neighbors.astype("int32"))
            conditional_permutations = _np.empty_like(shuffled_conditional_permutations)
            conditional_permutations[
                _np.arange(size*len(vars))[:,None],
                shuffled_inds,
            ] = shuffled_inds[ 
                _np.arange(size*len(vars))[:,None],
                shuffled_conditional_permutations
            ]

            for j,v in enumerate(vars):
                data_as_numpy[:,:,data.columns.get_loc(v)] = data_as_numpy[0,:,data.columns.get_loc(v)][
                    conditional_permutations.reshape((size,len(vars),data.shape[0]))[:,j,:]
                ]
    else:
        if not(vars):
            vars = data.columns
        else:
            vars = list(vars)
        data_as_numpy = data.to_numpy()[None,:,:].repeat(size,0)
        data_to_permute = data[vars].to_numpy()[None,:,:].repeat(size,0)
        rng = _np.random.default_rng()
        permuted_data = rng.permuted(data_to_permute,axis=1)
        data_as_numpy[:,:,data.columns.get_indexer(vars)] = permuted_data

    data_as_df = _pd.concat([_pd.DataFrame(
        a,
        columns=data.columns,
        index=_pd.MultiIndex.from_product(
            [data.index,(i,)],
            names=[
                "index" if data.index.name is None else data.index.name,
                "permutation" if permutation_index is None else permutation_index
            ]
        )
    ) for i,a in enumerate(data_as_numpy)])

    return data_as_df.convert_dtypes()

def generate_jackknife(data,size=None,jackknife_index=None):
    data, _, _ = _utils.check_dataframe(data)
    if size is None:
        remove_inds = data.index
    else:
        rng = _np.random.default_rng()
        remove_inds = rng.choice(data.index,size=size,replace=False)
    return _pd.concat([_pd.DataFrame(
        (df := data.drop(i)).to_numpy(),
        columns = data.columns,
        index = _pd.MultiIndex.from_product(
            [df.index,(i,)],
            names=[
                "index" if data.index.name is None else data.index.name,
                "removed" if jackknife_index is None else jackknife_index
            ]
        )
    ) for i in remove_inds]).convert_dtypes()