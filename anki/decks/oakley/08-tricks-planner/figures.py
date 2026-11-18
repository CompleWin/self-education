"""Картинки к главе 8 «Думай как математик»: способы, советы и хитрости."""
# media/book-zombie-list.png взята из книги (рисунок в начале главы 8), этот файл её не рисует.

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import C, new, save  # noqa: E402


def box(ax, x, y, w, h, color, fill=0.12, lw=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.05,rounding_size=0.2",
                                facecolor=to_rgba(color, fill), edgecolor=color, lw=lw))


def arrow(ax, p, q, color=C.gray, lw=2.2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=18,
                                 color=color, lw=lw, connectionstyle=f"arc3,rad={rad}"))


def blank(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


# ---------- нежелание начинать ----------

t = np.linspace(0, 10, 400)
start = 4.0
u = np.where(t < start, 0.55 + 0.11 * t, 0.87 * np.exp(-(t - start) / 0.9) + 0.12)

fig, ax = new(size=(6.6, 3.8))
ax.axvspan(0, start, color=C.red, alpha=0.06)
ax.plot(t, u, color=C.red)
ax.axvline(start, color=C.gray, ls="--", lw=1.5)
ax.text(start + 0.15, 1.02, "начал работу", fontsize=12, color=C.ink, va="top")
ax.text(1.9, 0.38, "до начала:\nне хочется", ha="center", fontsize=12, color=C.red)
ax.text(7.3, 0.35, "стало легче", ha="center", fontsize=13, color=C.green)
ax.set_xlabel("время")
ax.set_ylabel("нежелание")
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 10)
ax.set_ylim(0, 1.08)
ax.grid(False)
save(fig, "start-reluctance")


# ---------- недельный и дневной списки ----------

fig, ax = new(size=(7.4, 4.0))
blank(ax, (-0.3, 14.3), (-1.2, 7.4))

box(ax, 0, 0, 5.4, 6.2, C.blue)
ax.text(2.7, 6.75, "неделя", ha="center", fontsize=15, color=C.blue, fontweight="bold")
for i in range(10):
    y = 5.6 - i * 0.56
    ax.plot([0.5, 0.75], [y, y], color=C.blue, lw=3)
    ax.plot([1.0, 4.4 - 0.25 * (i % 3)], [y, y], color=C.gray, lw=2)
ax.text(2.7, -0.7, "не больше 20 дел", ha="center", fontsize=12, color=C.ink)

box(ax, 8.6, 1.4, 5.4, 3.6, C.green)
ax.text(11.3, 5.55, "завтра", ha="center", fontsize=15, color=C.green, fontweight="bold")
for i in range(5):
    y = 4.4 - i * 0.62
    ax.add_patch(Rectangle((9.1, y - 0.18), 0.36, 0.36, fill=False, ec=C.green, lw=1.8))
    ax.plot([9.8, 13.2 - 0.3 * (i % 2)], [y, y], color=C.gray, lw=2)
ax.text(11.3, 0.7, "5–10 дел", ha="center", fontsize=12, color=C.ink)

arrow(ax, (5.7, 3.2), (8.3, 3.2), color=C.ink)
ax.text(7.0, 3.65, "каждый\nвечер", ha="center", va="bottom", fontsize=12, color=C.ink)
save(fig, "weekly-daily-lists")


# ---------- план дня: лягушка утром, конец в 17:00 ----------

fig, ax = new(size=(7.8, 2.8))
blank(ax, (7.0, 23.6), (-1.6, 2.6))
y0, h = 0.0, 1.0
ax.add_patch(Rectangle((8, y0), 2.2, h, fc=to_rgba(C.orange, 0.35), ec=C.orange, lw=2))
ax.text(9.1, y0 + h / 2, "лягушка", ha="center", va="center", fontsize=11, color=C.ink)
for a, b in [(10.4, 12.0), (12.8, 14.4), (14.6, 16.8)]:
    ax.add_patch(Rectangle((a, y0), b - a, h, fc=to_rgba(C.blue, 0.18), ec=C.blue, lw=1.8))
ax.text(13.6, 1.55, "дела из списка", ha="center", fontsize=12, color=C.blue)
ax.add_patch(Rectangle((17, y0), 6, h, fc=to_rgba(C.green, 0.18), ec=C.green, lw=1.8))
ax.text(20, y0 + h / 2, "отдых", ha="center", va="center", fontsize=13, color=C.green)
ax.plot([17, 17], [-0.4, 1.9], color=C.red, lw=2.5)
ax.text(17, 2.05, "конец работы", ha="center", fontsize=12, color=C.red)
for hr in [8, 12, 17, 23]:
    ax.text(hr, -0.85, f"{hr}:00", ha="center", fontsize=11, color=C.gray)
save(fig, "day-plan")


# ---------- журнал прокрастинации ----------

rows = [
    ("задачи по матанализу", "пришло сообщение", "час в телефоне"),
    ("конспект лекции", "сел за ноутбук дома", "видео на YouTube"),
    ("лаба по ML", "ошибка в коде", "пошёл за чаем"),
]
head = ("не сделано", "сигнал", "реакция")
cols = [C.ink, C.orange, C.red]

fig, ax = new(size=(7.8, 2.6))
ax.axis("off")
xs = [0.02, 0.37, 0.69]
for x, s, c in zip(xs, head, cols):
    ax.text(x, 0.88, s, fontsize=13, fontweight="bold", color=c, transform=ax.transAxes)
ax.plot([0.0, 1.0], [0.8, 0.8], color=C.gray, lw=1.5, transform=ax.transAxes)
for i, r in enumerate(rows):
    y = 0.6 - i * 0.24
    for x, s in zip(xs, r):
        ax.text(x, y, s, fontsize=12, color=C.ink, transform=ax.transAxes, va="center")
save(fig, "procrastination-log")
