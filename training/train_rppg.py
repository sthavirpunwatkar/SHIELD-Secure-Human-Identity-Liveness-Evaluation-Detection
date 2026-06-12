import os
import sys
import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from training.rppg_dataset import RPPGDataset

def build_rppg_model(window_size=30):
    model = nn.Sequential(
        nn.Conv1d(1, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool1d(2),
        nn.Conv1d(16, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.AdaptiveAvgPool1d(1),
        nn.Flatten(),
        nn.Linear(32, 1),
        nn.Sigmoid()
    )
    return model

def evaluate(model, dataloader, device, criterion):
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
            
            all_preds.extend(outputs.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
    val_loss /= len(dataloader.dataset)
    all_preds = torch.tensor(np.array(all_preds)).squeeze()
    all_labels = torch.tensor(np.array(all_labels)).squeeze()
    
    preds_binary = (all_preds > 0.5).float()
    acc = (preds_binary == all_labels).float().mean().item()
    
    return {
        'loss': val_loss,
        'acc': acc
    }

def train(args):
    print("--- Starting rPPG 1D-CNN Training ---")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    dataset = RPPGDataset(video_dir=args.data_dir if not args.use_synthetic else None, window_size=args.window_size)
    
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)
    
    model = build_rppg_model(window_size=args.window_size).to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    best_loss = float('inf')
    patience_counter = 0
    os.makedirs(args.save_dir, exist_ok=True)
    save_path = os.path.join(args.save_dir, "rppg_1dcnn_v1.pt")
    
    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
            
        train_loss = running_loss / len(train_loader.dataset)
        val_metrics = evaluate(model, val_loader, device, criterion)
        
        print(f"Epoch {epoch+1}/{args.epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_metrics['loss']:.4f} - Val Acc: {val_metrics['acc']:.4f}")
        
        if val_metrics['loss'] < best_loss:
            best_loss = val_metrics['loss']
            patience_counter = 0
            torch.save(model.state_dict(), save_path)
            print("  [+] Best model saved")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print(f"Early stopping at epoch {epoch+1}")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str, default='data/UBFC-rPPG')
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch-size', type=int, default=128)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--save-dir', type=str, default='models')
    parser.add_argument('--window-size', type=int, default=30)
    parser.add_argument('--patience', type=int, default=15)
    parser.add_argument('--use-synthetic', action='store_true')
    args = parser.parse_args()
    train(args)
