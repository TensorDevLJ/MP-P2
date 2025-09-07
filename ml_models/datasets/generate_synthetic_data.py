"""
Generate synthetic datasets for training and testing
"""
import numpy as np
import pandas as pd
from pathlib import Path
import argparse
from typing import Dict, List, Tuple
import structlog

logger = structlog.get_logger(__name__)

class SyntheticEEGGenerator:
    """Generate realistic synthetic EEG data for model training"""
    
    def __init__(self, sampling_rate: int = 128):
        self.fs = sampling_rate
        self.frequency_bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 12),
            'beta': (12, 30),
            'gamma': (30, 45)
        }
    
    def generate_emotion_dataset(
        self, 
        n_samples_per_class: int = 200, 
        duration: float = 5.0
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Generate synthetic EEG data labeled by emotional state"""
        
        emotions = ['happy', 'sad', 'neutral', 'stressed', 'relaxed']
        n_timepoints = int(duration * self.fs)
        
        # Emotional state templates (frequency characteristics)
        emotion_templates = {
            'happy': {
                'alpha': 0.6,    # High alpha
                'beta': 0.4,     # Moderate beta
                'theta': 0.3,    # Low theta
                'gamma': 0.3     # Moderate gamma
            },
            'sad': {
                'alpha': 0.2,    # Low alpha
                'theta': 0.8,    # High theta
                'beta': 0.3,     # Low beta
                'delta': 0.6     # High delta
            },
            'neutral': {
                'alpha': 0.5,    # Balanced
                'beta': 0.5,
                'theta': 0.4,
                'delta': 0.3
            },
            'stressed': {
                'beta': 0.9,     # Very high beta
                'alpha': 0.2,    # Very low alpha
                'gamma': 0.6,    # High gamma
                'theta': 0.3
            },
            'relaxed': {
                'alpha': 0.9,    # Very high alpha
                'theta': 0.6,    # Moderate theta
                'beta': 0.2,     # Very low beta
                'delta': 0.4
            }
        }
        
        data = []
        labels = []
        
        for emotion_idx, emotion in enumerate(emotions):
            template = emotion_templates[emotion]
            
            for _ in range(n_samples_per_class):
                signal = self._generate_signal_from_template(template, n_timepoints)
                data.append(signal.reshape(1, -1))  # Add channel dimension
                labels.append(emotion_idx)
        
        # Shuffle data
        indices = np.random.permutation(len(data))
        data = np.array(data)[indices]
        labels = np.array(labels)[indices]
        
        logger.info(f"Generated {len(data)} EEG samples for {len(emotions)} emotions")
        
        return data, labels, emotions
    
    def generate_anxiety_dataset(
        self,
        n_samples_per_class: int = 200,
        duration: float = 5.0
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Generate synthetic EEG data labeled by anxiety level"""
        
        anxiety_levels = ['low', 'moderate', 'high']
        n_timepoints = int(duration * self.fs)
        
        anxiety_templates = {
            'low': {
                'alpha': 0.8,     # High alpha (relaxed)
                'beta': 0.3,      # Low beta
                'gamma': 0.2,     # Low gamma
                'theta': 0.5      # Moderate theta
            },
            'moderate': {
                'alpha': 0.4,     # Reduced alpha
                'beta': 0.6,      # Increased beta
                'gamma': 0.4,     # Moderate gamma
                'theta': 0.4      # Moderate theta
            },
            'high': {
                'alpha': 0.2,     # Very low alpha
                'beta': 0.9,      # Very high beta
                'gamma': 0.8,     # High gamma
                'theta': 0.3      # Low theta
            }
        }
        
        data = []
        labels = []
        
        for anxiety_idx, anxiety in enumerate(anxiety_levels):
            template = anxiety_templates[anxiety]
            
            for _ in range(n_samples_per_class):
                signal = self._generate_signal_from_template(template, n_timepoints)
                
                # Add anxiety-specific noise characteristics
                if anxiety == 'high':
                    # Add more irregular patterns for high anxiety
                    signal += 0.3 * np.random.randn(n_timepoints)
                
                data.append(signal.reshape(1, -1))
                labels.append(anxiety_idx)
        
        # Shuffle
        indices = np.random.permutation(len(data))
        data = np.array(data)[indices]
        labels = np.array(labels)[indices]
        
        logger.info(f"Generated {len(data)} EEG samples for {len(anxiety_levels)} anxiety levels")
        
        return data, labels, anxiety_levels
    
    def _generate_signal_from_template(
        self, 
        template: Dict[str, float], 
        n_timepoints: int
    ) -> np.ndarray:
        """Generate EEG signal based on frequency template"""
        
        t = np.linspace(0, n_timepoints / self.fs, n_timepoints)
        signal = np.zeros(n_timepoints)
        
        # Add each frequency component
        for band, amplitude in template.items():
            if band in self.frequency_bands:
                low_freq, high_freq = self.frequency_bands[band]
                
                # Random frequency within band
                freq = np.random.uniform(low_freq, high_freq)
                
                # Random phase
                phase = np.random.uniform(0, 2 * np.pi)
                
                # Add component
                signal += amplitude * np.sin(2 * np.pi * freq * t + phase)
        
        # Add realistic 1/f noise
        freqs = np.fft.fftfreq(n_timepoints, 1/self.fs)
        freq_mask = freqs > 0
        noise_spectrum = np.zeros(n_timepoints, dtype=complex)
        noise_spectrum[freq_mask] = (freqs[freq_mask] ** -1) * np.random.randn(np.sum(freq_mask))
        
        # Convert back to time domain and add to signal
        noise = np.real(np.fft.ifft(noise_spectrum))
        signal += 0.1 * noise
        
        # Normalize
        signal = signal / np.std(signal)
        
        return signal

def generate_text_dataset(n_samples_per_class: int = 300) -> pd.DataFrame:
    """Generate synthetic text dataset for depression classification"""
    
    logger.info("Generating synthetic text dataset...")
    
    # Depression severity classes and example patterns
    text_templates = {
        'not_depressed': [
            "Had a wonderful day today, feeling grateful and positive about life",
            "Really enjoying my work and feeling accomplished with recent projects", 
            "Looking forward to weekend activities with friends and family",
            "Feeling energetic and motivated to tackle new challenges ahead",
            "Having great conversations and feeling connected to people around me"
        ],
        'moderate': [
            "Feeling a bit down lately, not as much energy as usual",
            "Having trouble sleeping and feeling tired during the day",
            "Lost interest in some activities I used to really enjoy",
            "Feeling overwhelmed with daily tasks and responsibilities recently", 
            "Having difficulty concentrating at work and feeling less productive"
        ],
        'severe': [
            "Everything feels pointless and I have no energy for anything",
            "Can't seem to get out of bed, feeling hopeless about everything",
            "Nothing brings me joy anymore, feeling completely empty inside",
            "Feel like such a burden to everyone around me",
            "Don't see any point in trying anymore, everything feels impossible"
        ]
    }
    
    # Generate variations of each template
    dataset = []
    
    for label, templates in text_templates.items():
        for i in range(n_samples_per_class):
            # Select base template
            base_text = np.random.choice(templates)
            
            # Add variations
            variations = [
                base_text,
                base_text.replace("feeling", "been feeling"),
                base_text.replace("I", "I've been"),
                f"Lately, {base_text.lower()}",
                f"{base_text}. This has been going on for a while."
            ]
            
            final_text = np.random.choice(variations)
            
            # Add noise words occasionally
            if np.random.random() < 0.3:
                noise_words = ["really", "quite", "very", "somewhat", "pretty", "rather"]
                final_text = final_text.replace("feeling", f"feeling {np.random.choice(noise_words)}")
            
            dataset.append({
                'text': final_text,
                'label': list(text_templates.keys()).index(label),
                'depression_severity': label
            })
    
    # Shuffle dataset
    df = pd.DataFrame(dataset)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    logger.info(f"Generated {len(df)} text samples")
    logger.info(f"Class distribution: {df['depression_severity'].value_counts().to_dict()}")
    
    return df

def main():
    """Generate all synthetic datasets"""
    
    parser = argparse.ArgumentParser(description="Generate synthetic datasets")
    parser.add_argument("--eeg_samples", type=int, default=200, help="Samples per EEG class")
    parser.add_argument("--text_samples", type=int, default=300, help="Samples per text class")
    parser.add_argument("--output_dir", type=str, default="ml_models/datasets", help="Output directory")
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate EEG datasets
    generator = SyntheticEEGGenerator()
    
    # Emotion dataset
    emotion_data, emotion_labels, emotion_classes = generator.generate_emotion_dataset(
        n_samples_per_class=args.eeg_samples
    )
    
    np.save(output_path / "synthetic_eeg_emotion_data.npy", emotion_data)
    np.save(output_path / "synthetic_eeg_emotion_labels.npy", emotion_labels)
    
    with open(output_path / "emotion_classes.json", 'w') as f:
        json.dump(emotion_classes, f)
    
    # Anxiety dataset
    anxiety_data, anxiety_labels, anxiety_classes = generator.generate_anxiety_dataset(
        n_samples_per_class=args.eeg_samples
    )
    
    np.save(output_path / "synthetic_eeg_anxiety_data.npy", anxiety_data)
    np.save(output_path / "synthetic_eeg_anxiety_labels.npy", anxiety_labels)
    
    with open(output_path / "anxiety_classes.json", 'w') as f:
        json.dump(anxiety_classes, f)
    
    # Text dataset
    text_df = generate_text_dataset(n_samples_per_class=args.text_samples)
    text_df.to_csv(output_path / "synthetic_depression_text.csv", index=False)
    
    print(f"\n✅ Synthetic datasets generated in {output_path}")
    print(f"   📊 EEG Emotion: {len(emotion_data)} samples")
    print(f"   😰 EEG Anxiety: {len(anxiety_data)} samples") 
    print(f"   📝 Text Depression: {len(text_df)} samples")
    
    print(f"\n📁 Files created:")
    print(f"   {output_path / 'synthetic_eeg_emotion_data.npy'}")
    print(f"   {output_path / 'synthetic_eeg_anxiety_data.npy'}")
    print(f"   {output_path / 'synthetic_depression_text.csv'}")

if __name__ == "__main__":
    import json
    main()