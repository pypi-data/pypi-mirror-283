
import matplotlib.pyplot as plt
import scvelo as scv
from pygot.tools.markov import velocity_graph

def potential_embedding(adata,  basis='X_umap', cell_type_key=None, ax=None, ):
    if ax is None:
        fig, ax = plt.subplots(1,1, dpi=300)
    
    scv.pl.velocity_embedding_stream(adata, basis=basis.split('_')[-1], ax=ax, show=False,  title='GOT Potential', color=cell_type_key,  fontsize=15)
    xt = adata.obsm[basis]
    s = ax.scatter(xt[:,0], xt[:,1], s=2, c=adata.obs['ent'], cmap='Reds')
    plt.title('GOT Potential')
    plt.colorbar(
                s, ax=ax, pad=0.01, fraction=0.08, aspect=30, label='differentiation potential'
            )



def velocity_embedding_grid(adata, velocity_key='velocity_pca', embedding_key='X_pca', basis='X_umap', k=30,  norm=False, update=True, **kwargs):
    if (not 'velocity_' + basis.split('_')[-1] in adata.obsm.keys()) or update:
        #project_velocity(adata, velocity_key=velocity_key, embedding_key=embedding_key, basis=basis, k=k, norm=norm)
        velocity_graph(adata, embedding_key, velocity_key, basis=embedding_key, k=k)
        if 'velocity_' + basis.split('_')[-1] in adata.obsm.keys():
            del adata.obsm['velocity_' + basis.split('_')[-1]]
    scv.pl.velocity_embedding_grid(adata, basis=basis.split('_')[-1], **kwargs)

def velocity_embedding(adata, velocity_key='velocity_pca', embedding_key='X_pca', basis='X_umap', k=30,  norm=False, update=True, **kwargs):
    if (not 'velocity_' + basis.split('_')[-1] in adata.obsm.keys()) or update:
        #project_velocity(adata, velocity_key=velocity_key, embedding_key=embedding_key, basis=basis, k=k, norm=norm)
        velocity_graph(adata, embedding_key, velocity_key, basis=embedding_key, k=k)
        if 'velocity_' + basis.split('_')[-1] in adata.obsm.keys():
            del adata.obsm['velocity_' + basis.split('_')[-1]]
    scv.pl.velocity_embedding(adata, basis=basis.split('_')[-1], **kwargs)

def velocity_embedding_stream(adata, velocity_key='velocity_pca', embedding_key='X_pca', basis='X_umap', k=30,  norm=False, update=True, **kwargs):
    if (not 'velocity_' + basis.split('_')[-1] in adata.obsm.keys()) or update:
        #project_velocity(adata, velocity_key=velocity_key, embedding_key=embedding_key, basis=basis, k=k, norm=norm)
        velocity_graph(adata, embedding_key, velocity_key, basis=embedding_key, k=k)
        if 'velocity_' + basis.split('_')[-1] in adata.obsm.keys():
            del adata.obsm['velocity_' + basis.split('_')[-1]]
    scv.pl.velocity_embedding_stream(adata, basis=basis.split('_')[-1], **kwargs)


'''
def get_velocity_embedding(adata, model = None, idx=None, embedding_key='X_pca', basis='X_umap', k=30, time_vary=True, time_key=None, norm=False, vt = None):
    if (vt is None) and (model is not None):
        vt = pred_velocity(adata, model, idx, embedding_key, time_vary=time_vary, time_key=time_key)
    elif vt is None:
        print('please offer model or vt')
        raise ValueError
    adata.obsm['velocity_' + embedding_key.split('_')[-1]] = vt.numpy()
    if embedding_key == basis:
        #adata.obsm['velocity_' + graph_key] = vt / torch.norm(vt, dim=-1)[:, None]
        adata.obsm['velocity_' + basis.split('_')[-1]] = vt
        return adata
    
    
    tree = KDTree(adata.obsm[embedding_key])
    dist, ind = tree.query(adata.obsm[embedding_key]+vt.numpy(), k=k)
    velocity = []
    for i in tqdm(range(adata.shape[0])):
        expectation = dist[i,:] / np.sum(dist[i,:])
        expectation = 1-expectation
        v = np.sum((adata.obsm[basis][ind[i,:],:] - adata.obsm[basis][i]) * (expectation[:, None]), axis=0)
        velocity.append(v)
    
    velocity = np.array(velocity)
    if norm:
        velocity /= np.linalg.norm(velocity, axis=-1)[:, None]    
    adata.obsm['velocity_' + basis.split('_')[-1]] = velocity
'''
