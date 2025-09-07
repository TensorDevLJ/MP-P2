"""
EEG processing pipeline tests
"""
import pytest
import numpy as np
import pandas as pd
from app.services.ml.eeg_processor import EEGProcessor
from app.utils.signal_processing import SignalProcessor

@pytest.fixture
def sample_eeg_data():
    """Generate sample EEG data for testing"""
    fs = 128
    duration = 10  # 10 seconds
    t = np.linspace(0, duration, fs * duration)
    
    # Generate synthetic EEG with known frequency components
    signal = (
        0.5 * np.sin(2 * np.pi * 10 * t) +      # Alpha (10 Hz)
        0.3 * np.sin(2 * np.pi * 6 * t) +       # Theta (6 Hz) 
        0.2 * np.sin(2 * np.pi * 20 * t) +      # Beta (20 Hz)
        0.1 * np.random.randn(len(t))           # Noise
    )
    
    # Create DataFrame
    df = pd.DataFrame({
        'Time': t,
        'EEG.AF3': signal,
        'EEG.F7': signal + 0.1 * np.random.randn(len(t))
    })
    
    return df, fs

def test_eeg_processor_initialization():
    """Test EEG processor initialization"""
    processor = EEGProcessor(sampling_rate=128)
    assert processor.sampling_rate == 128
    assert 'alpha' in processor.frequency_bands
    assert processor.frequency_bands['alpha'] == (8, 12)

@pytest.mark.asyncio
async def test_metadata_extraction(sample_eeg_data, tmp_path):
    """Test EEG file metadata extraction"""
    df, fs = sample_eeg_data
    
    # Save sample data to temporary file
    csv_file = tmp_path / "test_eeg.csv"
    df.to_csv(csv_file, index=False)
    
    processor = EEGProcessor(sampling_rate=fs)
    metadata = await processor.extract_metadata(str(csv_file))
    
    assert metadata['sampling_rate'] == fs
    assert 'EEG.AF3' in metadata['channels']
    assert metadata['duration_seconds'] == pytest.approx(10, rel=0.1)

def test_signal_preprocessing():
    """Test signal preprocessing pipeline"""
    # Generate test signal with known artifacts
    fs = 128
    t = np.linspace(0, 5, fs * 5)
    signal = np.sin(2 * np.pi * 10 * t) + 0.1 * np.sin(2 * np.pi * 50 * t)  # Alpha + 50Hz noise
    
    processor = SignalProcessor(sampling_rate=fs)
    
    # Test bandpass filter
    filtered = processor.apply_bandpass_filter(signal, 8, 12)  # Alpha band
    assert len(filtered) == len(signal)
    assert np.std(filtered) > 0  # Signal not completely removed
    
    # Test notch filter
    notched = processor.apply_notch_filter(signal, 50)
    assert len(notched) == len(signal)
    
    # Verify 50Hz is reduced (simplified check)
    freqs, psd_orig = signal.welch(signal, fs=fs)
    freqs, psd_filt = signal.welch(notched, fs=fs)
    
    # Find 50Hz bin
    freq_50_idx = np.argmin(np.abs(freqs - 50))
    # Power at 50Hz should be reduced
    assert psd_filt[freq_50_idx] < psd_orig[freq_50_idx]

def test_feature_extraction():
    """Test EEG feature extraction"""
    # Create test epoch
    fs = 128
    epoch_length = 2
    t = np.linspace(0, epoch_length, fs * epoch_length)
    
    # Alpha-dominant signal
    epoch = 0.8 * np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn(len(t))
    
    processor = SignalProcessor(sampling_rate=fs)
    
    # Test spectral features
    spectral_features = processor.compute_spectral_features(epoch)
    
    # Should detect high alpha power
    assert 'alpha_power' in spectral_features
    assert 'beta_power' in spectral_features
    assert spectral_features['alpha_power'] > spectral_features['beta_power']
    
    # Test temporal features
    temporal_features = processor.compute_temporal_features(epoch)
    
    assert 'hjorth_activity' in temporal_features
    assert 'hjorth_mobility' in temporal_features
    assert 'hjorth_complexity' in temporal_features
    assert all(isinstance(v, float) for v in temporal_features.values())

@pytest.mark.asyncio
async def test_eeg_processing_pipeline(sample_eeg_data, tmp_path):
    """Test complete EEG processing pipeline"""
    df, fs = sample_eeg_data
    
    # Save to file
    csv_file = tmp_path / "pipeline_test.csv"
    df.to_csv(csv_file, index=False)
    
    processor = EEGProcessor(sampling_rate=fs)
    
    # Process the file
    results = await processor.process_eeg_data(
        file_path=str(csv_file),
        channel="EEG.AF3",
        epoch_length=2.0,
        overlap=0.5
    )
    
    # Verify results structure
    assert 'features' in results
    assert 'charts' in results
    assert 'metadata' in results
    
    # Verify features
    features = results['features']
    assert 'band_powers' in features
    assert 'spectral_features' in features
    assert 'temporal_features' in features
    
    # Verify charts data
    charts = results['charts']
    assert 'bands_timeseries' in charts
    assert 'psd' in charts
    
    # Verify metadata
    metadata = results['metadata']
    assert metadata['sampling_rate'] == fs
    assert metadata['channel'] == "EEG.AF3"
    assert metadata['n_epochs'] > 0

def test_epoch_creation():
    """Test epoch creation from continuous data"""
    from app.utils.signal_processing import extract_eeg_epochs
    
    # 10 seconds of data at 128 Hz
    fs = 128
    duration = 10
    data = np.random.randn(fs * duration)
    
    # Extract 2-second epochs with 50% overlap
    epochs = extract_eeg_epochs(data, epoch_length=2.0, overlap=0.5, sampling_rate=fs)
    
    # Should get multiple epochs
    assert len(epochs) > 1
    
    # Each epoch should be 2 seconds long
    epoch_length = len(epochs[0])
    assert epoch_length == 2 * fs  # 256 samples
    
    # Test edge case: epoch longer than data
    short_data = np.random.randn(fs)  # 1 second
    short_epochs = extract_eeg_epochs(short_data, epoch_length=2.0, overlap=0.5, sampling_rate=fs)
    
    # Should return the original data as single epoch
    assert len(short_epochs) == 1
    assert len(short_epochs[0]) == len(short_data)

if __name__ == "__main__":
    pytest.main([__file__])