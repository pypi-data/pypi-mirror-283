import torch
from jacobian import GRN
import numpy as np
def cos_loss(vector1, vector2):
    dot_product = torch.dot(vector1, vector2)

    # 计算向量的模长
    norm1 = torch.norm(vector1)
    norm2 = torch.norm(vector2)

    # 计算余弦相似度
    return dot_product / (norm1 * norm2)

def mean_taylor_approximate(grn : GRN, x):
    v = []
    for i in range(grn.shape[0]):
        v.append(grn.latent_jacobian[i] @ x[i][:, None])
    v = torch.Tensor(np.array(v).reshape(len(v),-1))
    return v

def get_observed_v(grn1, grn2, x1, x2):
    v1 = mean_taylor_approximate(grn1, x1)
    v2 = mean_taylor_approximate(grn2, x2)
    return v1, v2