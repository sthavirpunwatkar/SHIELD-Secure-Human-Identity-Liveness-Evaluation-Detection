"""
MiniFASNet-V2 — Lightweight Face Anti-Spoofing Network
=======================================================

Architecture (MobileNet-style depthwise separable convolutions + SE attention):

  Input  : 3 × 80 × 80
  Stem   : Conv 3×3, stride 2  →  32 × 40 × 40
  Stage 1: DSConv ×2           →  64 × 20 × 20  (+SE)
  Stage 2: DSConv ×2           → 128 × 10 × 10  (+SE)
  Stage 3: DSConv ×2           → 256 ×  5 ×  5  (+SE)
  Head   : GAP → BN1d → Dropout(0.4) → Linear(256, 2)

Total parameters: ~510 K  (fits easily inside 3 GB VRAM).

Design choices
--------------
* ReLU6 prevents activation blow-up on quantised / low-precision hardware.
* SEBlock (reduction=4) adds negligible cost but meaningfully boosts accuracy.
* BatchNorm1d in the classification head normalises the final feature vector —
  this directly addresses the "no feature normalisation" weakness of the v1 CNN.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------

class DepthwiseSeparableConv(nn.Module):
    """Depthwise-separable convolution block.

    Depthwise conv (groups=C_in) → BN → ReLU6
    Pointwise conv (1×1)         → BN → ReLU6
    """

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1) -> None:
        super().__init__()
        self.dw = nn.Conv2d(
            in_channels, in_channels, kernel_size=3, stride=stride,
            padding=1, groups=in_channels, bias=False,
        )
        self.bn_dw = nn.BatchNorm2d(in_channels)
        self.pw = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn_pw = nn.BatchNorm2d(out_channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu6(self.bn_dw(self.dw(x)), inplace=True)
        x = F.relu6(self.bn_pw(self.pw(x)), inplace=True)
        return x


class SEBlock(nn.Module):
    """Squeeze-and-Excitation channel attention.

    Squeeze  : global average pool  → (B, C)
    Excite   : FC-ReLU-FC-Sigmoid   → (B, C, 1, 1)
    Scale    : element-wise multiply
    """

    def __init__(self, channels: int, reduction: int = 4) -> None:
        super().__init__()
        mid = max(1, channels // reduction)
        self.avg = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, mid, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(mid, channels, bias=False),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, c, _, _ = x.shape
        s = self.avg(x).view(b, c)
        s = self.fc(s).view(b, c, 1, 1)
        return x * s


# ---------------------------------------------------------------------------
# Main model
# ---------------------------------------------------------------------------

class MiniFASNetV2(nn.Module):
    """MiniFASNet-V2 for binary liveness classification (live=1, spoof=0).

    Args:
        num_classes: Number of output logits (default 2).
        drop_rate  : Dropout probability before the final FC layer (default 0.4).
    """

    def __init__(self, num_classes: int = 2, drop_rate: float = 0.4) -> None:
        super().__init__()

        # ── Stem ────────────────────────────────────────────────────────────
        # 3 × 80 × 80  →  32 × 40 × 40
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU6(inplace=True),
        )

        # ── Stage 1 ─────────────────────────────────────────────────────────
        # 32 × 40 × 40  →  64 × 20 × 20
        self.stage1 = nn.Sequential(
            DepthwiseSeparableConv(32, 32, stride=1),
            DepthwiseSeparableConv(32, 64, stride=2),
        )
        self.se1 = SEBlock(64)

        # ── Stage 2 ─────────────────────────────────────────────────────────
        # 64 × 20 × 20  →  128 × 10 × 10
        self.stage2 = nn.Sequential(
            DepthwiseSeparableConv(64, 64, stride=1),
            DepthwiseSeparableConv(64, 128, stride=2),
        )
        self.se2 = SEBlock(128)

        # ── Stage 3 ─────────────────────────────────────────────────────────
        # 128 × 10 × 10  →  256 × 5 × 5
        self.stage3 = nn.Sequential(
            DepthwiseSeparableConv(128, 128, stride=1),
            DepthwiseSeparableConv(128, 256, stride=2),
        )
        self.se3 = SEBlock(256)

        # ── Classification head ──────────────────────────────────────────────
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.BatchNorm1d(256),          # ← feature normalisation (v2 upgrade)
            nn.Dropout(p=drop_rate),
            nn.Linear(256, num_classes),
        )

        self._init_weights()

    # -----------------------------------------------------------------------
    def _init_weights(self) -> None:
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, (nn.BatchNorm2d, nn.BatchNorm1d)):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    # -----------------------------------------------------------------------
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Float tensor (N, 3, 80, 80).

        Returns:
            Logits (N, num_classes).
        """
        x = self.stem(x)           # 32 × 40 × 40
        x = self.se1(self.stage1(x))   # 64 × 20 × 20
        x = self.se2(self.stage2(x))   # 128 × 10 × 10
        x = self.se3(self.stage3(x))   # 256 × 5 × 5
        x = self.pool(x)           # 256 × 1 × 1
        x = self.classifier(x)    # num_classes
        return x

    # -----------------------------------------------------------------------
    def count_parameters(self) -> int:
        """Return total trainable parameter count."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def get_model(num_classes: int = 2, drop_rate: float = 0.4) -> MiniFASNetV2:
    """Factory — returns a freshly initialised MiniFASNetV2."""
    return MiniFASNetV2(num_classes=num_classes, drop_rate=drop_rate)


def count_parameters(model: nn.Module) -> int:
    """Count trainable parameters in any nn.Module."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    model = get_model()
    dummy = torch.randn(4, 3, 80, 80)
    out = model(dummy)
    n = count_parameters(model)
    print(f"MiniFASNet-V2  |  output: {out.shape}  |  params: {n:,}")
    assert out.shape == (4, 2), f"Unexpected output shape: {out.shape}"
    print("Self-test PASSED.")
