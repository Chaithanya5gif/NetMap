import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Mumbai data
df = pd.read_csv('output/mumbai_data.csv')

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.facecolor'] = 'white'

# Figure 1: Operator Speed Comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Average download speed by operator
operator_speeds = df.groupby('operator')['download_speed'].mean().sort_values(ascending=False)
colors = {'jio': '#1A936F', 'airtel': '#004E89', 'vi': '#FF6B35'}
bar_colors = [colors.get(op, '#333') for op in operator_speeds.index]

axes[0].bar(operator_speeds.index, operator_speeds.values, color=bar_colors, edgecolor='black', linewidth=0.5)
axes[0].set_title('Mumbai: Average Download Speed by Operator', fontsize=12, fontweight='bold', pad=10)
axes[0].set_ylabel('Download Speed (Mbps)', fontsize=10)
axes[0].set_ylim(0, max(operator_speeds.values) * 1.2)

# Add value labels
for i, (op, val) in enumerate(operator_speeds.items()):
    axes[0].text(i, val + 2, f'{val:.1f}', ha='center', fontweight='bold', fontsize=11)

# Right: 4G vs 5G comparison
tech_data = df.groupby(['operator', 'technology'])['download_speed'].mean().unstack()
x = np.arange(len(tech_data.index))
width = 0.35

bars1 = axes[1].bar(x - width/2, tech_data['4G'], width, label='4G', color='#E63946', edgecolor='black', linewidth=0.5)
bars2 = axes[1].bar(x + width/2, tech_data['5G'], width, label='5G', color='#457B9D', edgecolor='black', linewidth=0.5)

axes[1].set_title('Mumbai: 4G vs 5G Download Speed', fontsize=12, fontweight='bold', pad=10)
axes[1].set_ylabel('Download Speed (Mbps)', fontsize=10)
axes[1].set_xticks(x)
axes[1].set_xticklabels(tech_data.index)
axes[1].legend()
axes[1].set_ylim(0, tech_data['5G'].max() * 1.2)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        axes[1].annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('output/mumbai_speed_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: output/mumbai_speed_comparison.png")

# Figure 2: Quality Score Distribution
fig, ax = plt.subplots(figsize=(10, 6))

for op in ['jio', 'airtel', 'vi']:
    op_data = df[df['operator'] == op]['quality_score']
    ax.hist(op_data, bins=30, alpha=0.6, label=op.upper(), color=colors[op], edgecolor='black', linewidth=0.3)

ax.set_title('Mumbai: Quality Score Distribution by Operator', fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel('Quality Score (0-100)', fontsize=10)
ax.set_ylabel('Number of Tests', fontsize=10)
ax.legend(title='Operator')
ax.axvline(df['quality_score'].mean(), color='black', linestyle='--', linewidth=1, label=f'Overall Mean: {df["quality_score"].mean():.1f}')

plt.tight_layout()
plt.savefig('output/mumbai_quality_distribution.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: output/mumbai_quality_distribution.png")

# Figure 3: Signal Strength vs Download Speed Scatter
fig, ax = plt.subplots(figsize=(10, 7))

for op in ['jio', 'airtel', 'vi']:
    op_df = df[df['operator'] == op].sample(min(500, len(df[df['operator'] == op])))  # Sample for clarity
    ax.scatter(op_df['signal_strength'], op_df['download_speed'], 
               alpha=0.5, s=20, label=op.upper(), color=colors[op])

ax.set_title('Mumbai: Signal Strength vs Download Speed', fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel('Signal Strength (RSRP dBm)', fontsize=10)
ax.set_ylabel('Download Speed (Mbps)', fontsize=10)
ax.legend(title='Operator')
ax.invert_xaxis()  # Stronger signal (less negative) to the right

plt.tight_layout()
plt.savefig('output/mumbai_signal_vs_speed.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: output/mumbai_signal_vs_speed.png")

print("\n=== ALL CHARTS GENERATED ===")
print("1. output/mumbai_speed_comparison.png — Bar charts")
print("2. output/mumbai_quality_distribution.png — Histograms")
print("3. output/mumbai_signal_vs_speed.png — Scatter plot")