"""
Signal processing utilities for EEG analysis
"""
import numpy as np
import scipy.signal as signal
from scipy.stats import zscore
from typing import Tuple, Dict, List, Optional
import structlog

logger = structlog.get_logger(__name__)

class SignalProcessor:
    """Advanced signal processing utilities for EEG"""
    
    def __init__(self, sampling_rate: int = 128):
        self.fs = sampling_rate
        self.nyquist = sampling_rate / 2
    
    def apply_bandpass_filter(
        self, 
        data: np.ndarray, 
        low_freq: float = 0.5, 
        high_freq: float = 45,
        filter_order: int = 4
    ) -> np.ndarray:
        """Apply Butterworth bandpass filter"""
        
        try:
            low_norm = low_freq / self.nyquist
            high_norm = high_freq / self.nyquist
            
            # Check frequency bounds
            if low_norm >= 1 or high_norm >= 1:
                raise ValueError(f"Filter frequencies too high for sampling rate {self.fs}")
            
            b, a = signal.butter(filter_order, [low_norm, high_norm], btype='band')
            filtered_data = signal.filtfilt(b, a, data)
            
            return filtered_data
            
        except Exception as e:
            logger.error("Bandpass filtering failed", error=str(e))
            raise
    
    def apply_notch_filter(
        self, 
        data: np.ndarray, 
        notch_freq: float = 50, 
        quality_factor: float = 30
    ) -> np.ndarray:
        """Apply notch filter to remove power line interference"""
        
        try:
            freq_norm = notch_freq / self.nyquist
            
            if freq_norm >= 1:
                logger.warning(f"Notch frequency {notch_freq} too high, skipping")
                return data
            
            b, a = signal.iirnotch(freq_norm, quality_factor)
            filtered_data = signal.filtfilt(b, a, data)
            
            return filtered_data
            
        except Exception as e:
            logger.error("Notch filtering failed", error=str(e))
            return data  # Return original data if filtering fails
    
    def remove_artifacts_ica(self, data: np.ndarray, n_components: int = 5) -> np.ndarray:
        """Remove artifacts using ICA (simplified implementation)"""
        
        try:
            # For production, use MNE-Python's ICA implementation
            # This is a simplified version for demonstration
            
            from sklearn.decomposition import FastICA
            
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            if data.shape[0] < n_components:
                logger.warning("Not enough channels for ICA, skipping artifact removal")
                return data.squeeze()
            
            # Apply ICA
            ica = FastICA(n_components=n_components, random_state=42)
            sources = ica.fit_transform(data.T)
            
            # Simple artifact detection: remove components with extreme kurtosis
            kurtosis_values = [signal.kurtosis(source) for source in sources.T]
            clean_indices = [i for i, k in enumerate(kurtosis_values) if abs(k) < 5]
            
            if not clean_indices:
                logger.warning("All ICA components appear to be artifacts, using original data")
                return data.squeeze()
            
            # Reconstruct with clean components only
            clean_sources = sources[:, clean_indices]
            clean_mixing = ica.components_[clean_indices, :]
            reconstructed = (clean_sources @ clean_mixing).T
            
            return reconstructed.squeeze()
            
        except Exception as e:
            logger.error("ICA artifact removal failed", error=str(e))
            return data.squeeze()  # Return original data
    
    def compute_spectral_features(
        self, 
        data: np.ndarray, 
        nperseg: int = 256
    ) -> Dict[str, float]:
        """Compute comprehensive spectral features"""
        
        try:
            # Power spectral density
            freqs, psd = signal.welch(data, fs=self.fs, nperseg=min(nperseg, len(data)))
            
            # Frequency bands
            bands = {
                'delta': (0.5, 4),
                'theta': (4, 8),
                'alpha': (8, 12),
                'beta': (12, 30),
                'gamma': (30, 45)
            }
            
            features = {}
            
            # Band powers
            for band_name, (low, high) in bands.items():
                idx = np.logical_and(freqs >= low, freqs <= high)
                if np.any(idx):
                    features[f'{band_name}_power'] = np.sum(psd[idx])
                else:
                    features[f'{band_name}_power'] = 0.0
            
            # Relative band powers
            total_power = sum(features[f'{band}_power'] for band in bands.keys())
            if total_power > 0:
                for band in bands.keys():
                    features[f'{band}_relative'] = features[f'{band}_power'] / total_power
            
            # Spectral edge frequency (95% power)
            cumsum_psd = np.cumsum(psd)
            total_power_psd = cumsum_psd[-1]
            edge_idx = np.where(cumsum_psd >= 0.95 * total_power_psd)[0]
            features['spectral_edge'] = freqs[edge_idx[0]] if len(edge_idx) > 0 else freqs[-1]
            
            # Peak frequency
            features['peak_frequency'] = freqs[np.argmax(psd)]
            
            # Spectral entropy
            psd_norm = psd / np.sum(psd)
            spectral_entropy = -np.sum(psd_norm * np.log2(psd_norm + 1e-12))
            features['spectral_entropy'] = spectral_entropy
            
            # Alpha/beta ratio (relaxation indicator)
            if features['alpha_power'] > 0 and features['beta_power'] > 0:
                features['alpha_beta_ratio'] = features['alpha_power'] / features['beta_power']
            else:
                features['alpha_beta_ratio'] = 0.0
            
            # Theta/beta ratio (attention indicator)
            if features['theta_power'] > 0 and features['beta_power'] > 0:
                features['theta_beta_ratio'] = features['theta_power'] / features['beta_power']
            else:
                features['theta_beta_ratio'] = 0.0
            
            return features
            
        except Exception as e:
            logger.error("Spectral feature computation failed", error=str(e))
            # Return default features
            return {f'{band}_power': 0.0 for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']}
    
    def compute_temporal_features(self, data: np.ndarray) -> Dict[str, float]:
        """Compute temporal domain features"""
        
        try:
            features = {}
            
            # Basic statistics
            features['mean'] = float(np.mean(data))
            features['std'] = float(np.std(data))
            features['variance'] = float(np.var(data))
            features['skewness'] = float(signal.skew(data))
            features['kurtosis'] = float(signal.kurtosis(data))
            
            # Hjorth parameters
            features.update(self._compute_hjorth_parameters(data))
            
            # Zero crossing rate
            zero_crossings = np.where(np.diff(np.signbit(data)))[0]
            features['zero_crossing_rate'] = len(zero_crossings) / len(data)
            
            # Mean frequency
            diff_data = np.diff(data)
            if np.var(data) > 0:
                features['mean_frequency'] = np.sqrt(np.var(diff_data) / np.var(data)) * self.fs / (2 * np.pi)
            else:
                features['mean_frequency'] = 0.0
            
            # Complexity measures
            features['sample_entropy'] = self._compute_sample_entropy(data)
            
            return features
            
        except Exception as e:
            logger.error("Temporal feature computation failed", error=str(e))
            return {'mean': 0.0, 'std': 1.0, 'variance': 1.0}
    
    def _compute_hjorth_parameters(self, data: np.ndarray) -> Dict[str, float]:
        """Compute Hjorth parameters (Activity, Mobility, Complexity)"""
        
        try:
            # First and second derivatives
            first_deriv = np.diff(data)
            second_deriv = np.diff(first_deriv)
            
            # Activity (variance)
            activity = np.var(data)
            
            # Mobility
            if activity > 0:
                mobility = np.sqrt(np.var(first_deriv) / activity)
            else:
                mobility = 0.0
            
            # Complexity
            if np.var(first_deriv) > 0 and mobility > 0:
                complexity = np.sqrt(np.var(second_deriv) / np.var(first_deriv)) / mobility
            else:
                complexity = 0.0
            
            return {
                'hjorth_activity': float(activity),
                'hjorth_mobility': float(mobility),
                'hjorth_complexity': float(complexity)
            }
            
        except Exception as e:
            logger.error("Hjorth parameters computation failed", error=str(e))
            return {'hjorth_activity': 0.0, 'hjorth_mobility': 0.0, 'hjorth_complexity': 0.0}
    
    def _compute_sample_entropy(self, data: np.ndarray, m: int = 2, r: float = 0.2) -> float:
        """Compute Sample Entropy as a complexity measure"""
        
        try:
            N = len(data)
            
            def _maxdist(xi, xj, m):
                return max([abs(ua - va) for ua, va in zip(xi, xj)])
            
            def _phi(m):
                patterns = np.array([data[i:i + m] for i in range(N - m + 1)])
                C = np.zeros(N - m + 1)
                
                for i in range(N - m + 1):
                    template = patterns[i]
                    for j in range(N - m + 1):
                        if _maxdist(template, patterns[j], m) <= r * np.std(data):
                            C[i] += 1.0
                
                phi = np.sum(C) / ((N - m + 1) * (N - m))
                return phi
            
            phi_m = _phi(m)
            phi_m1 = _phi(m + 1)
            
            if phi_m1 == 0:
                return 0.0
            
            return -np.log(phi_m1 / phi_m)
            
        except Exception as e:
            logger.error("Sample entropy computation failed", error=str(e))
            return 0.0

def preprocess_eeg_signal(
    data: np.ndarray, 
    sampling_rate: int = 128,
    apply_ica: bool = False
) -> np.ndarray:
    """Complete EEG preprocessing pipeline"""
    
    processor = SignalProcessor(sampling_rate)
    
    # Remove DC offset
    data = data - np.mean(data)
    
    # Bandpass filter
    filtered_data = processor.apply_bandpass_filter(data, 0.5, 45)
    
    # Notch filter for power line noise
    filtered_data = processor.apply_notch_filter(filtered_data, 50)  # EU
    filtered_data = processor.apply_notch_filter(filtered_data, 60)  # US
    
    # ICA artifact removal (if requested and data is suitable)
    if apply_ica and len(data.shape) > 1:
        filtered_data = processor.remove_artifacts_ica(filtered_data)
    
    # Z-score normalization
    filtered_data = zscore(filtered_data)
    
    return filtered_data

def extract_eeg_epochs(
    data: np.ndarray, 
    epoch_length: float, 
    overlap: float, 
    sampling_rate: int
) -> List[np.ndarray]:
    """Extract overlapping epochs from continuous EEG data"""
    
    epoch_samples = int(epoch_length * sampling_rate)
    step_samples = int(epoch_samples * (1 - overlap))
    
    if epoch_samples > len(data):
        logger.warning(f"Epoch length ({epoch_length}s) longer than data ({len(data)/sampling_rate:.1f}s)")
        return [data]
    
    epochs = []
    for start in range(0, len(data) - epoch_samples + 1, step_samples):
        epoch = data[start:start + epoch_samples]
        epochs.append(epoch)
    
    logger.info(f"Extracted {len(epochs)} epochs from {len(data)/sampling_rate:.1f}s of data")
    
    return epochs