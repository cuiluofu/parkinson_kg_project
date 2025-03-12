import torch
import numpy as np
import networkx as nx
import pandas as pd


print(f"PyTorch CUDA available:{torch.cuda.is_available()}")
print(f"Numpy version:{np.__version__}")

G = nx.Graph()
G.add_edge("Parkinson","Tremor")
print(f"Networkx test - Nodes: {G.nodes()}")


df = pd.DataFrame({'entity': ['Parkinson','Tremor'], 'type':['Disease','Symptom']})
print("Pandas DataFrame test:\n", df.head())