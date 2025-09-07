"""
CNN-LSTM model for EEG emotion and anxiety classification
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Tuple, Optional
import structlog

logger = structlog.get_logger(__name__)

class EEGCNNLSTM(nn.Module):
    """CNN-LSTM hybrid model for EEG classification"""
    
    def __init__(
        self,
        n_channels: int = 1,
        n_time_points: int = 256,
        n_classes_emotion: int = 5,
        n_classes_anxiety: int = 3,
        cnn_filters: List[int] = [32, 64, 128],
        lstm_hidden: int = 128,
        dropout_rate: float = 0.5
    ):
        super(EEGCNNLSTM, self).__init__()
        
        self.n_classes_emotion = n_classes_emotion
        self.n_classes_anxiety = n_classes_anxiety
        
        # CNN layers for spatial feature extraction
        self.conv1 = nn.Conv1d(n_channels, cnn_filters[0], kernel_size=7, padding=3)
        self.conv2 = nn.Conv1d(cnn_filters[0], cnn_filters[1], kernel_size=5, padding=2)
        self.conv3 = nn.Conv1d(cnn_filters[1], cnn_filters[2], kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2)
        self.dropout = nn.Dropout(dropout_rate)
        
        # Calculate LSTM input size after CNN layers
        # Assuming 3 pooling operations: time_points / 8
        lstm_input_size = cnn_filters[2]
        self.lstm_time_steps = n_time_points // 8
        
        # LSTM for temporal dynamics
        self.lstm = nn.LSTM(
            input_size=lstm_input_size,
            hidden_size=lstm_hidden,
            num_layers=2,
            batch_first=True,
            dropout=dropout_rate,
            bidirectional=True
        )
        
        # Classification heads
        lstm_output_size = lstm_hidden * 2  # Bidirectional
        
        self.emotion_classifier = nn.Sequential(
            nn.Linear(lstm_output_size, lstm_hidden),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(lstm_hidden, n_classes_emotion)
        )
        
        self.anxiety_classifier = nn.Sequential(
            nn.Linear(lstm_output_size, lstm_hidden),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(lstm_hidden, n_classes_anxiety)
        )
        
        # Attention mechanism for interpretability
        self.attention = nn.Sequential(
            nn.Linear(lstm_output_size, lstm_hidden),
            nn.Tanh(),
            nn.Linear(lstm_hidden, 1),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass returning emotion, anxiety predictions and attention weights"""
        
        # CNN feature extraction
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = self.dropout(x)
        
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = self.dropout(x)
        
        x = F.relu(self.conv3(x))
        x = self.pool(x)
        x = self.dropout(x)
        
        # Reshape for LSTM: (batch, time_steps, features)
        batch_size = x.size(0)
        x = x.transpose(1, 2)  # (batch, time_steps, features)
        
        # LSTM temporal modeling
        lstm_out, _ = self.lstm(x)
        
        # Attention-weighted pooling
        attention_weights = self.attention(lstm_out)
        weighted_lstm_out = torch.sum(lstm_out * attention_weights, dim=1)
        
        # Classification
        emotion_logits = self.emotion_classifier(weighted_lstm_out)
        anxiety_logits = self.anxiety_classifier(weighted_lstm_out)
        
        return emotion_logits, anxiety_logits, attention_weights

class EEGModelInference:
    """Model inference wrapper for production use"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = None
        self.emotion_classes = ['happy', 'sad', 'neutral', 'stressed', 'relaxed']
        self.anxiety_classes = ['low', 'moderate', 'high']
        
        self._load_model(model_path)
    
    def _load_model(self, model_path: str):
        """Load trained model"""
        try:
            # For development, create a dummy model
            # In production, load actual trained weights
            self.model = EEGCNNLSTM()
            
            # Load state dict if file exists
            try:
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                logger.info("Loaded trained EEG model", model_path=model_path)
            except FileNotFoundError:
                logger.warning("Model file not found, using untrained model", model_path=model_path)
            
            self.model.to(self.device)
            self.model.eval()
            
        except Exception as e:
            logger.error("Failed to load EEG model", model_path=model_path, error=str(e))
            raise
    
    def predict(self, eeg_features: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on EEG features"""
        
        try:
            with torch.no_grad():
                # For demonstration, return mock predictions
                # In production, process features and run through model
                
                # Mock emotion prediction
                emotion_probs = np.random.dirichlet([1] * len(self.emotion_classes))
                emotion_label = self.emotion_classes[np.argmax(emotion_probs)]
                
                # Mock anxiety prediction  
                anxiety_probs = np.random.dirichlet([1] * len(self.anxiety_classes))
                anxiety_label = self.anxiety_classes[np.argmax(anxiety_probs)]
                
                # Calculate confidence as max probability
                emotion_confidence = float(np.max(emotion_probs))
                anxiety_confidence = float(np.max(anxiety_probs))
                
                return {
                    'emotion': {
                        'label': emotion_label,
                        'probabilities': {
                            cls: float(prob) 
                            for cls, prob in zip(self.emotion_classes, emotion_probs)
                        },
                        'confidence': emotion_confidence
                    },
                    'anxiety': {
                        'label': anxiety_label,
                        'probabilities': {
                            cls: float(prob) 
                            for cls, prob in zip(self.anxiety_classes, anxiety_probs)
                        },
                        'confidence': anxiety_confidence
                    },
                    'model_version': '1.0.0-demo'
                }
                
        except Exception as e:
            logger.error("EEG inference failed", error=str(e))
            raise ValueError(f"EEG inference failed: {str(e)}")