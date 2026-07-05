from onnxruntime.quantization import quantize_dynamic, QuantType

try:
    quantize_dynamic(
        "models/rppg_1dcnn_v2_infer.onnx", 
        "models/rppg_1dcnn_v2_int8.onnx", 
        weight_type=QuantType.QUInt8,
    )
    print("Quantization successful!")
except Exception as e:
    print(f"Failed again: {e}")
