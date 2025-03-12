import sys
import torch

print("Python interpreter",sys.executable)
print("Pytorch CUDA available",torch.cuda.is_available())