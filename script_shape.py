import onnx
from onnx import shape_inference
try:
    model = onnx.load("models/rppg_1dcnn_v2.onnx")
    inferred = shape_inference.infer_shapes(model)
    onnx.save(inferred, "models/rppg_1dcnn_v2_infer.onnx")
    print("Shape inference success.")
except Exception as e:
    print(f"Shape inference failed: {e}")
