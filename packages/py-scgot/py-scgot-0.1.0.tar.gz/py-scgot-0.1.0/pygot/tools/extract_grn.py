import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from tqdm import tqdm
from pygot.evalute import *


# 定义多元多任务回归模型
class MultiTaskRegression(nn.Module):
    def __init__(self, input_size, output_size, init_jacobian, beta_grad=True, init_beta=1., min_beta=0.0):
        super(MultiTaskRegression, self).__init__()
        self.linear = nn.Parameter(init_jacobian)
        self.linear.register_hook(self.remove_diagonal_hook)
        if beta_grad:
            self.beta = nn.Parameter(init_beta*torch.ones(output_size))
            self.beta.register_hook(self.hinge_hook)
            self.min_beta = torch.tensor(min_beta)
        else:
            self.beta = init_beta*torch.ones(output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        return (self.linear @ x[:,:,None]).squeeze(-1) - self.relu(self.beta) * x
    
    def hinge_hook(self, grad):
        with torch.no_grad():
            self.beta.data = torch.clamp(self.beta, min=self.min_beta)
            #self.beta[self.beta < self.min_beta] = self.min_beta
        return grad
        
        

    def remove_diagonal_hook(self, grad):
        with torch.no_grad():
            self.linear -= torch.diag(torch.diag(self.linear))
            #self.linear.weight[self.linear.weight < 0] = 0
            
        return grad



class GRN:
    def __init__(self, G_hat:MultiTaskRegression, gene_names):
        self.model = G_hat
        self.G = G_hat.linear.detach().numpy()
        self.beta = G_hat.beta.data.detach().numpy()
        self.ranked_edges = get_ranked_edges(self.G, gene_names=gene_names)


def optimize_global_GRN(prototype_adata, time_key, beta_grad=True, num_epochs=100000, lr=0.01, l1_penalty = 0.005, init_beta=1.0, min_beta=1.0, coverage_cutoff=5e-3, true_df=None, init_jacobian=None, A=None):
    print('l1_penalty:', l1_penalty, 'min_beta:', min_beta)
    print('Coverage when weight change below {}'.format(coverage_cutoff))
    
    
    y = torch.Tensor(prototype_adata.obsm['y'])
    
    if init_jacobian is None:

        init_jacobian = torch.rand(prototype_adata.X.shape[1],prototype_adata.X.shape[1])
    

    X_train = torch.Tensor(prototype_adata.X)
    y_train = y


    # 初始化模型
    input_size = X_train.shape[1]
    output_size = y_train.shape[1]  # 多任务回归的输出维度
    
    G_hat = MultiTaskRegression(input_size, output_size, init_jacobian, beta_grad, init_beta, min_beta)
    if true_df is not None:
        pred_df = get_ranked_edges(G_hat.linear.detach().numpy(), gene_names=prototype_adata.var.index)
        pr = compute_pr(true_df, pred_df)
        print('Init', pr)
    optimizer = optim.SGD(G_hat.parameters(), lr=lr)
    loss_list = []
    # 训练模型
    prev_weights = G_hat.linear.clone() 
    
    pbar = tqdm(range(num_epochs))
    for epoch in pbar:
        optimizer.zero_grad()
        # 前向传播
        outputs = G_hat(X_train)
        
        #loss = torch.mean(weights * ((outputs - y_train) ** 2))
        mse_loss = torch.mean( ((outputs - y_train) ** 2))
        # L1正则化损失
        l1_loss = l1_penalty * torch.norm(G_hat.linear, p=1)
        loss = mse_loss + l1_loss
        # 反向传播和优化
        
        loss.backward()
        optimizer.step()

        if (epoch+1) % 100 == 0:
            # 检查权重是否收敛
            current_weights = G_hat.linear.clone()
            
            weight_change = torch.norm(current_weights - prev_weights)
            if weight_change < coverage_cutoff:  # 设置一个阈值，例如1e-4
                print(f'Converged at epoch {epoch+1}. Weight change: {weight_change.item():.5f}')
                break
    
            prev_weights = current_weights  # 更新前一次的权重
            if true_df is not None:
                matrix = G_hat.linear.detach().numpy()
                if A is not None:
                    matrix = A @ matrix @ A.T
                pred_df = get_ranked_edges(matrix, gene_names=prototype_adata.uns['gene_name'])
                pr = compute_pr(true_df, pred_df)
                epr, _ = compute_epr(true_df, pred_df, len(prototype_adata.var), False)
                pbar.set_description(f'Epoch [{epoch+1}/{num_epochs}], PR: {pr:.4f} EPR: {epr:.4f} | Weight change: {weight_change.item():.4f} | Loss: {loss.item():.4f} MSELoss: {mse_loss.item():.4f} L1Loss: {l1_loss.item():.4f}')
            else:
                pbar.set_description(f'Epoch [{epoch+1}/{num_epochs}],  Weight change: {weight_change.item():.4f} Loss: {loss.item():.4f}')
            
            
        loss_list.append(loss.item())
        
    return G_hat, np.array(loss_list)


def get_ranked_edges(jacobian, gene_names):

    df = pd.DataFrame(jacobian, index=gene_names, columns=gene_names).T
    stacked = df.stack()
    result = stacked.reset_index()
    result.columns = ['Gene1', 'Gene2', 'EdgeWeight']
    result['absEdgeWeight'] = abs(result.EdgeWeight)
    result = result.sort_values('absEdgeWeight', ascending=False)
    return result


def infer_GRN(adata, time_key, beta_grad=True, num_epochs=100000, lr=0.01, l1_penalty = 0.005, init_beta=1.0, min_beta=1.0, coverage_cutoff=5e-3, true_df=None, init_jacobian=None, A=None):
    G_hat, _ = optimize_global_GRN(adata, time_key,  beta_grad, num_epochs, lr, l1_penalty, init_beta, min_beta, coverage_cutoff, true_df, init_jacobian, A)
    grn = GRN(G_hat, adata.uns['gene_name'])
    return grn

'''
def infer_GRN(
        model, adata, time_key, embedding_key, 
        cluster_num=2, percent=5, num_epochs=100000, 
        lr=0.01, l1_penalty = 0.005, init_beta=1.0, min_beta=1.0, coverage_cutoff=5e-2, 
        true_df=None, init_jacobian=None):
    
    prototype_adata = construct_prototype_adata(model, adata, time_key, embedding_key, cluster_num, percent)
    
    G_hat, history = optimize_global_GRN(prototype_adata, time_key, num_epochs, lr, l1_penalty, init_beta, min_beta, coverage_cutoff, true_df, init_jacobian=init_jacobian)
    
    GRN_matrix = G_hat.linear.detach().numpy()
    
    pred_df = get_ranked_edges(GRN_matrix, gene_names=adata.var.index)
    return pred_df, GRN_matrix

def infer_GRN_ensemble(model_list, adata, time_key, embedding_key, cluster_num=2, percent=5, num_epochs=100000, lr=0.01, l1_penalty = 0.005, 
            min_beta=1.0, init_beta=1.0, coverage_cutoff=5e-2, true_df=None, init_jacobian=None):
    ensemble_GRN = []
    ensemble_adata = []
    for model in model_list:
        prototype_adata = construct_prototype_adata(model, adata, time_key, embedding_key, cluster_num=cluster_num, percent=percent)
        ensemble_adata.append(prototype_adata)
    ensemble_adata = sc.concat(ensemble_adata)
    print('Flow Number: ', len(ensemble_adata))
    G_hat, history = optimize_global_GRN(ensemble_adata, time_key, num_epochs, lr, l1_penalty, init_beta, min_beta, coverage_cutoff, true_df=true_df, init_jacobian=init_jacobian)
    
    ensemble_GRN = G_hat.linear.detach().numpy()

    pred_df = get_ranked_edges(ensemble_GRN, gene_names=adata.var.index)
    return pred_df, ensemble_GRN
'''