import torch
from tqdm import tqdm
import numpy as np


class MLP(torch.nn.Module):
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
    
    def forward(self, x):
        return self.net(x) 
    def compute_G(self, x):
        pass


def _train_ode(
        model : torch.nn.Module, 
        optimizer : torch.optim.Optimizer, 
        sample_fun, 
        iter_n=10000,
        additional_loss=None):
    """Fit a neural network given sampling velocity function

    Args:
        model: Neural network model to fit vector field (e.g. MLP)
        optimizer: Optimizer for optimize parameter of model
        sample_fun: Sampling velocity function

    Returns:
        Trained neural network

    """
    history = []
    pbar = tqdm(range(iter_n))
    best_loss = np.inf
    losses = []
    for i in pbar:
        optimizer.zero_grad()
        
        t, xt, ut = sample_fun()
        vt = model(t, xt)
        #vt = model(torch.cat([xt, t], dim=-1))
        loss = torch.mean((vt - ut) ** 2)
        if additional_loss != None:
            loss += additional_loss()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        history.append(loss.item())
        if i % 100 == 0:
            losses = np.mean(losses)
            best_loss = np.min([losses, best_loss])
            pbar.set_description('loss :{:.4f} best :{:.4f}'.format(losses, best_loss))
            losses = []
    return model, np.array(history)

def _train_sde(model, score_model, optimizer, sample_fun, sigma, iter_n=10000):
    try:
        from torchcfm.conditional_flow_matching import SchrodingerBridgeConditionalFlowMatcher
        
    except ImportError:
        raise ImportError(
                "Please install the OTCFM algorithm: `https://github.com/atong01/conditional-flow-matching`.")
    SPSF2M = SchrodingerBridgeConditionalFlowMatcher(sigma=sigma)
    pbar = tqdm(range(iter_n))
    best_flow_loss, best_score_loss = np.inf, np.inf
    flow_losses, score_losses = [], []
    for i in pbar:
        optimizer.zero_grad()
        
        t, xt, ut, eps = sample_fun()
        eps = torch.Tensor(eps)
        lambda_t = SPSF2M.compute_lambda(t % 1)
        vt = model(torch.cat([xt, t], dim=-1))
        st = score_model(torch.cat([xt, t], dim=-1))
        flow_loss = torch.mean((vt - ut) ** 2)
    
        score_loss = torch.mean((lambda_t * st + eps) ** 2)
        loss = flow_loss + score_loss
        loss.backward()
        optimizer.step()
        flow_losses.append(flow_loss.item())
        score_losses.append(score_loss.item())
        if i % 10 == 0:
            flow_losses, score_losses = np.mean(flow_losses), np.mean(score_losses)
            best_flow_loss, best_score_loss = np.min([flow_losses, best_flow_loss]), np.min([score_losses, best_score_loss])
            pbar.set_description('loss :{:.4f} | {:.4f}; best :{:.4f} | {:.4f}'.format(flow_losses, score_losses, best_flow_loss, best_score_loss))
            flow_losses, score_losses = [], []
    return model, score_model