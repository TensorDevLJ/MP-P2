"""
Jupyter notebook equivalent for EEG analysis demonstration
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal
import mne
from pathlib import Path
import sys

# Add backend to path
sys.path.append('../../backend')
from app.services.ml.eeg_processor import EEGProcessor
from app.utils.signal_processing import SignalProcessor, preprocess_eeg_signal

def demonstrate_eeg_pipeline():
    """Demonstrate the complete EEG processing pipeline"""
    
    print("EEG Mental Health Analysis Pipeline Demo")
    print("=" * 50)
    
    # Generate synthetic EEG data for demonstration
    print("\n1. Generating synthetic EEG data...")
    fs = 128  # Sampling rate
    duration = 30  # 30 seconds
    t = np.linspace(0, duration, fs * duration)
    
    # Create multi-component signal
    eeg_signal = (
        0.5 * np.sin(2 * np.pi * 10 * t) +      # Alpha (10 Hz)
        0.3 * np.sin(2 * np.pi * 6 * t) +       # Theta (6 Hz)
        0.2 * np.sin(2 * np.pi * 20 * t) +      # Beta (20 Hz)
        0.1 * np.random.randn(len(t))           # Noise
    )
    
    # Add some artifacts
    eeg_signal[1000:1100] += 5  # Artifact burst
    eeg_signal += 0.05 * np.sin(2 * np.pi * 50 * t)  # Power line noise
    
    print(f"Generated {duration}s of EEG data at {fs} Hz")
    
    # 2. Preprocessing
    print("\n2. Applying preprocessing...")
    processed_signal = preprocess_eeg_signal(eeg_signal, fs)
    
    # 3. Feature extraction
    print("\n3. Extracting features...")
    processor = SignalProcessor(fs)
    
    # Spectral features
    spectral_features = processor.compute_spectral_features(processed_signal)
    print("Spectral features extracted:")
    for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
        power = spectral_features.get(f'{band}_power', 0)
        print(f"  {band.capitalize()}: {power:.4f} μV²")
    
    # Temporal features
    temporal_features = processor.compute_temporal_features(processed_signal)
    print(f"\nTemporal features:")
    print(f"  Hjorth Activity: {temporal_features['hjorth_activity']:.4f}")
    print(f"  Hjorth Mobility: {temporal_features['hjorth_mobility']:.4f}")
    print(f"  Hjorth Complexity: {temporal_features['hjorth_complexity']:.4f}")
    
    # 4. Visualization
    print("\n4. Generating visualizations...")
    
    # Time domain plot
    plt.figure(figsize=(15, 10))
    
    plt.subplot(3, 2, 1)
    plt.plot(t[:fs*5], eeg_signal[:fs*5], 'b-', alpha=0.7, linewidth=1)
    plt.title('Raw EEG Signal (first 5s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (μV)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(3, 2, 2)
    plt.plot(t[:fs*5], processed_signal[:fs*5], 'g-', alpha=0.7, linewidth=1)
    plt.title('Preprocessed EEG Signal (first 5s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (μV)')
    plt.grid(True, alpha=0.3)
    
    # Power spectral density
    plt.subplot(3, 2, 3)
    freqs, psd = signal.welch(processed_signal, fs=fs, nperseg=256)
    plt.semilogy(freqs, psd, 'b-', linewidth=2)
    plt.title('Power Spectral Density')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power (μV²/Hz)')
    plt.xlim([0.5, 45])
    plt.grid(True, alpha=0.3)
    
    # Band powers bar plot
    plt.subplot(3, 2, 4)
    bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']
    powers = [spectral_features.get(f'{band}_power', 0) for band in bands]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    plt.bar(bands, powers, color=colors, alpha=0.7)
    plt.title('Frequency Band Powers')
    plt.ylabel('Power (μV²)')
    plt.xticks(rotation=45)
    
    # Spectrogram
    plt.subplot(3, 1, 3)
    f, t_spec, Sxx = signal.spectrogram(processed_signal, fs, nperseg=256, noverlap=128)
    plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.colorbar(label='Power (dB)')
    plt.title('EEG Spectrogram')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.ylim([0.5, 45])
    
    plt.tight_layout()
    plt.savefig('ml_models/notebooks/eeg_demo_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\nDemo completed! Visualization saved as 'eeg_demo_analysis.png'")
    
    return {
        'spectral_features': spectral_features,
        'temporal_features': temporal_features,
        'processed_signal': processed_signal,
        'raw_signal': eeg_signal
    }

def demonstrate_model_prediction():
    """Demonstrate model prediction on sample data"""
    
    print("\n" + "=" * 50)
    print("Model Prediction Demo")
    print("=" * 50)
    
    # Import model
    from app.services.ml.eeg_cnn_lstm import EEGModelInference
    
    # Initialize model (using demo weights)
    model = EEGModelInference('../../backend/saved_models/eeg_cnn_lstm.pth')
    
    # Create sample features
    sample_features = {
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
    
    # Run prediction
    predictions = model.predict(sample_features)
    
    print("\nPrediction Results:")
    print(f"Emotion: {predictions['emotion']['label']} ({predictions['emotion']['confidence']:.2f} confidence)")
    print(f"Anxiety: {predictions['anxiety']['label']} ({predictions['anxiety']['confidence']:.2f} confidence)")
    
    print("\nEmotion probabilities:")
    for emotion, prob in predictions['emotion']['probabilities'].items():
        print(f"  {emotion}: {prob:.3f}")
    
    print("\nAnxiety probabilities:")
    for level, prob in predictions['anxiety']['probabilities'].items():
        print(f"  {level}: {prob:.3f}")
    
    return predictions

if __name__ == "__main__":
    # Run demonstrations
    eeg_results = demonstrate_eeg_pipeline()
    prediction_results = demonstrate_model_prediction()
    
    print("\n" + "=" * 50)
    print("Pipeline demonstration completed!")
    print("Check the generated plots and results above.")