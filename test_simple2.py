import torch
import torch.nn as nn
from onnxruntime.quantization import quantize_dynamic, QuantType

class CustomLinear(nn.Linear):
    def forward(self, x):
        bias = self.bias if self.bias is not None else torch.zeros(self.out_features, device=x.device)
        return torch.matmul(x, self.weight.t()) + bias

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = CustomLinear(76, 64)
    def forward(self, x):
        return self.linear(x)

model = SimpleModel()
dummy = torch.randn(1, 76)
torch.onnx.export(model, dummy, "test_simple.onnx", opset_version=17)

try:
    quantize_dynamic("test_simple.onnx", "test_simple_int8.onnx", weight_type=QuantType.QUInt8)
    print("Simple model quantization success.")
except Exception as e:
    print(f"Simple model quantization failed: {e}")
