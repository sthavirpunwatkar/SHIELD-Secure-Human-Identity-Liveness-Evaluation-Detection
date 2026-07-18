import torch
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'benchmark/models/minifasnet'))
from benchmark.adapters.minifasnet_adapter import MiniFASNetAdapter
from benchmark.adapters.physnet_adapter import PhysNetAdapter

print("--- MiniFASNet ---")
m = MiniFASNetAdapter()
m.load_model()
tensor = np.random.rand(1, 3, 80, 80).astype(np.float32)
out = m.infer(tensor)
print("Output shape:", out.shape)

print("--- PhysNet ---")
p = PhysNetAdapter()
p.load_model()
tensor = np.random.rand(1, 3, 32, 128, 128).astype(np.float32)
out = p.infer(tensor)
print("Output shape:", out.shape)
