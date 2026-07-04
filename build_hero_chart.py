"""
Hero chart — World Cup Dataset Landscape (Round 2 Catalog)
Visualization: dataset coverage map showing table count vs rows, colored by quality tier
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("artifacts", exist_ok=True)

# ── Inline data for the hero chart ──────────────────────────────────────────
datasets = [
    # NEW in round 2 (solid markers)
    {"label": "martj42\nIntl Results", "era_start": 1872, "era_end": 2026, "tables": 3,
     "rows": 98034, "quality": "A+", "new_r2": True, "category": "Historical Primary", "wc_rows": 4031},
    {"label": "joshfjelstul\nWC Database", "era_start": 1930, "era_end": 2022, "tables": 27,
     "rows": 74979, "quality": "A+", "new_r2": True, "category": "Historical Primary", "wc_rows": 74979},
    {"label": "swaptr\nTeams 2026", "era_start": 2026, "era_end": 2026, "tables": 1,
     "rows": 48, "quality": "A", "new_r2": True, "category": "2026 Complement", "wc_rows": 48},
    {"label": "elo ratings\n(afonsocruz)", "era_start": 1901, "era_end": 2026, "tables": 1,
     "rows": 4683, "quality": "B+", "new_r2": True, "category": "Context", "wc_rows": 4683},
    {"label": "joebeachcapital\nz-Scores", "era_start": 2010, "era_end": 2022, "tables": 1,
     "rows": 5886, "quality": "B", "new_r2": True, "category": "Supplement", "wc_rows": 5886},
    {"label": "die9origephit\nWC 2022 Tactical", "era_start": 2022, "era_end": 2022, "tables": 1,
     "rows": 64, "quality": "B+", "new_r2": True, "category": "Supplement", "wc_rows": 64},
    {"label": "velvetcrystal\nWC 2026 Stats", "era_start": 2026, "era_end": 2026, "tables": 3,
     "rows": 3480, "quality": "C+", "new_r2": True, "category": "2026 Complement", "wc_rows": 3480},
    # From round 1 (outline markers)
    {"label": "mominullptr\nWC 2026 Primary", "era_start": 2026, "era_end": 2026, "tables": 11,
     "rows": 8263, "quality": "A", "new_r2": False, "category": "2026 Primary", "wc_rows": 8263},
    {"label": "swaptr\nMatches 2026", "era_start": 2026, "era_end": 2026, "tables": 1,
     "rows": 89, "quality": "A", "new_r2": False, "category": "2026 Complement", "wc_rows": 89},
    {"label": "swaptr\nPlayers 2026", "era_start": 2026, "era_end": 2026, "tables": 1,
     "rows": 1248, "quality": "A", "new_r2": False, "category": "2026 Complement", "wc_rows": 1248},
    {"label": "piterfm\nWC 1930-2026", "era_start": 1930, "era_end": 2026, "tables": 5,
     "rows": 10000, "quality": "A", "new_r2": False, "category": "Historical Primary", "wc_rows": 10000},
    {"label": "nawfeelrahman\nUltimate WC", "era_start": 1930, "era_end": 2026, "tables": 12,
     "rows": 3000, "quality": "B+", "new_r2": False, "category": "Supplement", "wc_rows": 3000},
    {"label": "darinhawley\nGoalscorers", "era_start": 1930, "era_end": 2018, "tables": 1,
     "rows": 1295, "quality": "B", "new_r2": False, "category": "Supplement", "wc_rows": 1295},
    {"label": "kkfkmf\nWhoScored", "era_start": 2026, "era_end": 2026, "tables": 20,
     "rows": 500000, "quality": "B", "new_r2": False, "category": "2026 Advanced", "wc_rows": 500000},
]
# SYNTHETIC excluded from chart

df = pd.DataFrame(datasets)

# ── Quality color map ─────────────────────────────────────────────────────────
q_colors = {
    "A+": "#1a7431",
    "A":  "#2db44a",
    "B+": "#F59E0B",
    "B":  "#F97316",
    "C+": "#9AA0A6",
}

fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [2, 1]})
fig.patch.set_facecolor("#FAFAFA")

# ── LEFT PANEL: Era coverage timeline ────────────────────────────────────────
ax = axes[0]
ax.set_facecolor("#FAFAFA")
ax.spines[['top', 'right']].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

# Sort by era_start then era_end
df_sorted = df.sort_values(["era_start", "era_end"]).reset_index(drop=True)
y_positions = range(len(df_sorted))

for i, row in df_sorted.iterrows():
    color = q_colors.get(row['quality'], '#999')
    lw = 8 if row['new_r2'] else 4
    alpha = 1.0 if row['new_r2'] else 0.6
    ls = '-' if row['new_r2'] else '--'
    ax.plot([row['era_start'], row['era_end']], [i, i],
            color=color, linewidth=lw, alpha=alpha, linestyle=ls,
            solid_capstyle='round')
    # Dot at each end
    ax.plot(row['era_start'], i, 'o', color=color, markersize=5 if row['new_r2'] else 3)
    ax.plot(row['era_end'], i, 'o', color=color, markersize=5 if row['new_r2'] else 3)

ax.set_yticks(list(y_positions))
ax.set_yticklabels(df_sorted['label'].tolist(), fontsize=7.5)
ax.set_xlabel("Year", fontsize=10)
ax.set_title("Era Coverage by Dataset", fontsize=11, fontweight='bold', loc='left', pad=8)
ax.axvline(x=2026, color='#D62728', linewidth=1.2, linestyle=':', alpha=0.7)
ax.text(2026.2, len(df_sorted)-0.5, "2026\ntoday", color='#D62728', fontsize=7.5, va='top')
ax.set_xlim(1865, 2030)
ax.grid(axis='x', color='#EEEEEE', linewidth=0.7)

# NEW badge
for i, row in df_sorted.iterrows():
    if row['new_r2']:
        ax.text(2028.5, i, "NEW", color='#1a7431', fontsize=6.5, fontweight='bold', va='center')

# ── RIGHT PANEL: Table count vs dataset rows (bubble) ────────────────────────
ax2 = axes[1]
ax2.set_facecolor("#FAFAFA")
ax2.spines[['top', 'right']].set_visible(False)
ax2.spines['left'].set_color('#CCCCCC')
ax2.spines['bottom'].set_color('#CCCCCC')

for _, row in df.iterrows():
    if row['rows'] is None:
        continue
    color = q_colors.get(row['quality'], '#999')
    marker = 'o' if row['new_r2'] else 's'
    ec = '#333333' if row['new_r2'] else 'none'
    size = max(40, min(800, row['rows'] / 200))
    ax2.scatter(row['tables'], np.log10(max(row['rows'], 1)),
                s=size, c=color, marker=marker, alpha=0.8,
                edgecolors=ec, linewidths=0.8, zorder=3)

ax2.set_xlabel("# Tables in dataset", fontsize=10)
ax2.set_ylabel("log₁₀(total rows)", fontsize=10)
ax2.set_title("Richness: Tables × Rows", fontsize=11, fontweight='bold', loc='left', pad=8)
ax2.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax2.set_yticklabels(['1', '10', '100', '1K', '10K', '100K', '1M'], fontsize=8)
ax2.grid(color='#EEEEEE', linewidth=0.7)

# ── Legend ───────────────────────────────────────────────────────────────────
legend_patches = [
    mpatches.Patch(color=q_colors["A+"], label="A+ quality"),
    mpatches.Patch(color=q_colors["A"],  label="A quality"),
    mpatches.Patch(color=q_colors["B+"], label="B+ quality"),
    mpatches.Patch(color=q_colors["B"],  label="B quality"),
    mpatches.Patch(color=q_colors["C+"], label="C+ quality"),
]
new_patch = plt.Line2D([0], [0], marker='o', color='w', label='New in Round 2',
                       markerfacecolor='#555', markersize=7, markeredgecolor='#333', markeredgewidth=1.5)
r1_patch  = plt.Line2D([0], [0], marker='s', color='w', label='Round 1 (dashed)',
                       markerfacecolor='#555', markersize=7)
fig.legend(handles=legend_patches + [new_patch, r1_patch],
           loc='lower center', ncol=4, fontsize=8,
           framealpha=0.9, edgecolor='#CCCCCC', bbox_to_anchor=(0.5, -0.04))

# ── Titles ───────────────────────────────────────────────────────────────────
fig.suptitle(
    "Round 2 Dataset Catalog: 14 Kaggle WC Sources Evaluated — 7 NEW Datasets Found",
    fontsize=13, fontweight='bold', y=1.01
)
fig.text(0.5, -0.07,
         "Italic = new in round 2 (solid line/circle). Source: Kaggle · n=14 datasets evaluated · "
         "boxwheel/wc-surprising-truths-catalog-r2",
         ha='center', fontsize=7.5, color='#666666', style='italic')

plt.tight_layout()
plt.savefig("artifacts/hero_catalog_r2.png", dpi=200, bbox_inches='tight', facecolor='#FAFAFA')
plt.savefig("artifacts/hero_catalog_r2.svg", bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print("Charts saved: artifacts/hero_catalog_r2.png / .svg")
