import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fft, fftfreq
import mne
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
from typing import Dict, List, Tuple, Optional
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

class EEGProcessor:
    def __init__(self):
        self.sampling_rates = [128, 256, 512, 1000]
        self.bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30),
            'gamma': (30, 45)
        }
        self.scaler = StandardScaler()
        
    def validate_eeg_data(self, data: pd.DataFrame) -> Dict:
        """Validate EEG data format and quality"""
        validation_result = {
            'valid': True,
            'messages': [],
            'detected_sr': None,
            'channels': [],
            'duration': 0
        }
        
        try:
            # Detect sampling rate from column names
            for col in data.columns:
                for sr in self.sampling_rates:
                    if str(sr) in col:
                        validation_result['detected_sr'] = sr
                        break
                        
            # Default to 128 if not detected
            if not validation_result['detected_sr']:
                validation_result['detected_sr'] = 128
                validation_result['messages'].append("Sampling rate not detected, defaulting to 128 Hz")
            
            # Identify EEG channels
            eeg_cols = [col for col in data.columns if 'eeg' in col.lower() or 'af' in col.lower() or 'fp' in col.lower()]
            validation_result['channels'] = eeg_cols
            
            if not eeg_cols:
                validation_result['valid'] = False
                validation_result['messages'].append("No EEG channels detected")
                return validation_result
            
            # Check duration (minimum 2 seconds)
            duration = len(data) / validation_result['detected_sr']
            validation_result['duration'] = duration
            
            if duration < 2:
                validation_result['valid'] = False
                validation_result['messages'].append(f"Recording too short: {duration:.1f}s (minimum 2s required)")
            
            # Check for missing values
            if data[eeg_cols].isnull().any().any():
                validation_result['messages'].append("Missing values detected, will be interpolated")
                
        except Exception as e:
            validation_result['valid'] = False
            validation_result['messages'].append(f"Validation error: {str(e)}")
            
        return validation_result
    
    def preprocess_eeg(self, data: pd.DataFrame, sr: int = 128, channel: str = None) -> np.ndarray:
        """Preprocess EEG signals"""
        # Select channel
        if channel and channel in data.columns:
            eeg_data = data[channel].values
        else:
            # Use first EEG channel found
            eeg_cols = [col for col in data.columns if 'eeg' in col.lower()]
            if eeg_cols:
                eeg_data = data[eeg_cols[0]].values
            else:
                raise ValueError("No EEG channels found")
        
        # Handle missing values
        eeg_data = pd.Series(eeg_data).interpolate().fillna(0).values
        
        # Bandpass filter (0.5-45 Hz)
        nyquist = sr / 2
        low_freq = 0.5 / nyquist
        high_freq = 45 / nyquist
        
        if high_freq >= 1.0:
            high_freq = 0.99
            
        b, a = signal.butter(4, [low_freq, high_freq], btype='band')
        filtered_data = signal.filtfilt(b, a, eeg_data)
        
        # Notch filter for power line interference
        notch_freq = 50  # or 60 for US
        Q = 30  # Quality factor
        b_notch, a_notch = signal.iirnotch(notch_freq, Q, sr)
        filtered_data = signal.filtfilt(b_notch, a_notch, filtered_data)
        
        return filtered_data
    
    def extract_band_powers(self, eeg_data: np.ndarray, sr: int = 128, epoch_length: int = 4) -> Dict:
        """Extract band powers using Welch's method"""
        epoch_samples = epoch_length * sr
        overlap_samples = epoch_samples // 2
        
        bands_data = {
            'times': [],
            'bands_timeseries': {band: [] for band in self.bands.keys()},
            'bands_per_epoch': []
        }
        
        # Create epochs
        for start in range(0, len(eeg_data) - epoch_samples + 1, overlap_samples):
            end = start + epoch_samples
            epoch = eeg_data[start:end]
            
            # Calculate PSD using Welch's method
            freqs, psd = signal.welch(epoch, sr, nperseg=min(len(epoch), sr))
            
            # Extract band powers
            epoch_bands = {}
            start_time = start / sr
            end_time = end / sr
            
            for band_name, (low_freq, high_freq) in self.bands.items():
                freq_mask = (freqs >= low_freq) & (freqs <= high_freq)
                band_power = np.trapz(psd[freq_mask], freqs[freq_mask])
                epoch_bands[band_name] = float(band_power)
                bands_data['bands_timeseries'][band_name].append(band_power)
            
            bands_data['times'].append(start_time)
            bands_data['bands_per_epoch'].append({
                'start_time': start_time,
                'end_time': end_time,
                **epoch_bands
            })
        
        return bands_data
    
    def compute_spectrograms(self, eeg_data: np.ndarray, sr: int = 128) -> Dict:
        """Compute spectrogram for visualization"""
        nperseg = min(sr * 2, len(eeg_data) // 8)  # 2-second windows
        
        freqs, times, Sxx = signal.spectrogram(
            eeg_data, sr, 
            nperseg=nperseg,
            noverlap=nperseg//2,
            scaling='density'
        )
        
        # Convert to dB
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        
        return {
            'freqs': freqs.tolist(),
            'times': times.tolist(),
            'power_db': Sxx_db.tolist()
        }
    
    def generate_visualizations(self, bands_data: Dict, spectrogram_data: Dict) -> Dict:
        """Generate base64 encoded visualization images"""
        plt.style.use('seaborn-v0_8-darkgrid')
        visualizations = {}
        
        # Band powers time series
        fig, ax = plt.subplots(figsize=(12, 6))
        times = bands_data['times']
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        for i, (band_name, powers) in enumerate(bands_data['bands_timeseries'].items()):
            ax.plot(times, powers, label=band_name.title(), color=colors[i], linewidth=2)
        
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Power (µV²)')
        ax.set_title('EEG Band Powers Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Save as base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        bands_image = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Spectrogram
        fig, ax = plt.subplots(figsize=(12, 6))
        freqs = np.array(spectrogram_data['freqs'])
        times = np.array(spectrogram_data['times'])
        power_db = np.array(spectrogram_data['power_db'])
        
        im = ax.pcolormesh(times, freqs, power_db, shading='gouraud', cmap='viridis')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title('EEG Spectrogram')
        ax.set_ylim(0, 45)  # Focus on relevant frequencies
        plt.colorbar(im, ax=ax, label='Power (dB)')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        spectrogram_image = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            'bands_chart': bands_image,
            'spectrogram': spectrogram_image
        }

class EEGCNNLSTMModel(nn.Module):
    """CNN-LSTM model for EEG emotion classification"""
    
    def __init__(self, input_channels=1, sequence_length=512, num_classes=5):
        super(EEGCNNLSTMModel, self).__init__()
        
        # CNN layers for spatial feature extraction
        self.conv1 = nn.Conv1d(input_channels, 32, kernel_size=5, padding=2)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=5, padding=2)
        self.conv3 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        
        # Batch normalization and dropout
        self.bn1 = nn.BatchNorm1d(32)
        self.bn2 = nn.BatchNorm1d(64)
        self.bn3 = nn.BatchNorm1d(128)
        self.dropout1 = nn.Dropout(0.3)
        self.dropout2 = nn.Dropout(0.4)
        
        # LSTM for temporal modeling
        self.lstm = nn.LSTM(128, 64, batch_first=True, bidirectional=True)
        self.lstm_dropout = nn.Dropout(0.5)
        
        # Classification head
        self.fc1 = nn.Linear(128, 64)  # 64*2 for bidirectional
        self.fc2 = nn.Linear(64, num_classes)
        
        # Activation functions
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        # CNN feature extraction
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.dropout1(x)
        x = nn.MaxPool1d(2)(x)
        
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.dropout1(x)
        x = nn.MaxPool1d(2)(x)
        
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.dropout2(x)
        x = nn.MaxPool1d(2)(x)
        
        # Reshape for LSTM (batch, sequence, features)
        x = x.transpose(1, 2)
        
        # LSTM processing
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        # Use last LSTM output
        x = lstm_out[:, -1, :]
        x = self.lstm_dropout(x)
        
        # Classification
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        
        return self.softmax(x)

class EEGModelInference:
    def __init__(self, model_path: str = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = EEGCNNLSTMModel()
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        
        self.model.to(self.device)
        self.model.eval()
        
        self.emotion_labels = ['happy', 'sad', 'angry', 'relaxed', 'stressed']
        self.anxiety_labels = ['low', 'moderate', 'high']
    
    def predict_emotion(self, eeg_features: np.ndarray) -> Dict:
        """Predict emotion from EEG features"""
        try:
            # Prepare input tensor
            input_tensor = torch.FloatTensor(eeg_features).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = outputs.cpu().numpy()[0]
            
            # Get prediction
            predicted_class = np.argmax(probabilities)
            
            return {
                'label': self.emotion_labels[predicted_class],
                'confidence': float(probabilities[predicted_class]),
                'probabilities': {
                    label: float(prob) for label, prob in 
                    zip(self.emotion_labels, probabilities)
                }
            }
        except Exception as e:
            return {
                'label': 'unknown',
                'confidence': 0.0,
                'probabilities': {label: 0.2 for label in self.emotion_labels},
                'error': str(e)
            }
    
    def assess_anxiety(self, band_powers: Dict) -> Dict:
        """Assess anxiety level from band power features"""
        try:
            # Simple rule-based anxiety assessment
            # In production, this would use a trained model
            
            alpha_power = np.mean([epoch['alpha'] for epoch in band_powers['bands_per_epoch']])
            beta_power = np.mean([epoch['beta'] for epoch in band_powers['bands_per_epoch']])
            
            # Anxiety indicators: low alpha, high beta
            alpha_ratio = alpha_power / (alpha_power + beta_power)
            
            if alpha_ratio < 0.3:
                anxiety_level = 'high'
                confidence = 0.8
            elif alpha_ratio < 0.5:
                anxiety_level = 'moderate'
                confidence = 0.7
            else:
                anxiety_level = 'low'
                confidence = 0.75
            
            return {
                'label': anxiety_level,
                'confidence': confidence,
                'score': 1.0 - alpha_ratio,
                'indicators': {
                    'alpha_suppression': alpha_power < 0.1,
                    'beta_elevation': beta_power > 0.2,
                    'alpha_beta_ratio': alpha_ratio
                }
            }
        except Exception as e:
            return {
                'label': 'unknown',
                'confidence': 0.0,
                'score': 0.0,
                'error': str(e)
            }