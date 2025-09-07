"""
EEG signal processing pipeline using MNE-Python
"""
import numpy as np
import pandas as pd
import mne
from scipy import signal
from scipy.stats import entropy
import pywt
from typing import Dict, List, Tuple, Any, Optional
import structlog
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import io
import base64

logger = structlog.get_logger(__name__)

class EEGProcessor:
    """Production-ready EEG signal processing pipeline"""
    
    def __init__(self, sampling_rate: int = 128):
        self.sampling_rate = sampling_rate
        self.frequency_bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 12),
            'beta': (12, 30),
            'gamma': (30, 45)
        }
        
    async def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract basic metadata from EEG file"""
        try:
            # Read first few lines to detect format
            df = pd.read_csv(file_path, nrows=10)
            
            # Detect sampling rate from header or estimate from timestamps
            sampling_rate = self._detect_sampling_rate(df)
            
            # Detect channels (exclude time/timestamp columns)
            time_cols = ['time', 'timestamp', 'Time', 'Timestamp']
            channels = [col for col in df.columns if col not in time_cols]
            
            # Estimate duration
            total_rows = len(pd.read_csv(file_path))
            duration = total_rows / sampling_rate if sampling_rate else None
            
            return {
                "sampling_rate": sampling_rate,
                "channels": channels,
                "duration_seconds": duration,
                "total_samples": total_rows
            }
            
        except Exception as e:
            logger.error("Metadata extraction failed", file_path=file_path, error=str(e))
            raise ValueError(f"Failed to extract metadata: {str(e)}")
    
    def _detect_sampling_rate(self, df: pd.DataFrame) -> Optional[int]:
        """Detect sampling rate from data"""
        # Try to find in column names
        for col in df.columns:
            if 'hz' in col.lower() or 'rate' in col.lower():
                try:
                    return int(df[col].iloc[0])
                except:
                    continue
        
        # Try common sampling rates
        common_rates = [128, 256, 512, 1000]
        return common_rates[0]  # Default fallback
    
    async def process_eeg_data(
        self, 
        file_path: str, 
        channel: str = "EEG.AF3",
        epoch_length: float = 2.0,
        overlap: float = 0.5
    ) -> Dict[str, Any]:
        """Main EEG processing pipeline"""
        
        logger.info("Starting EEG processing", file_path=file_path, channel=channel)
        
        try:
            # Load data
            raw_data = self._load_eeg_data(file_path, channel)
            
            # Preprocessing
            filtered_data = self._preprocess_signal(raw_data)
            
            # Epoching
            epochs = self._create_epochs(filtered_data, epoch_length, overlap)
            
            # Feature extraction
            features = self._extract_features(epochs)
            
            # Generate visualizations
            charts_data = self._generate_charts(filtered_data, epochs, features)
            
            logger.info("EEG processing completed", 
                       n_epochs=len(epochs), 
                       n_features=len(features))
            
            return {
                "features": features,
                "charts": charts_data,
                "metadata": {
                    "n_epochs": len(epochs),
                    "epoch_length": epoch_length,
                    "sampling_rate": self.sampling_rate,
                    "channel": channel
                }
            }
            
        except Exception as e:
            logger.error("EEG processing failed", file_path=file_path, error=str(e))
            raise ValueError(f"EEG processing failed: {str(e)}")
    
    def _load_eeg_data(self, file_path: str, channel: str) -> np.ndarray:
        """Load EEG data from file"""
        try:
            df = pd.read_csv(file_path)
            
            if channel not in df.columns:
                # Try to find similar channel name
                similar_cols = [col for col in df.columns if channel.split('.')[-1] in col]
                if similar_cols:
                    channel = similar_cols[0]
                else:
                    # Use first non-time column
                    time_cols = ['time', 'timestamp', 'Time', 'Timestamp']
                    data_cols = [col for col in df.columns if col not in time_cols]
                    if data_cols:
                        channel = data_cols[0]
                    else:
                        raise ValueError("No data channels found")
            
            data = df[channel].values.astype(np.float64)
            
            # Remove NaN values
            data = data[~np.isnan(data)]
            
            if len(data) < self.sampling_rate * 2:  # Minimum 2 seconds
                raise ValueError("Insufficient data length")
            
            return data
            
        except Exception as e:
            logger.error("Data loading failed", file_path=file_path, error=str(e))
            raise
    
    def _preprocess_signal(self, data: np.ndarray) -> np.ndarray:
        """Preprocess EEG signal with filtering"""
        
        # Band-pass filter (0.5-45 Hz)
        nyquist = self.sampling_rate / 2
        low_freq = 0.5 / nyquist
        high_freq = 45 / nyquist
        
        # Butterworth filter
        b, a = signal.butter(4, [low_freq, high_freq], btype='band')
        filtered = signal.filtfilt(b, a, data)
        
        # Notch filter for power line noise (50/60 Hz)
        notch_freq = 50 / nyquist  # Adjust based on region
        b_notch, a_notch = signal.iirnotch(notch_freq, Q=30)
        filtered = signal.filtfilt(b_notch, a_notch, filtered)
        
        # Z-score normalization
        filtered = (filtered - np.mean(filtered)) / np.std(filtered)
        
        return filtered
    
    def _create_epochs(self, data: np.ndarray, epoch_length: float, overlap: float) -> List[np.ndarray]:
        """Create epochs from continuous data"""
        epoch_samples = int(epoch_length * self.sampling_rate)
        step_samples = int(epoch_samples * (1 - overlap))
        
        epochs = []
        for start in range(0, len(data) - epoch_samples + 1, step_samples):
            epoch = data[start:start + epoch_samples]
            epochs.append(epoch)
        
        return epochs
    
    def _extract_features(self, epochs: List[np.ndarray]) -> Dict[str, Any]:
        """Extract comprehensive features from epochs"""
        
        all_band_powers = []
        all_spectral_features = []
        all_temporal_features = []
        
        for epoch in epochs:
            # Band power features
            band_powers = self._compute_band_powers(epoch)
            all_band_powers.append(band_powers)
            
            # Spectral features
            spectral_features = self._compute_spectral_features(epoch)
            all_spectral_features.append(spectral_features)
            
            # Temporal features
            temporal_features = self._compute_temporal_features(epoch)
            all_temporal_features.append(temporal_features)
        
        # Aggregate features across epochs
        features = {
            'band_powers': {
                'per_epoch': all_band_powers,
                'mean': {band: np.mean([bp[band] for bp in all_band_powers]) 
                        for band in self.frequency_bands.keys()},
                'std': {band: np.std([bp[band] for bp in all_band_powers]) 
                       for band in self.frequency_bands.keys()}
            },
            'spectral_features': {
                'per_epoch': all_spectral_features,
                'mean': {key: np.mean([sf[key] for sf in all_spectral_features]) 
                        for key in all_spectral_features[0].keys()},
            },
            'temporal_features': {
                'per_epoch': all_temporal_features,
                'mean': {key: np.mean([tf[key] for tf in all_temporal_features]) 
                        for key in all_temporal_features[0].keys()},
            }
        }
        
        return features
    
    def _compute_band_powers(self, epoch: np.ndarray) -> Dict[str, float]:
        """Compute power spectral density for frequency bands"""
        freqs, psd = signal.welch(epoch, fs=self.sampling_rate, nperseg=min(256, len(epoch)))
        
        band_powers = {}
        for band_name, (low_freq, high_freq) in self.frequency_bands.items():
            idx = np.logical_and(freqs >= low_freq, freqs <= high_freq)
            band_power = np.sum(psd[idx])
            band_powers[band_name] = float(band_power)
        
        return band_powers
    
    def _compute_spectral_features(self, epoch: np.ndarray) -> Dict[str, float]:
        """Compute spectral features beyond band powers"""
        freqs, psd = signal.welch(epoch, fs=self.sampling_rate)
        
        # Spectral entropy
        psd_norm = psd / np.sum(psd)
        spectral_entropy = entropy(psd_norm)
        
        # Peak frequency
        peak_freq = freqs[np.argmax(psd)]
        
        # Spectral edge frequency (95% power)
        cumsum_psd = np.cumsum(psd)
        total_power = cumsum_psd[-1]
        edge_freq_idx = np.where(cumsum_psd >= 0.95 * total_power)[0][0]
        edge_freq = freqs[edge_freq_idx]
        
        return {
            'spectral_entropy': float(spectral_entropy),
            'peak_frequency': float(peak_freq),
            'spectral_edge_freq': float(edge_freq),
            'total_power': float(np.sum(psd))
        }
    
    def _compute_temporal_features(self, epoch: np.ndarray) -> Dict[str, float]:
        """Compute temporal domain features (Hjorth parameters)"""
        
        # First and second derivatives
        first_deriv = np.diff(epoch)
        second_deriv = np.diff(first_deriv)
        
        # Hjorth Activity (variance)
        activity = np.var(epoch)
        
        # Hjorth Mobility
        mobility = np.sqrt(np.var(first_deriv) / np.var(epoch))
        
        # Hjorth Complexity
        complexity = np.sqrt(np.var(second_deriv) / np.var(first_deriv)) / mobility
        
        # Zero crossing rate
        zero_crossings = len(np.where(np.diff(np.signbit(epoch)))[0])
        zcr = zero_crossings / len(epoch)
        
        return {
            'hjorth_activity': float(activity),
            'hjorth_mobility': float(mobility),
            'hjorth_complexity': float(complexity),
            'zero_crossing_rate': float(zcr),
            'variance': float(np.var(epoch)),
            'skewness': float(signal.skew(epoch)),
            'kurtosis': float(signal.kurtosis(epoch))
        }
    
    def _generate_charts(self, data: np.ndarray, epochs: List[np.ndarray], features: Dict) -> Dict[str, Any]:
        """Generate chart data for visualization"""
        
        # Time series for band powers
        times = np.arange(len(epochs)) * (len(epochs[0]) / self.sampling_rate)
        band_timeseries = {
            band: [features['band_powers']['per_epoch'][i][band] for i in range(len(epochs))]
            for band in self.frequency_bands.keys()
        }
        
        # Power spectral density
        freqs, psd_avg = signal.welch(data, fs=self.sampling_rate)
        
        # Spectrogram
        f_spec, t_spec, Sxx = signal.spectrogram(
            data, 
            fs=self.sampling_rate, 
            nperseg=256,
            noverlap=128
        )
        
        # Convert spectrogram to base64 image
        plt.figure(figsize=(12, 6))
        plt.pcolormesh(t_spec, f_spec, 10 * np.log10(Sxx), shading='gouraud')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        plt.title('EEG Spectrogram')
        plt.colorbar(label='Power [dB]')
        plt.ylim([0.5, 45])
        
        # Save plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        spectrogram_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            "bands_timeseries": {
                "times": times.tolist(),
                "data": band_timeseries
            },
            "psd": {
                "frequencies": freqs.tolist(),
                "power": psd_avg.tolist()
            },
            "spectrogram_base64": spectrogram_b64,
            "spectrogram_extent": [t_spec.min(), t_spec.max(), f_spec.min(), f_spec.max()]
        }