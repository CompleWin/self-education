"""Картинки к главе 6 «Думай как математик»: привычки-зомби и прокрастинация."""
# Рисунок media/book-small-rewards.png взят из книги (раздел «Как поставить привычки (зомби) себе на службу»), этот файл его не рисует.

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import C, new, save  # noqa: E402


def box(ax, x, y, text, color, w=2.6, h=0.9, fs=14, fill=0.15):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.05,rounding_size=0.18",
                                facecolor=to_rgba(color, fill), edgecolor=color, lw=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=C.ink)


def arrow(ax, p, q, color=C.gray, lw=2.2, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=20,
                                 color=color, lw=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


def blank(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


# ---------- петля привычки ----------

fig, ax = new(size=(6.0, 5.0))
blank(ax, (-3.9, 3.9), (-2.2, 3.0))
box(ax, 0, 2.2, "1. сигнал", C.orange)
box(ax, 2.3, -0.6, "2. действия", C.blue, w=2.5)
box(ax, -2.3, -0.6, "3. награда", C.green, w=2.5)
ax.text(0, -0.1, "4. вера", ha="center", va="center", fontsize=15, color=C.purple,
        fontweight="bold")
arrow(ax, (1.0, 1.7), (2.1, -0.05), rad=-0.25)
arrow(ax, (1.6, -1.15), (-1.6, -1.15), rad=-0.45)
arrow(ax, (-2.1, -0.05), (-1.0, 1.7), rad=-0.25)
save(fig, "habit-loop")


# ---------- где нужна сила воли ----------

fig, ax = new(size=(7.0, 4.2))
blank(ax, (-0.6, 9.6), (-1.0, 4.4))
box(ax, 1.2, 2.0, "сигнал", C.orange, w=2.2)
box(ax, 7.2, 3.3, "старая реакция:\nотвлечься", C.gray, w=3.6, h=1.2, fs=12)
box(ax, 7.2, 0.7, "новая реакция:\nработать", C.blue, w=3.6, h=1.2, fs=12)
arrow(ax, (2.4, 2.3), (5.3, 3.2), color=C.gray, ls="--")
arrow(ax, (2.4, 1.7), (5.3, 0.8), color=C.red, lw=3.2)
ax.text(3.9, -0.55, "сила воли нужна\nтолько здесь", ha="center", va="center",
        fontsize=12, color=C.red)
save(fig, "habit-loop-willpower")


# ---------- когда приходит награда ----------

t = np.linspace(0, 10, 400)
procr = 1.0 * np.exp(-t / 1.2) * (t > 0.15)
work = 1.0 / (1 + np.exp(-(t - 5.5) * 1.4))

fig, ax = new(size=(6.6, 3.8))
ax.plot(t, procr, color=C.red, label="прокрастинация")
ax.plot(t, work, color=C.blue, label="учёба")
ax.text(0.6, 0.97, "прокрастинация:\nнаграда сразу", color=C.red, fontsize=12, va="top")
ax.text(7.2, 0.82, "учёба:\nнаграда позже", color=C.blue, fontsize=12, va="top")
ax.set_xlabel("время")
ax.set_ylabel("удовольствие")
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(-0.05, 1.12)
save(fig, "reward-timing")


# ---------- мысленное сравнение ----------

fig, ax = new(size=(6.4, 4.0))
blank(ax, (-0.4, 9.4), (-0.4, 5.4))
box(ax, 3.0, 4.2, "желаемое будущее\n(я врач)", C.green, w=4.6, h=1.3, fs=13)
box(ax, 3.0, 0.8, "сейчас\n(долги, ржавая машина)", C.gray, w=4.6, h=1.3, fs=13)
ax.add_patch(FancyArrowPatch((6.0, 1.3), (6.0, 3.7), arrowstyle="<|-|>",
                             mutation_scale=22, color=C.blue, lw=2.8))
ax.text(6.4, 2.5, "контраст", va="center", fontsize=14, color=C.blue, fontweight="bold")
save(fig, "mental-contrast")


# ---------- процесс и продукт ----------

fig, (a1, a2) = new(nrows=2, size=(7.0, 3.6))
days = ["пн", "вт", "ср", "чт", "пт"]
for ax in (a1, a2):
    ax.set_xlim(-0.2, 10.6)
    ax.set_ylim(-0.7, 1.3)
    ax.axis("off")
for i, d in enumerate(days):
    x = i * 2.0
    a1.add_patch(Rectangle((x + 0.3, 0), 1.2, 0.9, color=C.blue, alpha=0.85))
    a1.text(x + 0.9, 0.45, "20 мин", ha="center", va="center", color="white", fontsize=11)
    a1.text(x + 0.9, -0.4, d, ha="center", color=C.gray, fontsize=11)
a1.set_title("процесс: отрезок работы каждый день", fontsize=13, color=C.blue, loc="left")
a2.add_patch(Rectangle((0.3, 0), 9.2, 0.9, facecolor="none", edgecolor=C.gray, lw=2,
                       linestyle="--"))
a2.text(4.9, 0.45, "5 решённых задач", ha="center", va="center", color=C.ink, fontsize=13)
a2.text(9.9, 0.45, "⚑", ha="left", va="center", color=C.red, fontsize=20)
a2.set_title("продукт: результат целиком", fontsize=13, color=C.gray, loc="left")
save(fig, "process-vs-product")


# ---------- многозадачность ----------

fig, (a1, a2) = new(nrows=2, size=(7.0, 4.6), gridspec_kw={"height_ratios": [1, 1.5]})
a1.set_xlim(0, 10)
a1.set_ylim(-0.2, 2.4)
a1.axis("off")
a1.add_patch(Rectangle((0, 1.4), 10, 0.7, color=C.blue, alpha=0.85))
a1.text(-0.1, 1.75, "одна задача", ha="right", va="center", fontsize=12)
seg = [C.blue, C.orange, C.purple] * 4
w = 10 / len(seg)
for i, col in enumerate(seg):
    a1.add_patch(Rectangle((i * w, 0.2), w, 0.7, color=col, alpha=0.85))
    if i:
        a1.plot([i * w] * 2, [0.05, 1.05], color=C.red, lw=2.5)
a1.text(-0.1, 0.55, "многозадачность", ha="right", va="center", fontsize=12)

x = np.linspace(0, 10, 500)
a2.plot(x, x * 0.6, color=C.blue, label="одна задача")
steps = 0.6 * x + 0.55 * np.floor(x / w)
a2.plot(x, steps, color=C.red, label="многозадачность")
a2.set_xlabel("время")
a2.set_ylabel("потрачено сил")
a2.set_xticks([])
a2.set_yticks([])
a2.legend(loc="upper left")
save(fig, "multitasking-switches")
