
from functools import partial
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import scanpy as sc
import pandas as pd
import numpy as np
from pygot.tools.manipulate import chi2_statistic_test, FateManipulator


def plot_traj(adata, color_key, traj, umaper=None, traj_line=False):
    
    
    start, end = traj[0,:,:], traj[-1,:,:]
    f, ax2 = plt.subplots(1, 1, figsize=(12, 8))
    if traj.shape[-1] != 2:
        start, end = umaper.transform(start), umaper.transform(end)
        if traj_line:
            traj = umaper.transform(traj.reshape(-1, traj.shape[-1]))
            traj = traj.reshape(-1, traj.shape[1],  2)
            
    for i in range(traj.shape[1]):
        ax2.scatter(
        start[:, 0], start[:, 1], s=10, alpha=1, marker="d", c="brown", zorder=3
    )
        ax2.scatter(
        end[:, 0], end[:, 1], s=10, alpha=1, marker="d", c="blue", zorder=3
    )
        if traj_line:
            ax2.plot(traj[:, i, 0], traj[:,i, 1], alpha=0.2, c="black", zorder=2)
    
    sc.pl.umap(adata, color=color_key, ax=ax2, show=False)

    plt.show()



def plot_sankey(obs:pd.DataFrame, flow_cell_type:list, target_key :list, name:str, cutoff=10):
    
    v_l, s_l, t_l = [], [], []
    
    def get_flow(single_source, single_target, label_source, label_target):

        values = []
        s = []
        t = []
        for i, source in enumerate(label_source):
        
            subset = obs.loc[obs[single_source] == source]
            for j, target in enumerate(label_target):
                num = len(subset.loc[subset[single_target] == target])
                if num > cutoff:
                    values.append(num)
                    s.append(i)
                    t.append(j)
        return np.array(values), np.array(s), np.array(t)
    start = 0
    for i in range(len(target_key) - 1):
        #all_label_list.append(cell_type_list)
        v, s, t = get_flow(target_key[i], target_key[i+1], flow_cell_type[i], flow_cell_type[i+1])
        s += start
        t += (start + len(flow_cell_type[i]))
        start += len(flow_cell_type[i])
        v_l.append(v)
        s_l.append(s)
        t_l.append(t)
    all_label_list = []
    for cell_type_list in flow_cell_type:
        all_label_list.extend(cell_type_list)
    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = all_label_list,
      
    ),
    link = dict(
      source = np.concatenate(s_l), # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = np.concatenate(t_l),
      value = np.concatenate(v_l)
    )), ])
    
    fig.update_layout(title_text=name, font_size=10)
    #fig.write_image("figures/"+name+'.png')
    fig.show()

def plot_sankey_traj(cell_idx, traj, manipulator:FateManipulator, name, stage_num=7, mode='certainty', specify=False, cutoff=10):
    stage_num -= 1
    obs = manipulator.adata[cell_idx].obs.copy()
    target_key = [ manipulator.cell_type_key ]

    flow_cell_type = [np.sort(
                            np.unique(
                            manipulator.adata[cell_idx].obs[manipulator.cell_type_key]))]
    if mode == 'certainty':
        pred_func = manipulator.clf.predict
    elif mode == 'uncertainty':
        pred_func = partial(manipulator.clf.predict_uncertainty, specify=specify)
        
    else:
        raise NotImplementedError
    
    for i in range(stage_num + 1):
        now = np.min([i * int(traj.shape[0] / stage_num), traj.shape[0]-1])
        pred_cell_type = pred_func(traj[now,:,:])       
        #pred_cell_type = [c+'_stage_' + str(i) for c in pred_cell_type]
        
        obs['stage_' + str(i)] = pred_cell_type
        flow_cell_type.append(np.sort(np.unique(pred_cell_type)))
        target_key.append('stage_' + str(i))
    #flow_cell_type = cell_type_list
    plot_sankey(obs, 
                flow_cell_type=flow_cell_type,
                target_key=target_key,
                name = name,
                cutoff=cutoff)
    


def plot_statistic_sankey(baseline_traj, manipulated_traj, manipulator:FateManipulator, name:str, mode='certainty',specify=True, cutoff=10):
    
    if mode == 'certainty':
        pred_func = manipulator.clf.predict
    elif mode == 'uncertainty':
        pred_func = partial(manipulator.clf.predict_uncertainty, specify=specify)
        
    else:
        raise NotImplementedError
    x, x_m = pred_func(baseline_traj[-1,:,:]), pred_func(manipulated_traj[-1,:,:])
    obs = pd.DataFrame(
        np.array([ [c+'_baseline' for c in x],
                    [c+'_manipulated' for c in x_m] 
                ]).T, columns=['baseline_fate', 'manipulated_fate']
        )
    cell_type_list=np.sort(
                            np.unique(
                            obs.to_numpy())).tolist()
    flow_cell_type = [cell_type_list, cell_type_list]
    stat, pvalue = chi2_statistic_test(x, x_m)
    plot_sankey(obs, 
                flow_cell_type=flow_cell_type,
                target_key=obs.columns,
                name = name+' (chi2 stat:{:.4f} pvalue{:.4f} )'.format(stat, pvalue),
                cutoff=cutoff)