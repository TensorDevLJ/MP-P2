"""
Training script for EEG CNN-LSTM model
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any
import pickle
import json
import os
from pathlib import Path
import argparse
import logging

# Add backend to path for imports
import sys
sys.path.append('../backend')

from app.services.ml.eeg_cnn_lstm import EEGCNNLSTM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EEGDataset(Dataset):
    """PyTorch dataset for EEG data"""
    
    def __init__(self, data: np.ndarray, emotion_labels: np.ndarray, anxiety_labels: np.ndarray):
        self.data = torch.FloatTensor(data)
        self.emotion_labels = torch.LongTensor(emotion_labels)
        self.anxiety_labels = torch.LongTensor(anxiety_labels)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return {
            'data': self.data[idx],
            'emotion_label': self.emotion_labels[idx],
            'anxiety_label': self.anxiety_labels[idx]
        }

class EEGModelTrainer:
    """Training pipeline for EEG models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Class mappings
        self.emotion_classes = ['happy', 'sad', 'neutral', 'stressed', 'relaxed']
        self.anxiety_classes = ['low', 'moderate', 'high']
        
        # Initialize model
        self.model = EEGCNNLSTM(
            n_channels=config.get('n_channels', 1),
            n_time_points=config.get('n_time_points', 256),
            n_classes_emotion=len(self.emotion_classes),
            n_classes_anxiety=len(self.anxiety_classes),
            dropout_rate=config.get('dropout_rate', 0.5)
        ).to(self.device)
        
    def load_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Load and preprocess training data"""
        
        logger.info(f"Loading data from {data_path}")
        
        # For demonstration, generate synthetic data
        # In production, load actual EEG datasets like DREAMER, DEAP, or SEED
        
        n_samples = self.config.get('n_samples', 1000)
        n_time_points = self.config.get('n_time_points', 256)
        
        # Generate synthetic EEG-like data
        np.random.seed(42)
        
        # Simulate different emotional states with different spectral characteristics
        data = []
        emotion_labels = []
        anxiety_labels = []
        
        for i in range(n_samples):
            # Generate base signal
            t = np.linspace(0, 2, n_time_points)  # 2 seconds
            
            # Base EEG with different frequency components
            signal = np.random.normal(0, 1, n_time_points)
            
            # Add frequency-specific patterns based on emotion
            emotion_idx = np.random.randint(0, len(self.emotion_classes))
            anxiety_idx = np.random.randint(0, len(self.anxiety_classes))
            
            if emotion_idx == 0:  # happy
                signal += 0.5 * np.sin(2 * np.pi * 10 * t)  # Strong alpha
            elif emotion_idx == 1:  # sad
                signal += 0.3 * np.sin(2 * np.pi * 4 * t)   # Strong theta
            elif emotion_idx == 3:  # stressed
                signal += 0.7 * np.sin(2 * np.pi * 20 * t)  # Strong beta
            
            # Add noise based on anxiety level
            noise_level = 0.1 + 0.2 * anxiety_idx
            signal += np.random.normal(0, noise_level, n_time_points)
            
            data.append(signal.reshape(1, -1))  # Add channel dimension
            emotion_labels.append(emotion_idx)
            anxiety_labels.append(anxiety_idx)
        
        data = np.array(data)
        emotion_labels = np.array(emotion_labels)
        anxiety_labels = np.array(anxiety_labels)
        
        logger.info(f"Generated {len(data)} synthetic EEG samples")
        logger.info(f"Data shape: {data.shape}")
        logger.info(f"Emotion distribution: {np.bincount(emotion_labels)}")
        logger.info(f"Anxiety distribution: {np.bincount(anxiety_labels)}")
        
        return data, emotion_labels, anxiety_labels
    
    def create_data_loaders(
        self, 
        data: np.ndarray, 
        emotion_labels: np.ndarray, 
        anxiety_labels: np.ndarray
    ) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """Create train/val/test data loaders"""
        
        # Create dataset
        dataset = EEGDataset(data, emotion_labels, anxiety_labels)
        
        # Split into train/val/test
        train_size = int(0.7 * len(dataset))
        val_size = int(0.15 * len(dataset))
        test_size = len(dataset) - train_size - val_size
        
        train_dataset, val_dataset, test_dataset = random_split(
            dataset, [train_size, val_size, test_size],
            generator=torch.Generator().manual_seed(42)
        )
        
        # Create data loaders
        batch_size = self.config.get('batch_size', 32)
        
        train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size, 
            shuffle=True,
            num_workers=2
        )
        val_loader = DataLoader(
            val_dataset, 
            batch_size=batch_size, 
            shuffle=False,
            num_workers=2
        )
        test_loader = DataLoader(
            test_dataset, 
            batch_size=batch_size, 
            shuffle=False,
            num_workers=2
        )
        
        return train_loader, val_loader, test_loader
    
    def train(self, train_loader: DataLoader, val_loader: DataLoader) -> Dict[str, List[float]]:
        """Train the model"""
        
        # Loss functions
        emotion_criterion = nn.CrossEntropyLoss()
        anxiety_criterion = nn.CrossEntropyLoss()
        
        # Optimizer
        optimizer = optim.Adam(
            self.model.parameters(),
            lr=self.config.get('learning_rate', 0.001),
            weight_decay=self.config.get('weight_decay', 1e-5)
        )
        
        # Learning rate scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=5, verbose=True
        )
        
        # Training loop
        num_epochs = self.config.get('num_epochs', 50)
        history = {'train_loss': [], 'val_loss': [], 'emotion_acc': [], 'anxiety_acc': []}
        
        best_val_loss = float('inf')
        patience_counter = 0
        early_stop_patience = self.config.get('early_stop_patience', 10)
        
        for epoch in range(num_epochs):
            # Training phase
            train_loss, train_emotion_acc, train_anxiety_acc = self._train_epoch(
                train_loader, emotion_criterion, anxiety_criterion, optimizer
            )
            
            # Validation phase
            val_loss, val_emotion_acc, val_anxiety_acc = self._validate_epoch(
                val_loader, emotion_criterion, anxiety_criterion
            )
            
            # Update learning rate
            scheduler.step(val_loss)
            
            # Save metrics
            history['train_loss'].append(train_loss)
            history['val_loss'].append(val_loss)
            history['emotion_acc'].append(val_emotion_acc)
            history['anxiety_acc'].append(val_anxiety_acc)
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # Save best model
                torch.save(self.model.state_dict(), 'saved_models/eeg_cnn_lstm_best.pth')
            else:
                patience_counter += 1
            
            logger.info(
                f"Epoch {epoch+1}/{num_epochs} - "
                f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, "
                f"Emotion Acc: {val_emotion_acc:.3f}, Anxiety Acc: {val_anxiety_acc:.3f}"
            )
            
            if patience_counter >= early_stop_patience:
                logger.info(f"Early stopping at epoch {epoch+1}")
                break
        
        return history
    
    def _train_epoch(
        self, 
        train_loader: DataLoader, 
        emotion_criterion: nn.Module,
        anxiety_criterion: nn.Module,
        optimizer: torch.optim.Optimizer
    ) -> Tuple[float, float, float]:
        """Train for one epoch"""
        
        self.model.train()
        total_loss = 0
        emotion_correct = 0
        anxiety_correct = 0
        total_samples = 0
        
        for batch in train_loader:
            data = batch['data'].to(self.device)
            emotion_labels = batch['emotion_label'].to(self.device)
            anxiety_labels = batch['anxiety_label'].to(self.device)
            
            optimizer.zero_grad()
            
            # Forward pass
            emotion_logits, anxiety_logits, attention_weights = self.model(data)
            
            # Compute losses
            emotion_loss = emotion_criterion(emotion_logits, emotion_labels)
            anxiety_loss = anxiety_criterion(anxiety_logits, anxiety_labels)
            
            # Multi-task loss with equal weighting
            total_batch_loss = emotion_loss + anxiety_loss
            
            # Backward pass
            total_batch_loss.backward()
            optimizer.step()
            
            # Track metrics
            total_loss += total_batch_loss.item()
            
            emotion_pred = torch.argmax(emotion_logits, dim=1)
            anxiety_pred = torch.argmax(anxiety_logits, dim=1)
            
            emotion_correct += (emotion_pred == emotion_labels).sum().item()
            anxiety_correct += (anxiety_pred == anxiety_labels).sum().item()
            total_samples += len(data)
        
        avg_loss = total_loss / len(train_loader)
        emotion_acc = emotion_correct / total_samples
        anxiety_acc = anxiety_correct / total_samples
        
        return avg_loss, emotion_acc, anxiety_acc
    
    def _validate_epoch(
        self,
        val_loader: DataLoader,
        emotion_criterion: nn.Module,
        anxiety_criterion: nn.Module
    ) -> Tuple[float, float, float]:
        """Validate for one epoch"""
        
        self.model.eval()
        total_loss = 0
        emotion_correct = 0
        anxiety_correct = 0
        total_samples = 0
        
        with torch.no_grad():
            for batch in val_loader:
                data = batch['data'].to(self.device)
                emotion_labels = batch['emotion_label'].to(self.device)
                anxiety_labels = batch['anxiety_label'].to(self.device)
                
                emotion_logits, anxiety_logits, _ = self.model(data)
                
                emotion_loss = emotion_criterion(emotion_logits, emotion_labels)
                anxiety_loss = anxiety_criterion(anxiety_logits, anxiety_labels)
                total_batch_loss = emotion_loss + anxiety_loss
                
                total_loss += total_batch_loss.item()
                
                emotion_pred = torch.argmax(emotion_logits, dim=1)
                anxiety_pred = torch.argmax(anxiety_logits, dim=1)
                
                emotion_correct += (emotion_pred == emotion_labels).sum().item()
                anxiety_correct += (anxiety_pred == anxiety_labels).sum().item()
                total_samples += len(data)
        
        avg_loss = total_loss / len(val_loader)
        emotion_acc = emotion_correct / total_samples
        anxiety_acc = anxiety_correct / total_samples
        
        return avg_loss, emotion_acc, anxiety_acc
    
    def evaluate(self, test_loader: DataLoader) -> Dict[str, Any]:
        """Evaluate model on test set"""
        
        self.model.eval()
        emotion_predictions = []
        anxiety_predictions = []
        emotion_true = []
        anxiety_true = []
        
        with torch.no_grad():
            for batch in test_loader:
                data = batch['data'].to(self.device)
                emotion_labels = batch['emotion_label']
                anxiety_labels = batch['anxiety_label']
                
                emotion_logits, anxiety_logits, _ = self.model(data)
                
                emotion_pred = torch.argmax(emotion_logits, dim=1).cpu()
                anxiety_pred = torch.argmax(anxiety_logits, dim=1).cpu()
                
                emotion_predictions.extend(emotion_pred.numpy())
                anxiety_predictions.extend(anxiety_pred.numpy())
                emotion_true.extend(emotion_labels.numpy())
                anxiety_true.extend(anxiety_labels.numpy())
        
        # Generate classification reports
        emotion_report = classification_report(
            emotion_true, emotion_predictions,
            target_names=self.emotion_classes,
            output_dict=True
        )
        
        anxiety_report = classification_report(
            anxiety_true, anxiety_predictions,
            target_names=self.anxiety_classes,
            output_dict=True
        )
        
        # Generate confusion matrices
        emotion_cm = confusion_matrix(emotion_true, emotion_predictions)
        anxiety_cm = confusion_matrix(anxiety_true, anxiety_predictions)
        
        return {
            'emotion_report': emotion_report,
            'anxiety_report': anxiety_report,
            'emotion_confusion_matrix': emotion_cm,
            'anxiety_confusion_matrix': anxiety_cm,
            'emotion_accuracy': emotion_report['accuracy'],
            'anxiety_accuracy': anxiety_report['accuracy']
        }
    
    def save_model(self, save_path: str, metadata: Dict[str, Any]):
        """Save trained model with metadata"""
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save model state dict
        torch.save(self.model.state_dict(), save_path)
        
        # Save metadata
        metadata_path = save_path.replace('.pth', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {save_path}")

def main():
    """Main training script"""
    
    parser = argparse.ArgumentParser(description="Train EEG CNN-LSTM model")
    parser.add_argument("--data_path", type=str, default="datasets/synthetic_eeg.csv")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--save_path", type=str, default="saved_models/eeg_cnn_lstm.pth")
    
    args = parser.parse_args()
    
    # Training configuration
    config = {
        'n_channels': 1,
        'n_time_points': 256,
        'num_epochs': args.epochs,
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'dropout_rate': 0.5,
        'weight_decay': 1e-5,
        'early_stop_patience': 10,
        'n_samples': 2000,  # For synthetic data
    }
    
    # Initialize trainer
    trainer = EEGModelTrainer(config)
    
    # Load data
    data, emotion_labels, anxiety_labels = trainer.load_data(args.data_path)
    
    # Create data loaders
    train_loader, val_loader, test_loader = trainer.create_data_loaders(
        data, emotion_labels, anxiety_labels
    )
    
    # Train model
    logger.info("Starting training...")
    history = trainer.train(train_loader, val_loader)
    
    # Evaluate on test set
    logger.info("Evaluating on test set...")
    test_results = trainer.evaluate(test_loader)
    
    # Save model and results
    metadata = {
        'config': config,
        'training_history': history,
        'test_results': {
            'emotion_accuracy': test_results['emotion_accuracy'],
            'anxiety_accuracy': test_results['anxiety_accuracy']
        },
        'emotion_classes': trainer.emotion_classes,
        'anxiety_classes': trainer.anxiety_classes,
        'timestamp': datetime.now().isoformat()
    }
    
    trainer.save_model(args.save_path, metadata)
    
    # Plot training curves
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Val Loss')
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 3, 2)
    plt.plot(history['emotion_acc'], label='Emotion Acc')
    plt.title('Emotion Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    
    plt.subplot(1, 3, 3)
    plt.plot(history['anxiety_acc'], label='Anxiety Acc')
    plt.title('Anxiety Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    
    plt.tight_layout()
    plt.savefig('saved_models/training_curves.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info("Training completed successfully")
    logger.info(f"Final emotion accuracy: {test_results['emotion_accuracy']:.3f}")
    logger.info(f"Final anxiety accuracy: {test_results['anxiety_accuracy']:.3f}")

if __name__ == "__main__":
    from datetime import datetime
    main()