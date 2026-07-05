import torch
import torch.nn as nn
from onnxruntime.quantization import quantize_dynamic, QuantType
from onnxruntime.quantization.shape_inference import quant_pre_process

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(76, 64)
    def forward(self, x):
        return self.linear(x)

model = SimpleModel()
dummy = torch.randn(1, 76)
torch.onnx.export(model, dummy, "test_simple.onnx", opset_version=17)

try:
    quant_pre_process("test_simple.onnx", "test_simple_prep.onnx", skip_symbolic_shape=True)
    quantize_dynamic("test_simple_prep.onnx", "test_simple_int8.onnx", weight_type=QuantType.QUInt8)
    print("Simple model quantization success.")
except Exception as e:
    print(f"Simple model quantization failed: {e}")
