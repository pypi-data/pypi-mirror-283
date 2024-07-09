Modelling and Deciphering Cell Dynamics with Time-series or Snapshot Single Cell Dataset by Graphical Optimal Transport(GOT)
First release. 
- [x] Velocity (snapshot)
- [x] Velocity (time-series)
- [x] Trajectory
- [ ] Cell Fate
- [x] Global Gene Regulatory Network
- [x] Local Gene Regulatory Network
- [ ] GRN Decomposition
- [ ] Perturbation

## Installation
### Installation with pip
To install with pip, run the following from a terminal:
```
conda create -n pyGOT python==3.10.0
pip install py-scgot
```

### Installation from GitHub
To clone the repository and install manually, run the following from a terminal:

```
git clone git@github.com:Witiy/pyGOT.git
cd pyGOT
conda create -n pyGOT python==3.10.0
python setup.py install
```

## Usage
### Velocity
#### snapshot
```
import pygot
model = pygot.tl.gotplus.gotplus_pipeline(adata, embedding_key='X_pca', kernel='dpt', scale=True, cell_type_key='cluster', plot=True, basis='tsne',
                                x_centered=False, lr=5e-3, v_centered_iter_n=500)
```

## TODO
- [ ] Architecture (beautiful interface)
- [ ] Cell fate calculation (real data)
- [ ] GRN Decomposition (real data)
- [ ] Systematically evalute method (velocity, cell fate, GRN)
- [ ] Tutorial (website)
- [ ] Document in Code
- [ ] Perturbation


