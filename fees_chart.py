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

# Update CASCADES fee (subtract 120)
df.loc[df['subdivision'] == 'CASCADES', 'sub_fees'] = df.loc[df['subdivision'] == 'CASCADES', 'sub_fees'] - 100

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

# Add subdivision names on bars with unit counts for specific subdivisions
for i, (idx, row) in enumerate(df.iterrows()):
    subdivision_name = row['subdivision']
    if subdivision_name == 'GLENEAGLES':
        subdivision_name = 'GLENEAGLES (92 units)'
    elif subdivision_name == 'SHORELINE':
        subdivision_name = 'SHORELINE (124 units)'
    elif subdivision_name == 'FAIRWAYS':
        subdivision_name = 'FAIRWAYS (56 units)'

    ax.text(i, row['sub_fees']/2, subdivision_name,
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
ax.legend(handles=legend_elements, loc='upper right', fontsize=14)

# Find positions of EDGEWATER and FAIRWAYS
shoreline_idx = None
fairways_idx = None
for i, (idx, row) in enumerate(df.iterrows()):
    if row['subdivision'] == 'SHORELINE':
        shoreline_idx = i
    elif row['subdivision'] == 'FAIRWAYS':
        fairways_idx = i

# Add label and arrows for "same buildings as GlenEagles"
if shoreline_idx is not None and fairways_idx is not None:
    # Place label in upper right area
    label_x = 9
    label_y = 210
    ax.text(label_x, label_y, 'Same condos\nas in GlenEagles',
            fontsize=16, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black'))

    # Arrow to EDGEWATER
    edgewater_fee = df.iloc[shoreline_idx]['sub_fees']
    arrow1 = FancyArrowPatch((label_x + 0.5, label_y - 10), (shoreline_idx+0.4, edgewater_fee - 3),
                             arrowstyle='->', mutation_scale=20, linewidth=1.5, color='black')
    ax.add_patch(arrow1)

    # Arrow to FAIRWAYS
    fairways_fee = df.iloc[fairways_idx]['sub_fees']
    arrow2 = FancyArrowPatch((label_x + 0.5, label_y - 10), (fairways_idx+0.4, fairways_fee - 10),
                            arrowstyle='->', mutation_scale=20, linewidth=1.5, color='black')
    ax.add_patch(arrow2)

# Add label and arrow for "Our new HOA" pointing to GLENEAGLES
if gleneagles_idx is not None:
    gleneagles_fee = df.iloc[gleneagles_idx]['sub_fees']
    # Place label above the GlenEagles bar
    label2_x = gleneagles_idx + 5
    label2_y = gleneagles_fee - 5
    ax.text(label2_x, label2_y, 'Our new HOA',
            fontsize=20, ha='center', va='center', weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black'))

    # Arrow pointing to the top of GLENEAGLES bar
    arrow3 = FancyArrowPatch((label2_x, label2_y), (gleneagles_idx + 0.5, label2_y),
                            arrowstyle='->', mutation_scale=20, linewidth=3, color='red')
    ax.add_patch(arrow3)

# Set title and labels
ax.set_title('Kiln Creek community HOA fees', fontsize=16, weight='bold')
ax.set_xlabel('Kiln Creek villages', fontsize=12)
ax.set_ylabel('HOA Fees ($)', fontsize=12)
ax.set_ylim(0, 360)
ax.set_xticks([])

# Adjust layout and save
plt.tight_layout()
plt.savefig('hoa_chart.png', dpi=300, bbox_inches='tight')
print("Chart saved as hoa_chart.png")
