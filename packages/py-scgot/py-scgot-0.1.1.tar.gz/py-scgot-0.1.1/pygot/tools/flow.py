import torch
def pred_velocity(adata, odefunc, embedding_key='X_pca', time_vary=True, time_key=None):
    
    xt = torch.Tensor(adata.obsm[embedding_key])
    #TODO 如果时间统一了的话，这里需要修改
    if time_vary:
        #time_map = {i: t for t, i in enumerate(np.sort(np.unique(adata.obs[time_key])))}
        t = adata.obs[time_key]
        #t = torch.Tensor(np.array([time_map[x] for x in t]))[:, None]
        t = torch.Tensor(t)[:,None]
        #vt = model(xt, t).detach()
        
        vt = odefunc(torch.concat([xt, t], dim=-1)).detach().numpy()
    else:
        vt = odefunc(xt).detach().numpy()
    return vt

   