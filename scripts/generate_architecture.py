from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "system-architecture.png"

fig, ax = plt.subplots(figsize=(13.5, 6.2), dpi=180)
fig.patch.set_facecolor("#07111f")
ax.set_facecolor("#07111f")
ax.set_xlim(0, 13.5)
ax.set_ylim(0, 6.2)
ax.axis("off")

nodes = {
    "Plant digital twin\nMATLAB + Python": (0.5, 3.7, 2.4, 1.1, "#0b5d7a"),
    "Virtual sensors\nand fault injection": (3.3, 3.7, 2.4, 1.1, "#096b63"),
    "Edge I/O + MCU\nemulation": (6.1, 3.7, 2.4, 1.1, "#5d4c9b"),
    "Virtual PLC\ninterlocks + sequence": (8.9, 3.7, 2.4, 1.1, "#8a4d23"),
    "Virtual VFD\nand choke": (11.7, 3.7, 1.4, 1.1, "#8a3f55"),
    "OPC UA / MQTT / Modbus": (4.1, 1.6, 2.6, 0.9, "#334155"),
    "Historian + analytics\nestimation + optimization": (7.3, 1.3, 2.7, 1.5, "#164e63"),
    "Engineering HMI\nmanual / advisory / auto": (10.7, 1.6, 2.3, 0.9, "#3f3f46"),
}

for label, (x, y, w, h, color) in nodes.items():
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                           facecolor=color, edgecolor="#94a3b8", linewidth=1.0)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", color="white", fontsize=9.2, weight="bold")

def arrow(a, b, color="#65d6ff", curve=0.0):
    x1, y1, w1, h1, _ = nodes[a]
    x2, y2, w2, h2, _ = nodes[b]
    start = (x1 + w1, y1 + h1 / 2) if x2 > x1 else (x1 + w1 / 2, y1)
    end = (x2, y2 + h2 / 2) if x2 > x1 else (x2 + w2 / 2, y2 + h2)
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                linewidth=1.5, color=color, connectionstyle=f"arc3,rad={curve}"))

top = list(nodes)[:5]
for left, right in zip(top, top[1:]):
    arrow(left, right)
arrow(top[-1], top[0], color="#f8b84e", curve=0.30)
arrow(top[2], "OPC UA / MQTT / Modbus", color="#a7f3d0")
arrow("OPC UA / MQTT / Modbus", "Historian + analytics\nestimation + optimization")
arrow("Historian + analytics\nestimation + optimization", "Engineering HMI\nmanual / advisory / auto")
arrow("Historian + analytics\nestimation + optimization", "Virtual PLC\ninterlocks + sequence", color="#f8b84e")

ax.text(0.5, 5.6, "OPENLIFT DED", color="#67e8f9", fontsize=18, weight="bold")
ax.text(0.5, 5.22, "Software-first multidisciplinary architecture for an ESP-lifted well", color="#cbd5e1", fontsize=10.5)
ax.text(0.5, 0.55, "Safety rule: analytics recommends; deterministic constraints and PLC interlocks authorize.", color="#f8b84e", fontsize=9.5)
plt.tight_layout(pad=0.3)
OUT.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT, bbox_inches="tight", facecolor=fig.get_facecolor())

