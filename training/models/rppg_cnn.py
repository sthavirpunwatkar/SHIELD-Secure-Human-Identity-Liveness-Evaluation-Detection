"""
Upgraded 1D-CNN + FFT Dual-Branch rPPG Model

Architecture:
  Branch A (Temporal): Conv1d stack (1→16→32→64→128) + GlobalAvgPool
  Branch B (Frequency): FFT of input → magnitude spectrum → 2-layer MLP (freq_size, 64, 32)
  Fusion: Concat(128, 32) → Linear(160, 1) → Sigmoid

Input:  (B, 1, window_size)   — normalized rPPG signal
Output: (B, 1)                — liveness probability
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class TemporalBranch(nn.Module):
    """1D Conv stack for temporal signal processing."""

    def __init__(self, window_size: int = 150) -> None:
        super().__init__()
        self.conv_stack = nn.Sequential(
            # Block 1
            nn.Conv1d(1, 16, kernel_size=7, padding=3, bias=False),
            nn.BatchNorm1d(16),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Dropout(0.1),

            # Block 2
            nn.Conv1d(16, 32, kernel_size=5, padding=2, bias=False),
            nn.BatchNorm1d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Dropout(0.1),

            # Block 3
            nn.Conv1d(32, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(2),

            # Block 4
            nn.Conv1d(64, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
        )
        self.pool = nn.AdaptiveAvgPool1d(1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, 1, T)"""
        x = self.conv_stack(x)   # (B, 128, T')
        x = self.pool(x)          # (B, 128, 1)
        return x.squeeze(-1)      # (B, 128)


class FrequencyBranch(nn.Module):
    """FFT-based frequency domain feature extractor."""

    def __init__(self, window_size: int = 150, freq_out: int = 32) -> None:
        super().__init__()
        self.freq_size = window_size // 2 + 1  # rfft output size

        self.mlp = nn.Sequential(
            nn.Linear(self.freq_size, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(64, freq_out),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, 1, T)"""
        sig = x.squeeze(1)                           # (B, T)
        freq = torch.fft.rfft(sig, norm="ortho")     # (B, T//2+1) complex
        mag = torch.abs(freq)                        # (B, T//2+1) magnitude
        # Pad / truncate to expected size
        if mag.shape[-1] != self.freq_size:
            mag = F.adaptive_avg_pool1d(mag.unsqueeze(1), self.freq_size).squeeze(1)
        out = self.mlp(mag)                          # (B, freq_out)
        return out


class RPPGCNNv2(nn.Module):
    """
    Dual-branch rPPG liveness model (Temporal + Frequency fusion).

    Args:
        window_size: Number of frames in the signal window (default 150 @ 30fps = 5s)
        freq_out: Frequency branch output dimension
    """

    def __init__(self, window_size: int = 150, freq_out: int = 32) -> None:
        super().__init__()
        self.window_size = window_size

        self.temporal = TemporalBranch(window_size)
        self.frequency = FrequencyBranch(window_size, freq_out)

        fused_dim = 128 + freq_out
        self.fusion = nn.Sequential(
            nn.Linear(fused_dim, 64),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

        self._init_weights()

    def _init_weights(self) -> None:
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode="fan_in", nonlinearity="relu")
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, 1, window_size)"""
        t_feat = self.temporal(x)      # (B, 128)
        f_feat = self.frequency(x)     # (B, freq_out)
        fused = torch.cat([t_feat, f_feat], dim=1)  # (B, 160)
        out = self.fusion(fused)       # (B, 1)
        return out


def get_model(window_size: int = 150) -> RPPGCNNv2:
    return RPPGCNNv2(window_size=window_size)


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ---------------------------------------------------------------------------
# Public aliases expected by train_rppg_v2.py and rppg_detector.py
# ---------------------------------------------------------------------------

#: Canonical class alias
RPPGNet = RPPGCNNv2


def build_rppg_model_v2(window_size: int = 150, dropout: float = 0.3) -> RPPGCNNv2:
    """Factory helper — mirrors legacy build_rppg_model signature."""
    return RPPGCNNv2(window_size=window_size)


if __name__ == "__main__":
    model = build_rppg_model_v2(window_size=150)
    dummy = torch.randn(8, 1, 150)
    out = model(dummy)
    print(f"RPPGCNNv2  |  Output: {out.shape}  |  Params: {count_parameters(model):,}")
    assert out.shape == (8, 1)
    assert 0.0 <= out.min().item() <= out.max().item() <= 1.0
    print("Sanity check passed.")
