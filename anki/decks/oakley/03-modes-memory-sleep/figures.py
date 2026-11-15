"""Картинки к главе 3 «Думай как математик»: переключение режимов, память и сон."""

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Circle, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import C, new, save  # noqa: E402


def blank(ax, xlim, ylim, equal=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    ax.axis("off")


# ---------- стоянки при восхождении ----------

pts = [(0, 0), (1.6, 1.4), (2.6, 1.4), (4.0, 2.9), (5.0, 2.9), (6.3, 4.4), (7.3, 4.4), (8.4, 5.8)]
fig, ax = new(size=(7.0, 4.2))
blank(ax, (-0.5, 9.6), (-0.6, 6.8))
ax.fill([-0.5, *[p[0] for p in pts], 9.6, 9.6], [-0.6, *[p[1] for p in pts], 2.4, -0.6],
        color=C.light, zorder=0)
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    climb = y1 > y0
    ax.plot([x0, x1], [y0, y1], color=C.blue if climb else C.green, lw=5 if climb else 7,
            solid_capstyle="round")
ax.text(8.4, 6.2, "понимание", ha="center", fontsize=13, color=C.ink)
ax.plot(8.4, 5.8, marker="^", color=C.orange, markersize=14)
ax.text(0.45, 1.25, "подъём:\nфокус", color=C.blue, fontsize=12, ha="right")
ax.text(1.7, 2.0, "стоянка:\nрассеянный", color=C.green, fontsize=12, ha="center")
save(fig, "mountain-rest-stops")


# ---------- запас сил в фокусе ----------

t = np.linspace(0, 10, 1000)
fig, ax = new(size=(6.6, 3.8))
ax.plot(t, np.clip(1 - 0.095 * t, 0, 1), color=C.red, label="без перерывов")
saw = np.empty_like(t)
for i, x in enumerate(t):
    phase = x % 2.5
    saw[i] = 1 - 0.12 * phase if phase < 2.1 else 1 - 0.12 * 2.1 + (phase - 2.1) / 0.4 * 0.12 * 2.1
ax.plot(t, saw, color=C.blue, label="с короткими передышками")
ax.set_xlabel("время работы в фокусе")
ax.set_ylabel("ментальная энергия")
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(-0.05, 1.15)
ax.legend(loc="lower left")
save(fig, "focus-energy")


# Кирпичная стена взята из книги: media/book-brick-wall.png (рисунок к разделу «Избегайте установки»).


# ---------- рабочая память: жонглёр ----------

fig, ax = new(size=(5.6, 4.2))
blank(ax, (-3.2, 3.2), (-1.2, 3.6))
ang = np.linspace(np.pi * 0.85, np.pi * 0.15, 4)
cols = [C.blue, C.orange, C.green, C.purple]
for a, c in zip(ang, cols):
    ax.add_patch(Circle((2.4 * np.cos(a), 0.6 + 2.4 * np.sin(a)), 0.38, color=c))
arc = np.linspace(np.pi * 0.95, np.pi * 0.05, 100)
ax.plot(2.4 * np.cos(arc), 0.6 + 2.4 * np.sin(arc), color=C.gray, lw=1.5, ls="--", zorder=0)
ax.plot([-2.3, -1.5], [-0.2, -0.2], color=C.ink, lw=6, solid_capstyle="round")
ax.plot([1.5, 2.3], [-0.2, -0.2], color=C.ink, lw=6, solid_capstyle="round")
ax.text(0, -0.9, "в воздухе около 4 порций", ha="center", fontsize=13, color=C.ink)
save(fig, "working-memory-juggler")


# ---------- рабочая память до и после понимания ----------

def slot(ax, i, row, color=None, label=""):
    x, y = i * 1.5, row
    if color is None:
        ax.add_patch(FancyBboxPatch((x, y), 1.2, 0.8, boxstyle="round,pad=0.03",
                                    facecolor="none", edgecolor=C.gray, lw=1.6, ls="--"))
        ax.text(x + 0.6, y + 0.4, "свободно", ha="center", va="center", fontsize=9, color=C.gray)
    else:
        ax.add_patch(FancyBboxPatch((x, y), 1.2, 0.8, boxstyle="round,pad=0.03",
                                    facecolor=to_rgba(color, 0.85), edgecolor=color, lw=1.6))
        ax.text(x + 0.6, y + 0.4, label, ha="center", va="center", fontsize=10, color="white")


fig, ax = new(size=(7.0, 3.4))
blank(ax, (-2.6, 6.0), (-0.3, 3.0))
ax.text(-0.3, 2.3, "не понято", ha="right", va="center", fontsize=12)
for i in range(3):
    slot(ax, i, 1.9, C.orange, f"часть {i + 1}")
slot(ax, 3, 1.9, C.blue, "другое")
ax.text(-0.3, 0.5, "понято", ha="right", va="center", fontsize=12)
slot(ax, 0, 0.1, C.orange, "понятие")
for i in range(1, 4):
    slot(ax, i, 0.1)
save(fig, "wm-before-after")


# ---------- интервальное повторение ----------

fig, (a1, a2) = new(nrows=2, size=(7.0, 3.6), sharex=True)
days = np.arange(7)
for ax in (a1, a2):
    ax.set_xlim(-0.5, 7.0)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
xs = np.linspace(0.1, 0.8, 20)
a1.vlines(xs, 0.15, 0.85, color=C.red, lw=1.6)
a1.set_title("20 повторений за один вечер: хуже", fontsize=12, color=C.red, loc="left")
counts = [3, 3, 3, 3, 3, 3, 2]
for d, n in zip(days, counts):
    a2.vlines(d + np.linspace(0.2, 0.7, n), 0.15, 0.85, color=C.green, lw=2)
a2.set_title("те же 20, разнесённые на неделю: лучше", fontsize=12, color=C.green, loc="left")
a2.set_xticks(days + 0.45)
a2.set_xticklabels([f"день {d + 1}" for d in days])
save(fig, "spaced-vs-massed")
