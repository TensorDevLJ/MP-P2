"""
Training script for RoBERTa depression classification model
"""
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import pandas as pd
import numpy as np
import json
import os
from typing import Dict, List, Any
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DepressionDataset(Dataset):
    """Dataset for depression classification"""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

class TextModelTrainer:
    """Training pipeline for text depression classification"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Depression severity classes
        self.depression_classes = ['not_depressed', 'moderate', 'severe']
        
        # Initialize tokenizer and model
        model_name = config.get('base_model', 'roberta-base')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(self.depression_classes),
            problem_type="single_label_classification"
        )
        
        logger.info(f"Initialized model: {model_name}")
    
    def load_data(self, data_path: str) -> pd.DataFrame:
        """Load training data"""
        
        logger.info(f"Loading data from {data_path}")
        
        # For demonstration, create synthetic depression dataset
        # In production, use real clinical datasets with proper licensing
        
        synthetic_data = []
        
        # Not depressed examples
        not_depressed_texts = [
            "I had a great day today, feeling positive and energetic",
            "Looking forward to meeting friends this weekend",
            "Work is going well and I feel accomplished",
            "Enjoyed a nice walk in the park, feeling calm",
            "Had a good laugh with my family today"
        ] * 200
        
        # Moderate depression examples
        moderate_texts = [
            "Feeling a bit down lately, not sure why",
            "Having trouble sleeping and feeling tired all the time",
            "Lost interest in things I used to enjoy",
            "Feeling overwhelmed with daily tasks",
            "Having difficulty concentrating at work"
        ] * 200
        
        # Severe depression examples  
        severe_texts = [
            "Everything feels pointless and I have no energy",
            "Can't get out of bed, feeling hopeless about everything",
            "Nothing brings me joy anymore, feeling empty inside",
            "Feel like a burden to everyone around me",
            "Don't see the point in trying anymore"
        ] * 200
        
        # Create dataset
        for texts, label in [
            (not_depressed_texts, 0),
            (moderate_texts, 1), 
            (severe_texts, 2)
        ]:
            for text in texts:
                synthetic_data.append({
                    'text': text,
                    'label': label,
                    'depression_severity': self.depression_classes[label]
                })
        
        df = pd.DataFrame(synthetic_data)
        
        # Shuffle the data
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        logger.info(f"Loaded {len(df)} samples")
        logger.info(f"Class distribution: {df['depression_severity'].value_counts().to_dict()}")
        
        return df
    
    def create_datasets(self, df: pd.DataFrame) -> tuple:
        """Create train/val/test datasets"""
        
        texts = df['text'].tolist()
        labels = df['label'].tolist()
        
        # Split data
        train_texts, temp_texts, train_labels, temp_labels = train_test_split(
            texts, labels, test_size=0.3, random_state=42, stratify=labels
        )
        
        val_texts, test_texts, val_labels, test_labels = train_test_split(
            temp_texts, temp_labels, test_size=0.5, random_state=42, stratify=temp_labels
        )
        
        # Create datasets
        max_length = self.config.get('max_length', 512)
        
        train_dataset = DepressionDataset(train_texts, train_labels, self.tokenizer, max_length)
        val_dataset = DepressionDataset(val_texts, val_labels, self.tokenizer, max_length)
        test_dataset = DepressionDataset(test_texts, test_labels, self.tokenizer, max_length)
        
        return train_dataset, val_dataset, test_dataset
    
    def compute_metrics(self, eval_pred):
        """Compute metrics for evaluation"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='macro')
        accuracy = accuracy_score(labels, predictions)
        
        return {
            'accuracy': accuracy,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    def train(self, train_dataset: Dataset, val_dataset: Dataset) -> Dict[str, Any]:
        """Train the model"""
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir='./saved_models/roberta_depression',
            num_train_epochs=self.config.get('num_epochs', 3),
            per_device_train_batch_size=self.config.get('batch_size', 16),
            per_device_eval_batch_size=self.config.get('batch_size', 16),
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=50,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            greater_is_better=True,
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
        )
        
        # Train model
        logger.info("Starting training...")
        train_result = trainer.train()
        
        # Save model and tokenizer
        trainer.save_model('saved_models/roberta_depression')
        self.tokenizer.save_pretrained('saved_models/roberta_depression')
        
        return train_result
    
    def evaluate(self, test_dataset: Dataset) -> Dict[str, Any]:
        """Evaluate model on test set"""
        
        # Create trainer for evaluation
        trainer = Trainer(
            model=self.model,
            eval_dataset=test_dataset,
            compute_metrics=self.compute_metrics
        )
        
        # Evaluate
        eval_results = trainer.evaluate()
        
        # Detailed classification report
        test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
        predictions = []
        true_labels = []
        
        self.model.eval()
        with torch.no_grad():
            for batch in test_loader:
                inputs = {
                    'input_ids': batch['input_ids'].to(self.device),
                    'attention_mask': batch['attention_mask'].to(self.device)
                }
                
                outputs = self.model(**inputs)
                logits = outputs.logits
                
                preds = torch.argmax(logits, dim=1).cpu().numpy()
                labels = batch['labels'].cpu().numpy()
                
                predictions.extend(preds)
                true_labels.extend(labels)
        
        # Generate detailed report
        detailed_report = classification_report(
            true_labels,
            predictions,
            target_names=self.depression_classes,
            output_dict=True
        )
        
        return {
            'eval_results': eval_results,
            'detailed_report': detailed_report,
            'predictions': predictions,
            'true_labels': true_labels
        }

def main():
    """Main training script"""
    
    parser = argparse.ArgumentParser(description="Train RoBERTa depression classifier")
    parser.add_argument("--data_path", type=str, default="datasets/depression_data.csv")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    parser.add_argument("--max_length", type=int, default=512)
    
    args = parser.parse_args()
    
    # Training configuration
    config = {
        'base_model': 'roberta-base',
        'num_epochs': args.epochs,
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'max_length': args.max_length
    }
    
    # Initialize trainer
    trainer = TextModelTrainer(config)
    
    # Load and prepare data
    df = trainer.load_data(args.data_path)
    train_dataset, val_dataset, test_dataset = trainer.create_datasets(df)
    
    # Train model
    train_result = trainer.train(train_dataset, val_dataset)
    
    # Evaluate on test set
    logger.info("Evaluating on test set...")
    test_results = trainer.evaluate(test_dataset)
    
    # Save evaluation results
    results = {
        'config': config,
        'train_result': train_result.metrics if hasattr(train_result, 'metrics') else {},
        'test_results': test_results,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    with open('saved_models/roberta_depression_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info("Training completed successfully")
    logger.info(f"Test accuracy: {test_results['detailed_report']['accuracy']:.3f}")

if __name__ == "__main__":
    main()