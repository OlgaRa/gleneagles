import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# Read CSV
df = pd.read_csv('hoa-info.csv')

# Filter rows with valid sub_fees and convert to numeric
df = df[df['sub_fees'].notna() & (df['sub_fees'] != 'per acre cost')]
df['sub_fees'] = pd.to_numeric(df['sub_fees'])

# Update GLENEAGLES fee to 325
df.loc[df['subdivision'] == 'GLENEAGLES', 'sub_fees'] = 325

# Sort by sub_fees descending
df = df.sort_values('sub_fees', ascending=False)

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Prepare colors: red for DIAMOND MANAGEMENT, blue for others
colors = ['red' if mgmt == 'DIAMOND MANAGEMENT' else 'blue' for mgmt in df['management']]

# Create bar chart
bars = ax.bar(range(len(df)), df['sub_fees'], color=colors)

# Add orange patch for GLENEAGLES increase (250 to 325)
for i, (idx, row) in enumerate(df.iterrows()):
    if row['subdivision'] == 'GLENEAGLES':
        gleneagles_idx = i
        orange_patch = Rectangle((i - 0.4, 250), 0.8, 75,
                                 linewidth=0, edgecolor=None, facecolor='orange')
        ax.add_patch(orange_patch)
        break

# Add subdivision names on bars
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(i, row['sub_fees']/2, row['subdivision'],
            ha='center', va='center', rotation=90, fontsize=8, color='white', weight='bold')

# Add city labels at bottom of bars
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(i, 5, row['city'],
            ha='center', va='bottom', rotation=0, fontsize=7, color='white', weight='bold')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='red', label='Diamond Management'),
    Patch(facecolor='blue', label='Other Managements')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Find positions of EDGEWATER and FAIRWAYS
edgewater_idx = None
fairways_idx = None
for i, (idx, row) in enumerate(df.iterrows()):
    if row['subdivision'] == 'EDGEWATER':
        edgewater_idx = i
    elif row['subdivision'] == 'FAIRWAYS':
        fairways_idx = i

# Add label and arrows for "same buildings as GlenEagles"
if edgewater_idx is not None and fairways_idx is not None:
    # Place label in upper right area
    label_x = len(df) - 5
    label_y = df['sub_fees'].max() * 0.75
    ax.text(label_x, label_y, 'Same buildings\nas GlenEagles',
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black'))

    # Arrow to EDGEWATER
    edgewater_fee = df.iloc[edgewater_idx]['sub_fees']
    arrow1 = FancyArrowPatch((label_x - 0.5, label_y - 10), (edgewater_idx, edgewater_fee + 10),
                            arrowstyle='->', mutation_scale=20, linewidth=1.5, color='black')
    ax.add_patch(arrow1)

    # Arrow to FAIRWAYS
    fairways_fee = df.iloc[fairways_idx]['sub_fees']
    arrow2 = FancyArrowPatch((label_x - 0.5, label_y - 10), (fairways_idx, fairways_fee + 10),
                            arrowstyle='->', mutation_scale=20, linewidth=1.5, color='black')
    ax.add_patch(arrow2)

# Set labels
ax.set_xlabel('Kiln Creek villages', fontsize=12)
ax.set_ylabel('HOA Fees ($)', fontsize=12)
ax.set_xticks([])

# Adjust layout and save
plt.tight_layout()
plt.savefig('hoa_chart.png', dpi=300, bbox_inches='tight')
print("Chart saved as hoa_chart.png")
