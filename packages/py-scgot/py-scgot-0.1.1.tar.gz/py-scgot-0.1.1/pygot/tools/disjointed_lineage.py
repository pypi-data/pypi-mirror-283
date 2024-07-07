from collections import deque
import scanpy as sc
import numpy as np

def detect_disjointed_lineage(adata, cell_type_key, percentile=50):
    adata.obs[cell_type_key] = adata.obs[cell_type_key].astype("category")
    sc.tl.paga(adata, groups=cell_type_key, model='v1.2')
    sc.pl.paga(adata, color=cell_type_key)
    
    node_name = adata.obs[cell_type_key].dtypes.categories
    cutoff = np.percentile(adata.uns['paga']['connectivities'].data, percentile)

    adj_matrix = adata.uns['paga']['connectivities'].toarray()
    adj_matrix[adj_matrix < cutoff] = 0
    res = find_subgraphs(adj_matrix)
    subgraphs = []
    for item in res:
        subgraphs.append(node_name[item])
    subgraphs = sorted(subgraphs, key=lambda x: -len(x))
    
    if len(subgraphs) >= 2:
        print('Detect disjointed lineage! Lineage number :{}'.format(len(subgraphs)))
        for i, subgraph in enumerate(subgraphs):
            print('Lineage {} :'.format(i), subgraph.tolist())
    else:
        print('No disjointed lineage.')
    return subgraphs
    
def bfs(node, adj_matrix, visited, subgraph):
    queue = deque([node])
    visited[node] = True
    while queue:
        current = queue.popleft()
        subgraph.append(current)
        for neighbor, is_connected in enumerate(adj_matrix[current]):
            if is_connected and not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

def find_subgraphs(adj_matrix):
    num_nodes = adj_matrix.shape[0]
    visited = [False] * num_nodes
    subgraphs = []

    for node in range(num_nodes):
        if not visited[node]:
            subgraph = []
            bfs(node, adj_matrix, visited, subgraph)
            subgraphs.append(subgraph)
    
    return subgraphs

