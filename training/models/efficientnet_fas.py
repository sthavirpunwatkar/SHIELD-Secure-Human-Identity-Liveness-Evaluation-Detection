"""
EfficientNet-B0 Fine-Tuned for Face Anti-Spoofing (FAS)

Uses torchvision's EfficientNet-B0 with ImageNet pretrained weights.
The last 4 feature blocks + head are unfrozen for domain adaptation.

Input:  3 × 224 × 224  (RGB, ImageNet-normalized)
Output: 2-class logits [spoof_score, live_score]
Backbone params: ~5.3 M (EfficientNet-B0)
"""

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import EfficientNet_B0_Weights


class EfficientNetFAS(nn.Module):
    """
    EfficientNet-B0 adapted for Face Anti-Spoofing via transfer learning.

    Strategy:
        - Load ImageNet pretrained EfficientNet-B0
        - Freeze features[0..3] (low-level texture/edge features)
        - Fine-tune features[4..8] (high-level semantic features)
        - Replace classifier with: Dropout(0.4) → Linear(1280, 512) → GELU → Dropout(0.2) → Linear(512, 2)
    """

    FREEZE_UP_TO_BLOCK = 4  # freeze MBConv blocks 0..3

    def __init__(
        self,
        num_classes: int = 2,
        drop_rate: float = 0.4,
        pretrained: bool = True,
    ) -> None:
        super().__init__()

        weights = EfficientNet_B0_Weights.IMAGENET1K_V1 if pretrained else None
        backbone = models.efficientnet_b0(weights=weights)

        # ---- Freeze early blocks ----
        for i, block in enumerate(backbone.features):
            if i < self.FREEZE_UP_TO_BLOCK:
                for param in block.parameters():
                    param.requires_grad = False

        self.features = backbone.features        # 1280-channel feature map
        self.avgpool = backbone.avgpool          # AdaptiveAvgPool2d(1)

        in_features = backbone.classifier[1].in_features  # 1280

        # FAS-specific head: deeper than the original 1-layer classifier
        self.classifier = nn.Sequential(
            nn.Dropout(p=drop_rate),
            nn.Linear(in_features, 512),
            nn.GELU(),
            nn.Dropout(p=drop_rate / 2),
            nn.Linear(512, num_classes),
        )

        # Initialize new head
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

    def unfreeze_all(self) -> None:
        """Unfreeze all backbone parameters (call after initial warm-up)."""
        for param in self.features.parameters():
            param.requires_grad = True

    def trainable_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def total_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


def get_model(num_classes: int = 2, drop_rate: float = 0.4, pretrained: bool = True) -> EfficientNetFAS:
    """Factory function — returns a fine-tuned EfficientNetFAS."""
    return EfficientNetFAS(num_classes=num_classes, drop_rate=drop_rate, pretrained=pretrained)


# ImageNet normalization constants (use these in data preprocessing)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]


if __name__ == "__main__":
    model = get_model()
    dummy = torch.randn(2, 3, 224, 224)
    out = model(dummy)
    print(f"EfficientNet-B0 FAS  |  Output: {out.shape}")
    print(f"  Trainable: {model.trainable_params():,}  |  Total: {model.total_params():,}")
