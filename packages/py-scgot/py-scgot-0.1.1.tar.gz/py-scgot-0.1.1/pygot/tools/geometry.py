import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from pygot.tools.jacobian import get_jacobian, _get_minibatch_jacobian

import numpy as np

class potentialMLP(torch.nn.Module):
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
            torch.nn.Linear(16, 1, bias=False),
            #JAC(out_dim)
        )
        

    def forward(self, x):
        x.requires_grad = True
        p = -self.net(x)
        v = _get_minibatch_jacobian(p, x, return_np=False)[:,0,:]
        
        return v 

    def potential(self, x):
        return self.net(x) 
    



# 定义自定义数据集类
class CustomDataset(Dataset):
    def __init__(self, x, y):
        self.x = torch.tensor(x, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


def calcu_jacobian(
        adata,
        embedding_key,
        time_key,
        odefunc,
        jacobian_key=None,
        copy=False
):
    data = adata.copy() if copy else adata
    if jacobian_key is None:
        jacobian_key = 'jacobian_'+embedding_key.split('_')[-1]
    data.obsm[jacobian_key] = get_jacobian(data, time_key, embedding_key, odefunc, time_vary=odefunc.time_varying).latent_jacobian
    return adata if copy else None


def calcu_divergence(
        adata,
        jacobian_key,
        div_key=None,
        copy=False
):
    if jacobian_key not in adata.obsm.keys():
        print('please call calcu_jacobian first')
        return
    data = adata.copy() if copy else adata
    div = []
    for i in tqdm(range(data.shape[0])):
        div.append(np.trace(data.obsm[jacobian_key][i]))
    if div_key == None:
        div_key = 'div_' + jacobian_key.split('_')[-1]
    data.obs[div_key] = np.array(div)
    return data if copy else None

def calcu_eigenvalue(
        adata,
        jacobian_key,
        eigen_key=None,
        copy=False
):
    if jacobian_key not in adata.obsm.keys():
        print('please call calcu_jacobian first')
        return
    
    data = adata.copy() if copy else adata
    eigenvals = []
    for i in tqdm(range(data.shape[0])):
        eigenval, eigenvec = np.linalg.eig(data.obsm[jacobian_key][i])
        eigenval = eigenval.real
        eigenval.sort()
        eigenvals.append(eigenval)
    if eigen_key == None:
        eigen_key = 'eigenval_' + jacobian_key.split('_')[-1]
    data.obsm[eigen_key] = np.array(eigenvals)

    return data if copy else None

def calcu_sink_source(
        adata,
        eigen_key,
        div_key,
        sink_cutoff=1e-3,
        source_cutoff=0.,
        div_percentile=75,
        copy=False
):
    data = adata.copy() if copy else adata
    sink, source = [], []
    for i in tqdm(range(data.shape[0])):
        eigenval = data.obsm[eigen_key][i]
        sink.append( (1. * sum(eigenval < sink_cutoff)) / eigenval.shape[0] )
        source.append( (1. * sum(eigenval > source_cutoff)) / eigenval.shape[0] )

    data.obs['sink'] = np.array(sink) * (data.obs[div_key] < np.percentile(data.obs[div_key], 100 - div_percentile) ).astype(float)
    data.obs['source'] = np.array(source) * (data.obs[div_key] > np.percentile(data.obs[div_key], div_percentile) ).astype(float)
    
    return data if copy else None


def model_based_training(
        x_data,
        y_data,
        model,
        model_forward_func,
        batch_size = 32,
        lr=1e-3,
        n_epoch = 100,
        patience = 3,
):
    x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

    train_dataset = CustomDataset(x_train, y_train)
    val_dataset = CustomDataset(x_val, y_val)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)


    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # 定义 early stopping 相关参数
    best_val_loss = float('inf')
    
    counter = 0
    pbar = tqdm(range(n_epoch))

    for epoch in pbar:
        model.train()
        train_loss = 0.0
        for batch_x, batch_y in train_dataloader:
            optimizer.zero_grad()
            output = model_forward_func(batch_x)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        model.eval()
        val_loss = 0.0
        for batch_x, batch_y in val_dataloader:
            output = model_forward_func(batch_x)
            loss = criterion(output, batch_y)
            val_loss += loss.item()

    
        pbar.set_description('Train Loss:  :{:.4f} Val Loss :{:.4f}'.format(train_loss / len(train_dataloader), val_loss / len(val_dataloader)))

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            counter = 0
        else:
            counter += 1
            if counter >= patience:
                print("Early stopping!")
                break
    return model



def calcu_potential(
        adata, 
        embedding_key, 
        velocity_key, 
        batch_size = 32,
        lr=1e-3,
        n_epoch = 100,
        copy=False
):
    data = adata.copy() if copy else adata
    x_data = data.obsm[embedding_key] 
    y_data = data.obsm[velocity_key]  

    model = potentialMLP(dim=data.obsm[embedding_key].shape[1])
    model_forward_func = model.forward
    model_based_training(x_data, y_data, model, model_forward_func,
                         batch_size, lr, n_epoch)

    data.obs['potential'] = model.potential(torch.tensor(data.obsm[embedding_key])).detach().numpy()
    data.obs['potential_pseudotime'] = 1 - (data.obs['potential'] - np.min(data.obs['potential'])) / (np.max(data.obs['potential']) - np.min(data.obs['potential']))
    return (data, model) if copy else model