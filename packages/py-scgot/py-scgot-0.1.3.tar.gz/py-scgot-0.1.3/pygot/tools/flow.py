import torch
def latent_velocity(adata, odefunc, embedding_key='X_pca', time_vary=True, time_key=None):
    
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

def velocity(adata, odefunc, embedding_key='X_pca',  A=None, time_vary=True, time_key=None,
             dr_mode='linear', inverse_transform=None, dt=.001):
    if embedding_key == 'X_pca' and dr_mode == 'linear':
        A = adata.varm['PCs'].T
    v_latent = latent_velocity(adata, odefunc, embedding_key, time_vary, time_key)
    adata.obsm['velocity_'+embedding_key.split('_')[-1]] = v_latent
    if dr_mode == 'linear':
        adata.layers['velocity'] = v_latent @ A
    elif dr_mode == 'nonlinear' and inverse_transform is not None:
        x0 = inverse_transform(adata.obsm[embedding_key])
        x1 = inverse_transform(adata.obsm[embedding_key] + v_latent * dt)
        adata.layers['velocity'] = (x1 - x0) / dt
    
    

   