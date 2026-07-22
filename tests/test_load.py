import sys
import pytest

@pytest.mark.skip(reason="Needs local model path")
def test_load_minifasnet():
    sys.path.append('benchmark/models/minifasnet')
    import torch
    from MiniFASNet import MiniFASNetV2
    model = MiniFASNetV2(conv6_kernel=(5, 5))
    state_dict = torch.load('benchmark/models/minifasnet/2.7_80x80_MiniFASNetV2.pth', map_location='cpu')
    model.load_state_dict(state_dict)
    print("Loaded successfully")
