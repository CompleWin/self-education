"""Картинки к главе 7 «Думай как математик»: порции информации или ступор."""
# В главе 7 нет схем, только фото, поэтому все картинки нарисованы здесь.

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import C, new, save  # noqa: E402


def box(ax, x, y, text, color, w=2.6, h=0.9, fs=13, fill=0.15):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.05,rounding_size=0.18",
                                facecolor=to_rgba(color, fill), edgecolor=color, lw=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=C.ink)


def arrow(ax, p, q, color=C.gray, lw=2.2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=18,
                                 color=color, lw=lw, connectionstyle=f"arc3,rad={rad}"))


def blank(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


# ---------- шаг подсказывает следующий ----------

fig, ax = new(size=(7.6, 2.6))
blank(ax, (-0.3, 13.3), (-0.9, 3.0))
names = ["шаг 1", "шаг 2", "шаг 3", "ответ"]
for i, s in enumerate(names):
    box(ax, 1.4 + i * 3.4, 0.6, s, C.green if s == "ответ" else C.blue, w=2.4, h=1.0, fs=14)
    if i:
        x0 = 1.4 + (i - 1) * 3.4
        arrow(ax, (x0 + 1.3, 0.6), (x0 + 2.1, 0.6))
        ax.text(x0 + 1.7, -0.35, "подсказывает", ha="center", fontsize=10, color=C.gray)
ax.plot([0.2, 0.2, 12.8, 12.8], [1.45, 1.75, 1.75, 1.45], color=C.blue, lw=2)
ax.text(6.5, 2.2, "одна порция: решение целиком", ha="center", fontsize=13, color=C.blue)
save(fig, "solution-chain")


# ---------- метод: день 1 и день 2 ----------

fig, ax = new(size=(8.0, 3.6))
blank(ax, (-2.2, 15.2), (-1.0, 5.0))
ax.text(-2.0, 3.6, "день 1", fontsize=14, va="center", fontweight="bold")
day1 = [("решить\nсамому", C.blue), ("решить\nзаново", C.blue),
        ("перерыв", C.gray), ("решить\nперед сном", C.blue)]
for i, (s, c) in enumerate(day1):
    box(ax, 1.6 + i * 3.6, 3.6, s, c, w=2.8, h=1.3)
    if i:
        arrow(ax, (1.6 + (i - 1) * 3.6 + 1.5, 3.6), (1.6 + i * 3.6 - 1.5, 3.6))
ax.text(-2.0, 0.6, "день 2", fontsize=14, va="center", fontweight="bold")
box(ax, 3.4, 0.6, "решить снова:\nтолько трудные шаги", C.orange, w=5.2, h=1.3)
box(ax, 10.6, 0.6, "следующая задача:\nте же шаги", C.green, w=5.2, h=1.3)
arrow(ax, (6.1, 0.6), (7.9, 0.6))
arrow(ax, (12.4, 2.9), (4.5, 1.3), rad=-0.12)
ax.text(8.6, 2.15, "сон", fontsize=12, color=C.gray, ha="center")
save(fig, "method-timeline")


# ---------- намеренная тренировка ----------

steps = np.arange(1, 7)
hard = np.array([False, False, True, False, True, False])
even = np.full(6, 1.0)
focused = np.where(hard, 2.6, 0.3)

fig, (a1, a2) = new(nrows=2, size=(6.6, 4.6), sharex=True)
a1.bar(steps, even, color=C.gray, width=0.6)
a1.set_title("повторять всё подряд", loc="left", fontsize=13, color=C.gray)
a2.bar(steps, focused, color=[C.orange if h else C.gray for h in hard], width=0.6)
a2.set_title("намеренная тренировка", loc="left", fontsize=13, color=C.blue)
for ax in (a1, a2):
    ax.set_ylim(0, 3.1)
    ax.set_yticks([])
    ax.set_ylabel("время")
    ax.grid(False)
a2.set_xticks(steps, [f"шаг {s}" for s in steps])
for s in steps[hard]:
    a2.text(s, 2.7, "трудный", ha="center", fontsize=11, color=C.orange)
save(fig, "deliberate-practice")


# ---------- крах знаний ----------

t = np.linspace(0, 10, 500)
base = 0.25 + 0.06 * t
dip = -0.22 * np.exp(-((t - 5.0) / 0.9) ** 2)
jump = 0.32 / (1 + np.exp(-(t - 6.4) * 3.0))
u = base + dip + jump

fig, ax = new(size=(6.6, 3.8))
ax.axvspan(3.9, 6.1, color=C.red, alpha=0.08)
ax.plot(t, u, color=C.blue)
ax.text(5.0, 0.95, "крах знаний:\nмозг перестраивает\nзнания", ha="center", va="top",
        fontsize=11, color=C.red)
ax.text(7.4, 0.62, "скачок", ha="left", fontsize=13, color=C.green)
ax.set_xlabel("время учёбы")
ax.set_ylabel("понимание")
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0, 1.25)
ax.grid(False)
save(fig, "knowledge-collapse")


# ---------- ступор и рабочая память ----------

fig, (a1, a2) = new(ncols=2, size=(7.6, 3.6))
for ax in (a1, a2):
    blank(ax, (-0.4, 5.4), (-1.6, 4.4))
slots = [(1.2, 2.9), (3.8, 2.9), (1.2, 0.6), (3.8, 0.6)]
bits = [(-0.45, 0.35), (0.35, 0.45), (0.0, -0.1), (-0.3, -0.5), (0.45, -0.4)]

for (x, y) in slots:
    a1.add_patch(Circle((x, y), 1.0, facecolor=to_rgba(C.gray, 0.15), edgecolor=C.gray, lw=2))
    for (dx, dy) in bits:
        a1.add_patch(Circle((x + dx, y + dy), 0.13, color=C.gray))
for (x, y) in [(2.5, 4.15), (4.9, 4.0), (0.0, 4.1)]:
    a1.add_patch(Circle((x, y), 0.16, color=C.red))
a1.text(2.5, -1.2, "без порций: места нет,\nступор", ha="center", fontsize=12, color=C.red)

labels = ["решение\n(порция)", "детали\nзадачи", "свободно", "свободно"]
colors = [C.blue, C.orange, C.gray, C.gray]
for (x, y), lab, col in zip(slots, labels, colors):
    filled = col != C.gray
    a2.add_patch(Circle((x, y), 1.0, facecolor=to_rgba(col, 0.18 if filled else 0.0),
                        edgecolor=col, lw=2.5 if filled else 1.5))
    a2.text(x, y, lab, ha="center", va="center", fontsize=11, color=col if filled else C.gray)
a2.text(2.5, -1.2, "с порциями: место\nостаётся", ha="center", fontsize=12, color=C.blue)
save(fig, "choking-working-memory")


# ---------- эффект тестирования ----------

fig, ax = new(size=(7.4, 3.0))
blank(ax, (-0.4, 12.4), (-1.3, 2.4))
tt = np.linspace(0, 2 * np.pi, 200)
labels = ["слабый\nпаттерн", "после\nтеста", "после нескольких\nтестов"]
for k, (lw, al, lab) in enumerate(zip([1.5, 4, 8], [0.35, 0.65, 1.0], labels)):
    cx = 2 + k * 4
    for (dx, dy) in [(-0.8, 0.5), (0.0, 1.2), (0.8, 0.5), (0.3, -0.3), (-0.5, -0.3)]:
        ax.add_patch(Circle((cx + dx, 0.6 + dy * 0.8), 0.13, color=C.gray, zorder=3))
    xs = cx + 1.0 * np.cos(tt) * (1 + 0.15 * np.sin(3 * tt))
    ys = 0.85 + 0.85 * np.sin(tt) * (1 + 0.1 * np.cos(2 * tt))
    ax.plot(xs, ys, color=C.blue, lw=lw, alpha=al)
    ax.text(cx, -0.75, lab, ha="center", va="center", fontsize=11)
save(fig, "testing-effect")
