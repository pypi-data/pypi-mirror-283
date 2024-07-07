import numpy as np
import scanpy as sc
import torch
from tqdm import tqdm

import pandas as pd
from .classify import CellTypeClassifier, filter_cell_type
from functools import partial

from sklearn.neighbors import KDTree
from scipy.stats import chi2_contingency


class scPCAReducer:
    def __init__(self, adata, mean=None) -> None:
        self.A = np.array(adata.varm['PCs'])
        if mean == None:
            self.mean_ = adata.X.mean(axis=0)
        else:
            self.mean_ = mean

    def transform(self, X):
        X = np.array(X)
        X_center = X - self.mean_
        return (X_center @ self.A).astype('float32')
    
    def inverse_transform(self, X):
        return np.dot(X, np.transpose(self.A)) + self.mean_
    



def chi2_statistic_test(x, x_m):
    x, x_m = np.array(x), np.array(x_m)
    a, b = [], []

    for cell_type in pd.unique(np.concatenate([x, x_m])):
        a.append(sum(x==cell_type))
        b.append(sum(x_m==cell_type))
    obs = np.array([a, b])
    res = chi2_contingency(obs)
    return res.statistic, res.pvalue

class Simulator:
    def __init__(self, model, mode='ode', sigma=0.25) -> None:
        self.mode = mode
        if self.mode == 'ode':
            try:
                from torchdyn.core import NeuralODE
                from torchcfm.utils import torch_wrapper
        
            except ImportError:
                raise ImportError(
                    "Please install the torchdyn, torchcfm`.")
            
            self.smltr = NeuralODE(torch_wrapper(model), solver="dopri5", sensitivity="adjoint")
        elif self.mode == 'sde':
            try:
                import torchsde
                from torchcfm.utils import SDE
        
            except ImportError:
                raise ImportError(
                    "Please install the torchsde, torchcfm`.")
            self.smltr = SDE(model[0], model[1], noise=sigma)
        
    
    def simulate(self, x : torch.Tensor, t_start:float, t_end:float, n:int) -> np.array:
        
        with torch.no_grad():
            if self.mode == 'ode' :
                traj = self.smltr.trajectory(
                    x.float(),
                    t_span=torch.linspace(t_start, t_end, n),
                ).cpu().detach().numpy()

            elif self.mode == 'sde':
                traj = torchsde.sdeint(
                    self.smltr,
                    x.float(),
                    ts=torch.linspace(t_start, t_end, n),
                ).cpu().detach().numpy()
        return traj
    

class FateManipulator:

    def __init__(self, adata : sc.AnnData,
                 cell_type_key: str, 
                 time_key: str, 
                 embedding_key: str, 
                 simulator: Simulator,
                 embedder) -> None:
        self.adata = adata
        self.cell_type_key = cell_type_key
        self.time_series = np.sort(np.unique(adata.obs[time_key]))
        self.time_key = time_key
        self.embedding_key = embedding_key
        self.simulator = simulator
        self.tree = KDTree(adata.obsm[embedding_key])
        
        self.clf = CellTypeClassifier(adata, time_key, embedding_key, cell_type_key)
        self.clf.fit()
        self.embedder = embedder
    
    def compute_cell_fate(self, cell_idx, batch_size=2048):
        adata = self.adata[cell_idx]
        fate = []
        final_type = []
        
        for t in range(len(self.time_series)):
            
            cell_idx_t = adata.obs.loc[adata.obs[self.time_key] == self.time_series[t]].index
            if len(cell_idx_t) == 0:
                continue
            simulate_t = len(self.time_series) - t - 1
            print('calcu day: {} , travel time: {}'.format(self.time_series[t], simulate_t))
            for i in tqdm(range(len(cell_idx_t) // batch_size + 1)):
                
                cell_idx = cell_idx_t[i * batch_size: (i + 1) * batch_size]
                
                traj = self.pred_for_specific_cell(cell_idx, simulate_t)
                pred_state = traj[-1,:,:]
                
                pred_cell_type = pd.DataFrame(self.clf.predict(pred_state), index=cell_idx, columns=['simulated_cell_type'])
                
                pred_cell_type_proba = self.clf.predict_proba(pred_state)
                pred_cell_type_proba.index = cell_idx
                
                fate.append(pred_cell_type_proba)
                final_type.append(pred_cell_type)
                
        fate = pd.concat(fate)
        final_type = pd.concat(final_type)
        adata.obsm['cell_fate'] = fate.loc[adata.obs.index]
        adata.obs['simulated_cell_type'] = final_type.loc[adata.obs.index]['simulated_cell_type']
        return adata
        
    def check_t_start(self, cell_idx):
        t_start = np.unique(self.adata[cell_idx].obs[self.time_key])
        try:
            assert len(t_start) == 1
        except:
            print('Different start time in proven cells ! Start time need to be the same.')
            raise ValueError
        return t_start[0]
        
    def pred(self, xt : torch.Tensor, t_start : float, t_end : float,  query_num=50, point_num=200):
        trajs = []
        r = np.linspace(t_start, t_end, query_num+1)
        n = point_num // query_num
        for i in range(r.shape[0] - 1):
            
            traj = self.simulator.simulate(xt, r[i], r[i + 1], n)
            xt = torch.Tensor(self.adata.obsm[self.embedding_key][self.tree.query(traj[-1], k=1)[1]])[:,0,:]
            trajs.append(traj)
        return np.concatenate(trajs)
    




    def pred_for_specific_cell(self, cell_idx : pd.Index, t=None ):
        t_start = self.check_t_start(cell_idx)
        if t == None:
            t = len(self.time_series) - np.where(self.time_series == t_start)[0][0] - 1
        x = torch.Tensor(self.adata[cell_idx].obsm[self.embedding_key])

        return self.pred(x, t_start, t_start + t)

    def manipulate_gene(self, gene_idx : pd.Index, cell_idx : pd.Index, target_level : list):
        origin_input = self.adata[cell_idx].X.toarray()
        for g in range(len(gene_idx)):
            origin_input[:,np.where(self.adata.var.index == gene_idx[g])[0]] = target_level[g]
        low_input = self.embedder.transform(origin_input)
        return low_input

    def process_function(self, gene_level, para, method='KD'):
        

        if method == 'KD':
            #manipulated_level = [np.percentile(gene_level[:,i], para) for i in range(gene_level.shape[1])]
            manipulated_level = [np.mean(gene_level[:, i]) * para for i in range(gene_level.shape[1])]
        elif method == 'OE':
            manipulated_level = [np.mean(gene_level[:, i]) * para for i in range(gene_level.shape[1])]
        else:
            raise NotImplementedError
        
        return manipulated_level


    def _in_silico_process(self, gene_idx : pd.Index, cell_idx : pd.Index, t =None, 
                           method='KD', para=1, verbose=1):
        t_start = self.check_t_start(cell_idx)
    
        if t == None:
            t = len(self.time_series) - np.where(self.time_series == t_start)[0][0] - 1

        gene_level = self.adata[cell_idx, gene_idx].X.toarray()
        
        manipulated_level = self.process_function(gene_level=gene_level, method=method, para=para)
        if verbose > 0:
            print('In silico {} {} from level {} to {}, from time {} to {}'.format(method, 
                                                                     list(gene_idx),
                                                                     np.mean(gene_level, axis=0),
                                                                       manipulated_level,
                                                                       t_start, str(t_start)+'+'+str(t)))

        x = self.manipulate_gene(gene_idx, cell_idx, manipulated_level)
        manipulated_traj = self.pred(torch.Tensor(x), t)

        return manipulated_traj
    
    def in_silico_kd(self, gene_idx : pd.Index, cell_idx : pd.Index, kd2percent : float,  t=None, verbose=.1):
        
        return self._in_silico_process(gene_idx, cell_idx, t, 
                           method='KD', para=kd2percent, verbose=verbose)
    
    def in_silico_oe(self, gene_idx : pd.Index, cell_idx : pd.Index , oe2fold : float, t=None, verbose=1):
        
        return self._in_silico_process(gene_idx, cell_idx, t, 
                           method='OE', para=oe2fold, verbose=verbose)
    

    def _in_silico_perb_screen(self, cell_idx, candidate_gene_list = None, t=None, method='KD', para=.1, ):
        
        t_start = self.check_t_start(cell_idx)
    
        if t == None:
            t = len(self.time_series) - np.where(self.time_series == t_start)[0][0] - 1

        if candidate_gene_list == None:
            init_adata = self.adata[cell_idx]
            sc.pp.highly_variable_genes(init_adata)
            cutoff = np.quantile(init_adata.var.means.tolist(), q=0.75)
            candidate_gene_list = init_adata.var.loc[init_adata.var.means >= cutoff].index

        baseline_traj = self.pred_for_specific_cell(cell_idx, t=t)
        x =  self.clf.predict_uncertainty(baseline_traj[-1,:,:], specify=True)
        manipulate_func_wrapper = partial(self._in_silico_process, 
                                      cell_idx=cell_idx,
                                      t=t,
                                      method=method,
                                      para=para,
                                      verbose=0)
        screen_res = []
        pbar = tqdm(candidate_gene_list)
        for gene_idx in pbar:
            if isinstance(gene_idx, str):
                gene_idx = pd.Index([gene_idx])

            manipulated_traj = manipulate_func_wrapper(gene_idx)
            x_m = self.clf.predict_uncertainty(manipulated_traj[-1,:,:], specify=True)
            s, p = chi2_statistic_test(x, x_m)
            screen_res.append([s, p])
            pbar.set_description('In silico screen.. {}'.format(list(gene_idx)))
        
        screen_res = pd.DataFrame(screen_res, index=candidate_gene_list, columns=['statistic', 'pvalue'])
        screen_res = screen_res.sort_values('pvalue')
        return screen_res
    
    def in_silico_kd_screen(self, cell_idx, candidate_gene_list = None, t=None,  kd2percent=.1):
        return self._in_silico_perb_screen(cell_idx, candidate_gene_list, t, method='KD', para=kd2percent)
    
    def in_silico_oe_screen(self, cell_idx, candidate_gene_list = None, t=None,  oe2fold=2):
        return self._in_silico_perb_screen(cell_idx, candidate_gene_list, t, method='OE', para=oe2fold)
    
    def in_silico_screen_from_time(self, t_start, kd_rate=.1, oe_rate=2.):
        print('Start Screening Cell at Time {}'.format(self.time_series[t_start]))
        print('It may takes a while..')
        init_adata = self.adata[self.adata.obs[self.time_key] == self.time_series[t_start]]
        init_adata_cell_group = {}
        for cell_type in pd.unique(init_adata.obs[self.cell_type_key]):
            print('Screening for Cell Type {} ...'.format(cell_type))
            init_adata_cell = init_adata[init_adata.obs[self.cell_type_key] == cell_type]
            init_adata_cell = self.compute_cell_fate(init_adata_cell.obs.index)
            init_adata_cell = filter_cell_type(init_adata_cell, 'simulated_cell_type')
            cell_idx = init_adata_cell.obs.index
            kd_res = self.in_silico_kd_screen(cell_idx, kd2percent=kd_rate)
            oe_res = self.in_silico_oe_screen(cell_idx, kd2percent=oe_rate)
            init_adata_cell_group[cell_type] = {
                                        'cell_idx':cell_idx,
                                        'kd_res':kd_res,
                                        'oe_res':oe_res
                                        }
                            
        return init_adata_cell_group


