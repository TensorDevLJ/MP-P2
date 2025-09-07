"""
Utility functions for generating visualizations
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
import io
import base64
import structlog

logger = structlog.get_logger(__name__)

# Set matplotlib style
plt.style.use('default')
sns.set_palette("husl")

class VisualizationGenerator:
    """Generate charts and plots for EEG analysis results"""
    
    def __init__(self):
        self.figure_size = (12, 8)
        self.dpi = 150
        
    def generate_band_powers_plot(
        self, 
        band_powers: Dict[str, List[float]], 
        times: List[float],
        title: str = "EEG Band Powers Over Time"
    ) -> str:
        """Generate band powers time series plot as base64 image"""
        
        plt.figure(figsize=self.figure_size)
        
        colors = {
            'delta': '#FF6B6B',
            'theta': '#4ECDC4', 
            'alpha': '#45B7D1',
            'beta': '#96CEB4',
            'gamma': '#FFEAA7'
        }
        
        for band, powers in band_powers.items():
            if band in colors:
                plt.plot(times, powers, label=f'{band.capitalize()} ({band})', 
                        color=colors[band], linewidth=2, alpha=0.8)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Time (seconds)', fontsize=12)
        plt.ylabel('Power (μV²)', fontsize=12)
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3)
        
        # Add annotations for significant features
        if 'alpha' in band_powers and 'beta' in band_powers:
            alpha_avg = np.mean(band_powers['alpha'])
            beta_avg = np.mean(band_powers['beta'])
            
            if alpha_avg > beta_avg * 1.5:
                plt.annotate('Relaxed state\n(high α/β ratio)', 
                           xy=(times[len(times)//2], alpha_avg),
                           xytext=(times[len(times)//4], max(band_powers['alpha'])),
                           arrowprops=dict(arrowstyle='->', color='blue', alpha=0.6),
                           fontsize=10, ha='center')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return plot_base64
    
    def generate_psd_plot(
        self, 
        frequencies: List[float], 
        power: List[float],
        title: str = "Power Spectral Density"
    ) -> str:
        """Generate power spectral density plot"""
        
        plt.figure(figsize=(10, 6))
        
        plt.loglog(frequencies, power, 'b-', linewidth=2, alpha=0.8)
        
        # Add frequency band regions
        bands = {
            'Delta (0.5-4 Hz)': (0.5, 4, '#FF6B6B'),
            'Theta (4-8 Hz)': (4, 8, '#4ECDC4'),
            'Alpha (8-12 Hz)': (8, 12, '#45B7D1'),
            'Beta (12-30 Hz)': (12, 30, '#96CEB4'),
            'Gamma (30-45 Hz)': (30, 45, '#FFEAA7')
        }
        
        for band_name, (low, high, color) in bands.items():
            plt.axvspan(low, high, alpha=0.2, color=color, label=band_name)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Frequency (Hz)', fontsize=12)
        plt.ylabel('Power (μV²/Hz)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return plot_base64
    
    def generate_risk_trends_plot(
        self, 
        risk_data: List[Dict[str, Any]], 
        days: int = 30
    ) -> str:
        """Generate risk level trends plot"""
        
        if not risk_data:
            return self._generate_empty_plot("No risk data available")
        
        plt.figure(figsize=(12, 6))
        
        # Convert risk levels to numeric scores
        risk_scores = {'stable': 1, 'mild': 2, 'moderate': 3, 'high': 4}
        
        dates = [datetime.fromisoformat(item['date']) for item in risk_data]
        scores = [risk_scores.get(item['level'], 1) for item in risk_data]
        confidences = [item.get('confidence', 0.5) for item in risk_data]
        
        # Plot risk scores with confidence as alpha
        scatter = plt.scatter(dates, scores, c=scores, s=[c*100 for c in confidences], 
                            alpha=0.7, cmap='RdYlBu_r', edgecolors='black', linewidth=0.5)
        
        # Add trend line
        if len(dates) > 1:
            z = np.polyfit(range(len(scores)), scores, 1)
            trend_line = np.poly1d(z)
            plt.plot(dates, trend_line(range(len(scores))), 'r--', alpha=0.8, linewidth=2)
        
        plt.title('Mental Health Risk Trends', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Risk Level', fontsize=12)
        plt.yticks([1, 2, 3, 4], ['Stable', 'Mild', 'Moderate', 'High'])
        plt.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Risk Level', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return plot_base64
    
    def _generate_empty_plot(self, message: str) -> str:
        """Generate empty plot with message"""
        
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, message, ha='center', va='center', 
                fontsize=14, transform=plt.gca().transAxes)
        plt.axis('off')
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return plot_base64