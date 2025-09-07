"""
Model evaluation and performance analysis
"""
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_recall_fscore_support,
    roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import sys

# Add backend to path
sys.path.append('../../backend')
from app.services.ml.eeg_cnn_lstm import EEGModelInference
from app.services.ml.text_classifier import TextClassifier

class ModelEvaluator:
    """Comprehensive model evaluation suite"""
    
    def __init__(self, output_dir: str = "ml_models/evaluation/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def evaluate_eeg_model(
        self, 
        model_path: str,
        test_data: np.ndarray,
        test_labels_emotion: np.ndarray,
        test_labels_anxiety: np.ndarray,
        emotion_classes: List[str],
        anxiety_classes: List[str]
    ) -> Dict[str, Any]:
        """Evaluate EEG model performance"""
        
        print("🧠 Evaluating EEG Model Performance")
        print("=" * 50)
        
        # Load model
        model = EEGModelInference(model_path)
        
        # Run predictions on test data
        emotion_predictions = []
        anxiety_predictions = []
        emotion_probabilities = []
        anxiety_probabilities = []
        
        for i, sample in enumerate(test_data):
            # Convert to features format expected by model
            features = self._convert_to_features(sample)
            
            # Get predictions
            pred = model.predict(features)
            
            # Convert labels to indices
            emotion_pred_idx = emotion_classes.index(pred['emotion']['label'])
            anxiety_pred_idx = anxiety_classes.index(pred['anxiety']['label'])
            
            emotion_predictions.append(emotion_pred_idx)
            anxiety_predictions.append(anxiety_pred_idx)
            
            # Store probabilities for AUC calculation
            emotion_probs = [pred['emotion']['probabilities'][cls] for cls in emotion_classes]
            anxiety_probs = [pred['anxiety']['probabilities'][cls] for cls in anxiety_classes]
            
            emotion_probabilities.append(emotion_probs)
            anxiety_probabilities.append(anxiety_probs)
        
        emotion_predictions = np.array(emotion_predictions)
        anxiety_predictions = np.array(anxiety_predictions)
        emotion_probabilities = np.array(emotion_probabilities)
        anxiety_probabilities = np.array(anxiety_probabilities)
        
        # Calculate metrics
        results = {
            'emotion_metrics': self._calculate_classification_metrics(
                test_labels_emotion, emotion_predictions, emotion_classes,
                emotion_probabilities
            ),
            'anxiety_metrics': self._calculate_classification_metrics(
                test_labels_anxiety, anxiety_predictions, anxiety_classes,
                anxiety_probabilities
            ),
            'model_info': {
                'model_path': model_path,
                'test_samples': len(test_data),
                'emotion_classes': emotion_classes,
                'anxiety_classes': anxiety_classes
            }
        }
        
        # Generate visualizations
        self._plot_confusion_matrices(
            test_labels_emotion, emotion_predictions, emotion_classes,
            test_labels_anxiety, anxiety_predictions, anxiety_classes
        )
        
        self._plot_roc_curves(
            test_labels_emotion, emotion_probabilities, emotion_classes,
            test_labels_anxiety, anxiety_probabilities, anxiety_classes
        )
        
        # Save results
        with open(self.output_dir / "eeg_model_evaluation.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
    
    def evaluate_text_model(
        self,
        test_texts: List[str],
        test_labels: np.ndarray,
        depression_classes: List[str]
    ) -> Dict[str, Any]:
        """Evaluate text classification model"""
        
        print("📝 Evaluating Text Model Performance")
        print("=" * 50)
        
        # Initialize text classifier
        classifier = TextClassifier()
        
        # Run predictions
        predictions = []
        probabilities = []
        
        for text in test_texts:
            result = classifier.analyze_text(text)
            depression = result['depression']
            
            pred_idx = depression_classes.index(depression['label'])
            predictions.append(pred_idx)
            
            probs = [depression['probabilities'][cls] for cls in depression_classes]
            probabilities.append(probs)
        
        predictions = np.array(predictions)
        probabilities = np.array(probabilities)
        
        # Calculate metrics
        results = {
            'depression_metrics': self._calculate_classification_metrics(
                test_labels, predictions, depression_classes, probabilities
            ),
            'model_info': {
                'test_samples': len(test_texts),
                'depression_classes': depression_classes
            }
        }
        
        # Generate visualizations
        self._plot_text_confusion_matrix(test_labels, predictions, depression_classes)
        
        # Save results
        with open(self.output_dir / "text_model_evaluation.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
    
    def _calculate_classification_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray, 
        class_names: List[str],
        y_proba: np.ndarray = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive classification metrics"""
        
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        
        # Per-class metrics
        precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, average=None)
        
        metrics['per_class'] = {}
        for i, class_name in enumerate(class_names):
            metrics['per_class'][class_name] = {
                'precision': float(precision[i]),
                'recall': float(recall[i]),
                'f1_score': float(f1[i]),
                'support': int(support[i])
            }
        
        # Macro and weighted averages
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
        precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        
        metrics['macro_avg'] = {
            'precision': float(precision_macro),
            'recall': float(recall_macro),
            'f1_score': float(f1_macro)
        }
        
        metrics['weighted_avg'] = {
            'precision': float(precision_weighted),
            'recall': float(recall_weighted),
            'f1_score': float(f1_weighted)
        }
        
        # AUC scores (if probabilities provided)
        if y_proba is not None and len(class_names) > 2:
            try:
                # Multi-class AUC
                metrics['auc_ovr'] = float(roc_auc_score(y_true, y_proba, multi_class='ovr', average='macro'))
            except:
                metrics['auc_ovr'] = None
        elif y_proba is not None and len(class_names) == 2:
            metrics['auc'] = float(roc_auc_score(y_true, y_proba[:, 1]))
        
        return metrics
    
    def _plot_confusion_matrices(
        self,
        emotion_true, emotion_pred, emotion_classes,
        anxiety_true, anxiety_pred, anxiety_classes
    ):
        """Plot confusion matrices for EEG model"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Emotion confusion matrix
        emotion_cm = confusion_matrix(emotion_true, emotion_pred)
        sns.heatmap(emotion_cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=emotion_classes, yticklabels=emotion_classes, ax=ax1)
        ax1.set_title('Emotion Classification Confusion Matrix')
        ax1.set_ylabel('True Label')
        ax1.set_xlabel('Predicted Label')
        
        # Anxiety confusion matrix
        anxiety_cm = confusion_matrix(anxiety_true, anxiety_pred)
        sns.heatmap(anxiety_cm, annot=True, fmt='d', cmap='Oranges',
                    xticklabels=anxiety_classes, yticklabels=anxiety_classes, ax=ax2)
        ax2.set_title('Anxiety Classification Confusion Matrix')
        ax2.set_ylabel('True Label')
        ax2.set_xlabel('Predicted Label')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "eeg_confusion_matrices.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def _plot_roc_curves(
        self,
        emotion_true, emotion_proba, emotion_classes,
        anxiety_true, anxiety_proba, anxiety_classes
    ):
        """Plot ROC curves for multi-class classification"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Emotion ROC curves
        for i, class_name in enumerate(emotion_classes):
            y_true_binary = (emotion_true == i).astype(int)
            y_proba_binary = emotion_proba[:, i]
            
            fpr, tpr, _ = roc_curve(y_true_binary, y_proba_binary)
            auc = roc_auc_score(y_true_binary, y_proba_binary)
            
            ax1.plot(fpr, tpr, label=f'{class_name} (AUC = {auc:.3f})')
        
        ax1.plot([0, 1], [0, 1], 'k--', label='Random')
        ax1.set_xlabel('False Positive Rate')
        ax1.set_ylabel('True Positive Rate') 
        ax1.set_title('Emotion Classification ROC Curves')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Anxiety ROC curves
        for i, class_name in enumerate(anxiety_classes):
            y_true_binary = (anxiety_true == i).astype(int)
            y_proba_binary = anxiety_proba[:, i]
            
            fpr, tpr, _ = roc_curve(y_true_binary, y_proba_binary)
            auc = roc_auc_score(y_true_binary, y_proba_binary)
            
            ax2.plot(fpr, tpr, label=f'{class_name} (AUC = {auc:.3f})')
        
        ax2.plot([0, 1], [0, 1], 'k--', label='Random')
        ax2.set_xlabel('False Positive Rate')
        ax2.set_ylabel('True Positive Rate')
        ax2.set_title('Anxiety Classification ROC Curves') 
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "eeg_roc_curves.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def _plot_text_confusion_matrix(self, y_true, y_pred, class_names):
        """Plot confusion matrix for text classification"""
        
        plt.figure(figsize=(8, 6))
        
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                    xticklabels=class_names, yticklabels=class_names)
        
        plt.title('Depression Classification Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "text_confusion_matrix.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def _convert_to_features(self, eeg_sample: np.ndarray) -> Dict[str, Any]:
        """Convert raw EEG sample to feature format for model"""
        
        # Simplified feature conversion for testing
        # In practice, this would use the full feature extraction pipeline
        
        return {
            'features': {
                'band_powers': {
                    'mean': {
                        'delta': 0.15,
                        'theta': 0.25, 
                        'alpha': 0.35,
                        'beta': 0.20,
                        'gamma': 0.05
                    }
                }
            }
        }

def run_comprehensive_evaluation():
    """Run evaluation on all models"""
    
    evaluator = ModelEvaluator()
    
    # Load test data
    data_dir = Path("ml_models/datasets")
    
    try:
        # Load EEG test data
        emotion_data = np.load(data_dir / "synthetic_eeg_emotion_data.npy")
        emotion_labels = np.load(data_dir / "synthetic_eeg_emotion_labels.npy")
        anxiety_data = np.load(data_dir / "synthetic_eeg_anxiety_data.npy") 
        anxiety_labels = np.load(data_dir / "synthetic_eeg_anxiety_labels.npy")
        
        with open(data_dir / "emotion_classes.json") as f:
            emotion_classes = json.load(f)
        with open(data_dir / "anxiety_classes.json") as f:
            anxiety_classes = json.load(f)
        
        # Evaluate EEG model
        eeg_results = evaluator.evaluate_eeg_model(
            model_path="ml_models/saved_models/eeg_cnn_lstm.pth",
            test_data=emotion_data[-100:],  # Last 100 samples as test set
            test_labels_emotion=emotion_labels[-100:],
            test_labels_anxiety=anxiety_labels[-100:],
            emotion_classes=emotion_classes,
            anxiety_classes=anxiety_classes
        )
        
        print(f"EEG Model Results:")
        print(f"  Emotion Accuracy: {eeg_results['emotion_metrics']['accuracy']:.3f}")
        print(f"  Anxiety Accuracy: {eeg_results['anxiety_metrics']['accuracy']:.3f}")
        
    except FileNotFoundError:
        print("⚠️ EEG test data not found, skipping EEG evaluation")
        eeg_results = None
    
    try:
        # Load text test data
        text_df = pd.read_csv(data_dir / "synthetic_depression_text.csv")
        
        # Use last 20% as test set
        test_size = int(len(text_df) * 0.2)
        test_df = text_df.tail(test_size)
        
        # Evaluate text model
        text_results = evaluator.evaluate_text_model(
            test_texts=test_df['text'].tolist(),
            test_labels=test_df['label'].values,
            depression_classes=['not_depressed', 'moderate', 'severe']
        )
        
        print(f"Text Model Results:")
        print(f"  Depression Accuracy: {text_results['depression_metrics']['accuracy']:.3f}")
        
    except FileNotFoundError:
        print("⚠️ Text test data not found, skipping text evaluation")
        text_results = None
    
    # Generate summary report
    summary = {
        'evaluation_date': pd.Timestamp.now().isoformat(),
        'eeg_results': eeg_results,
        'text_results': text_results
    }
    
    with open(evaluator.output_dir / "evaluation_summary.json", 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"\n✅ Evaluation completed! Reports saved to {evaluator.output_dir}")
    
    return summary

if __name__ == "__main__":
    run_comprehensive_evaluation()