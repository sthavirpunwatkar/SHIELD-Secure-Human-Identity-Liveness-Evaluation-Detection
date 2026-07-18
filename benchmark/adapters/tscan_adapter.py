import os
import numpy as np
from .base_adapter import BenchmarkModel

class TSCANAdapter(BenchmarkModel):
    def __init__(self, model_path="benchmark/models/tscan/mtts_can.hdf5"):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        raise EnvironmentError("TS-CAN official weights are in .hdf5 format requiring TensorFlow. Environment is PyTorch-only. Integration stopped due to framework incompatibility.")

    def preprocess(self, input_data):
        return None

    def infer(self, tensor):
        return None

    def postprocess(self, output):
        return None

    def metadata(self):
        return {
            "name": "TS-CAN",
            "input_resolution": "36x36",
            "framework": "TensorFlow (Incompatible)",
            "category": "rPPG"
        }
