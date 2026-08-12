from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, FancyArrowPatch

OUT = Path(__file__).resolve().parent
png = OUT / "AQT_TOC_graphic_110x20mm.png"
svg = OUT / "AQT_TOC_graphic_110x20mm.svg"

# Advanced Quantum Technologies accepts a 110 mm x 20 mm graphical-ToC format.
# This canvas is approximately 1300 x 236 px and uses labels >= 10 pt.
fig = plt.figure(figsize=(11, 2), dpi=118.2)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 11)
ax.set_ylim(0, 2)
ax.axis("off")

ax.text(0.45, 1.55, "Fixed measurement", ha="left", va="center", fontsize=11, fontweight="bold")
for i, h in enumerate([0.35, 0.65, 0.95, 0.55]):
    ax.add_patch(Rectangle((0.55 + 0.22 * i, 0.45), 0.12, h, fill=False, linewidth=1.4))
ax.text(0.45, 0.22, "measurement-score space", ha="left", va="center", fontsize=10)
ax.add_patch(FancyArrowPatch((1.75, 1.0), (2.45, 1.0), arrowstyle="->", mutation_scale=14, linewidth=1.4))

cx, cy = 4.9, 1.0
ax.add_patch(Ellipse((cx, cy), width=3.7, height=1.25, fill=False, linewidth=1.7))
ax.text(cx, 1.72, r"Tangent covariance $C$", ha="center", va="center", fontsize=11, fontweight="bold")
ax.add_patch(FancyArrowPatch((3.4, 1.0), (6.4, 1.0), arrowstyle="<->", mutation_scale=11, linewidth=1.0))
ax.add_patch(FancyArrowPatch((4.9, 0.58), (4.9, 1.42), arrowstyle="<->", mutation_scale=11, linewidth=1.0))

ax.add_patch(Rectangle((4.68, 0.42), 0.44, 1.16, angle=22, fill=False, linewidth=2.0))
ax.add_patch(Rectangle((3.45, 0.84), 2.9, 0.32, fill=False, linewidth=2.0, linestyle="--"))
ax.text(3.55, 0.35, "physical readout", ha="center", va="center", fontsize=10)
ax.add_patch(FancyArrowPatch((3.9, 0.45), (4.52, 0.78), arrowstyle="->", mutation_scale=10, linewidth=1.0))
ax.text(5.95, 0.35, "aligned readout", ha="center", va="center", fontsize=10)
ax.add_patch(FancyArrowPatch((5.8, 0.45), (5.55, 0.82), arrowstyle="->", mutation_scale=10, linewidth=1.0))
ax.text(4.9, 0.08, r"same rank $r$  •  different spectral orientation", ha="center", va="center", fontsize=10)

ax.add_patch(FancyArrowPatch((6.95, 1.0), (7.7, 1.0), arrowstyle="->", mutation_scale=14, linewidth=1.4))
ax.text(8.0, 1.55, "Accessible tangent mass", ha="left", va="center", fontsize=11, fontweight="bold")
ax.text(8.0, 1.12, "misaligned  →  smaller", ha="left", va="center", fontsize=10)
ax.text(8.0, 0.80, "aligned      →  larger", ha="left", va="center", fontsize=10)
ax.text(8.0, 0.35, "finite-shot directional signal changes", ha="left", va="center", fontsize=10)

fig.savefig(png, dpi=118.2, bbox_inches=None, pad_inches=0)
fig.savefig(svg, format="svg", bbox_inches=None, pad_inches=0)
plt.close(fig)
print(png)
print(svg)
