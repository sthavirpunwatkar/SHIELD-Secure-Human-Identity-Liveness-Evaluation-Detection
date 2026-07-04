import os
import sys
import argparse
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split

# Ensure we can import from training and inference
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from training.dataset import FASDataset, FASAugmentation

def build_model(num_classes=2):
    """Build the MiniFASNet model with 2 output classes (Live/Spoof)."""
    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(64),
        nn.ReLU(),
        nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(128),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Dropout(0.3),
        nn.Linear(128, num_classes)
    )
    return model

def evaluate(model, dataloader, device, criterion):
    """Evaluate model and return metrics dict."""
    model.eval()
    val_loss = 0.0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * inputs.size(0)
            
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
    val_loss = val_loss / len(dataloader.dataset)
    
    all_preds = torch.tensor(all_preds)
    all_labels = torch.tensor(all_labels)
    
    tp = torch.sum((all_labels == 1) & (all_preds == 1)).item()
    tn = torch.sum((all_labels == 0) & (all_preds == 0)).item()
    fp = torch.sum((all_labels == 0) & (all_preds == 1)).item()
    fn = torch.sum((all_labels == 1) & (all_preds == 0)).item()
    
    spoof_count = torch.sum(all_labels == 0).item()
    live_count = torch.sum(all_labels == 1).item()
    
    apcer = fp / spoof_count if spoof_count > 0 else 0
    bpcer = fn / live_count if live_count > 0 else 0
    acer = (apcer + bpcer) / 2
    acc = (tp + tn) / (spoof_count + live_count) if (spoof_count + live_count) > 0 else 0
    
    return {
        'loss': val_loss,
        'acc': acc,
        'apcer': apcer,
        'bpcer': bpcer,
        'acer': acer
    }

def train(args):
    print("--- Starting SHIELD Anti-Spoof Training ---")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    train_dataset = FASDataset(root_dir=args.data_dir, split='train', img_size=args.img_size)
    
    if len(train_dataset) == 0:
        print(f"No training data found in {args.data_dir}. Generating dummy data for dry run.")
        train_dataset.samples = [('dummy', i % 2) for i in range(100)]
        
    # Split into train/val
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_ds, val_ds = random_split(train_dataset, [train_size, val_size])
    
    # Override transform for val
    val_ds.dataset.transform = FASAugmentation(is_train=False)
    
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)
    
    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    
    best_acer = float('inf')
    patience_counter = 0
    
    os.makedirs(args.save_dir, exist_ok=True)
    save_path = os.path.join(args.save_dir, "minifas_antispoof_v1.pt")
    
    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0
        
        for inputs, labels in train_loader:
            if isinstance(inputs, list): # dummy handling
                inputs = torch.randn(len(labels), 3, args.img_size, args.img_size)
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
            
        scheduler.step()
        train_loss = running_loss / len(train_loader.dataset)
        
        if len(val_loader) > 0:
            val_metrics = evaluate(model, val_loader, device, criterion)
            print(f"Epoch {epoch+1}/{args.epochs} - Train Loss: {train_loss:.4f} - Val ACER: {val_metrics['acer']:.4f} (APCER: {val_metrics['apcer']:.4f}, BPCER: {val_metrics['bpcer']:.4f})")
            
            if val_metrics['acer'] < best_acer:
                best_acer = val_metrics['acer']
                patience_counter = 0
                torch.save(model.state_dict(), save_path)
                print(f"  [+] Best model saved with ACER: {best_acer:.4f}")
            else:
                patience_counter += 1
                
            if patience_counter >= args.patience:
                print(f"Early stopping triggered at epoch {epoch+1}")
                break
        else:
            print(f"Epoch {epoch+1}/{args.epochs} - Train Loss: {train_loss:.4f}")
            torch.save(model.state_dict(), save_path)
            
    print(f"Training complete. Best ACER: {best_acer:.4f}. Model saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SHIELD Anti-Spoof Training')
    parser.add_argument('--data-dir', type=str, default='data/NUAA', help='Dataset root directory')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--save-dir', type=str, default='models')
    parser.add_argument('--img-size', type=int, default=80)
    parser.add_argument('--patience', type=int, default=10)
    args = parser.parse_args()
    train(args)
