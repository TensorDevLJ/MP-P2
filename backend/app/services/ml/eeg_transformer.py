"""
Transformer-based EEG model with self-attention for temporal patterns
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Tuple, Optional
import structlog

logger = structlog.get_logger(__name__)

class EEGTransformer(nn.Module):
    """Transformer model for EEG emotion and anxiety classification"""
    
    def __init__(
        self,
        n_channels: int = 1,
        n_time_points: int = 256,
        n_classes_emotion: int = 5,
        n_classes_anxiety: int = 3,
        d_model: int = 128,
        n_heads: int = 8,
        n_layers: int = 6,
        dropout_rate: float = 0.1
    ):
        super(EEGTransformer, self).__init__()
        
        self.d_model = d_model
        self.n_time_points = n_time_points
        
        # Input projection
        self.input_projection = nn.Linear(n_channels, d_model)
        
        # Positional encoding
        self.positional_encoding = PositionalEncoding(d_model, n_time_points)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model * 4,
            dropout=dropout_rate,
            activation='gelu',
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        
        # Global pooling
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        
        # Classification heads
        self.emotion_classifier = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(d_model // 2, n_classes_emotion)
        )
        
        self.anxiety_classifier = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(d_model // 2, n_classes_anxiety)
        )
        
        # Attention weights for interpretability
        self.attention_weights = None
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass with attention visualization"""
        # x shape: (batch_size, n_channels, n_time_points)
        
        # Transpose for transformer: (batch_size, n_time_points, n_channels)
        x = x.transpose(1, 2)
        
        # Project to model dimension
        x = self.input_projection(x)  # (batch_size, n_time_points, d_model)
        
        # Add positional encoding
        x = self.positional_encoding(x)
        
        # Transformer encoding with attention extraction
        x = self.transformer_encoder(x)
        
        # Extract attention weights from last layer for interpretability
        self.attention_weights = self._extract_attention_weights(x)
        
        # Global pooling
        x = x.transpose(1, 2)  # (batch_size, d_model, n_time_points)
        x = self.global_pool(x).squeeze(-1)  # (batch_size, d_model)
        
        # Classification
        emotion_logits = self.emotion_classifier(x)
        anxiety_logits = self.anxiety_classifier(x)
        
        return emotion_logits, anxiety_logits, self.attention_weights
    
    def _extract_attention_weights(self, x: torch.Tensor) -> torch.Tensor:
        """Extract attention weights for interpretability"""
        # This is a simplified version - in practice, you'd modify the transformer
        # to return attention weights from each layer
        return torch.ones(x.size(0), x.size(1))  # Placeholder

class PositionalEncoding(nn.Module):
    """Positional encoding for transformer"""
    
    def __init__(self, d_model: int, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-np.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        
        self.register_buffer('pe', pe)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:x.size(1), :].transpose(0, 1)

class EEGTransformerInference:
    """Inference wrapper for EEG Transformer model"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = None
        self.emotion_classes = ['happy', 'sad', 'neutral', 'stressed', 'relaxed']
        self.anxiety_classes = ['low', 'moderate', 'high']
        
        self._load_model(model_path)
    
    def _load_model(self, model_path: str):
        """Load trained transformer model"""
        try:
            self.model = EEGTransformer()
            
            # Load state dict if file exists
            try:
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                logger.info("Loaded trained EEG Transformer model", model_path=model_path)
            except FileNotFoundError:
                logger.warning("Model file not found, using untrained model", model_path=model_path)
            
            self.model.to(self.device)
            self.model.eval()
            
        except Exception as e:
            logger.error("Failed to load EEG Transformer model", model_path=model_path, error=str(e))
            raise
    
    def predict(self, eeg_features: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on EEG features with attention visualization"""
        
        try:
            with torch.no_grad():
                # For demonstration, return mock predictions with attention
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
                
                # Mock attention weights for interpretability
                attention_weights = np.random.rand(256)  # Time points
                
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
                    'attention_weights': attention_weights.tolist(),
                    'model_version': '1.0.0-transformer',
                    'model_type': 'transformer'
                }
                
        except Exception as e:
            logger.error("EEG Transformer inference failed", error=str(e))
            raise ValueError(f"EEG Transformer inference failed: {str(e)}")