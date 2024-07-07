import torch
from functools import partial


from .v_centric_training import v_centric_training, GraphicalOTVelocitySampler
from .x_centric_training import x_centric_training
from .jacobian import _get_minibatch_jacobian


class ODEwrapper(torch.nn.Module):
    def __init__(self, func):
        super(ODEwrapper, self).__init__()
        self.func = func


    def forward(self, t, x): #NOTE the forward pass when we use torchdiffeq must be forward(self,t,x)
        if self.func.time_varying:
            if len(t.size()) == 0:
                time = t.repeat(x.size()[0],1)
            else:
                time = t
        
            dxdt = self.func(torch.concat([x, time], dim=-1).float())
        else:
            dxdt = self.func(x)
        return dxdt
    
    
    def compute_G(self, t, x):
        if self.func.time_varying:
            if len(t.size()) == 0:
                time = t.repeat(x.size()[0],1)
            else:
                time = t
            G = self.func.compute_G(torch.concat([x, time], dim=-1).float())
        else:
            G = self.func.compute_G(x).float()
        return G

class ODEwrapperNoTime(torch.nn.Module):
    def __init__(self, func):
        super(ODEwrapperNoTime, self).__init__()
        self.func = func


    def forward(self, t, x): #NOTE the forward pass when we use torchdiffeq must be forward(self,t,x)
        dxdt = self.func(x)
        return dxdt
    
def hill_func(jacobian, x):
    # 将 alpha、a 和 b 扩展为与 x 具有相同的维度
    a = torch.ones_like(jacobian)
    b = torch.zeros_like(jacobian)
    a[jacobian > 0] = 0
    b[jacobian > 0] = 1
    alpha_expanded = torch.unsqueeze(jacobian, dim=-2)  # 在倒数第二个维度扩展
    a_expanded = torch.unsqueeze(a, dim=-2)
    b_expanded = torch.unsqueeze(b, dim=-2)

    # 计算 alpha * x
    alphax = alpha_expanded * x

    # 计算 Hill 函数的值
    result = (a_expanded * 1 + b_expanded * alphax) / (1 + alphax)
    
    # 转置结果以匹配所需的形状
    result = torch.transpose(result, dim0=1, dim1=0)
    
    return result


class GOT(torch.nn.Module):
    def __init__(self, dim, time_varying=False):
        super().__init__()
        self.time_varying = time_varying
        self.net = torch.nn.Sequential(
            torch.nn.Linear(dim + (1 if time_varying else 0), 16, bias=False),
            torch.nn.CELU(),
            torch.nn.Linear(16, 32, bias=False),
            torch.nn.CELU(),
            torch.nn.Linear(32, 16, bias=False),
            torch.nn.CELU(),
            torch.nn.Linear(16, dim, bias=False),
            #JAC(out_dim)
        )
        self.global_G = torch.nn.Parameter(torch.rand(dim, dim))
        self.beta = torch.nn.Parameter(torch.ones(dim))
        self.relu = torch.nn.ReLU()

    def compute_G(self, x):
        x.requires_grad = True
        v = self.net(x)
        if self.time_varying:
            G0 = _get_minibatch_jacobian(v, x, return_np=False)[:,:,:-1]
        else:
            G0 = _get_minibatch_jacobian(v, x, return_np=False)
        return G0 

    def forward(self, x):
        return self.net(x) 
    






def train_model(
        adata, time_key, embedding_key, device,
        graph_key=None,
        dim=None,
        n_neighbors=50,
        v_centered_iter_n=1000, dt=0.01, 
        sigma=0.1, add_noise=True,
        neighbor_sampling = False,
        v_centered_batch_size=256, lr=5e-3, #1e-4
        all_in=False,
        path='',
        linear=False,
        distance_matrices='L2',
        pretrained_model=None,
        x_centered=True,
        x_centered_iter_n=2000,
        x_centered_batch_size=256,
        reverse_schema=True,
        graph_inter=False,
        randomized=False,
        TF_loss=None, TF_idx=None,
        time_varying=True,
        ):
    
    if dim == None:
        dim = adata.obsm[embedding_key].shape[1]
    adata.obsm[embedding_key] = adata.obsm[embedding_key][:,:dim]
    sp_sampler = GraphicalOTVelocitySampler(
                    adata, time_key, 
                    graph_key=embedding_key if graph_key==None else graph_key, 
                    embedding_key=embedding_key, 
                    device=device, 
                    path=path, 
                    linear=linear,
                    neighbor_sampling=neighbor_sampling,
                    n_neighbors=n_neighbors)
    
    sp_sampler.compute_shortest_path(n_neighbors=n_neighbors)
    
    
    if pretrained_model == None:
        model = ODEwrapper(GOT(dim=dim, time_varying=time_varying)).to(device)
        #MLP(dim=dim,time_varying=True, w=w_dim).to(device)
    else:
        model = pretrained_model

    optimizer = torch.optim.Adam(model.parameters(), lr, weight_decay=0.001)
    sample_fn_path = partial(sp_sampler.filtered_sample_batch_path, all_in=all_in, sigma=sigma, dt=dt, batch_size=v_centered_batch_size, distance_matrices=distance_matrices, add_noise=add_noise)
    model, history = v_centric_training(model, optimizer, sample_fn_path, iter_n=v_centered_iter_n)

    if x_centered:

        model, history2 = x_centric_training(adata, time_key, embedding_key, model, 
                                             reverse_schema=reverse_schema,
                                             batch_size=x_centered_batch_size, 
                                             iter_n=x_centered_iter_n, 
                                            graph_inter=graph_inter, 
                                            sp_sampler=sp_sampler, 
                                            distance_matrices=distance_matrices, 
                                            randomized=randomized,
                                            TF_loss=TF_loss, TF_idx=TF_idx,
                                            neighbor_sampling=neighbor_sampling)
        return model, (history, history2)

    return model, history








