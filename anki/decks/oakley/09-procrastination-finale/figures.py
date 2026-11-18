"""Схемы к главе 9. Рисунок _36.jpg в книге декоративный, в карточках не используется."""
import sys
from pathlib import Path
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import new, save, C


def box(ax, x, y, text, color, w=2.8, h=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                              facecolor="white", edgecolor=color, linewidth=2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", color=color, fontsize=13)


def arrow(ax, start, end, color=C.gray):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", color=color, lw=2))


def canvas(size=(8.2, 3.0)):
    fig, ax = new(size=size)
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(-0.2, 3)
    ax.axis("off")
    return fig, ax


fig, ax = canvas()
box(ax, 0, 1.6, "Пауза", C.blue)
box(ax, 3.6, 1.6, "Оценить\nприоритеты", C.blue)
box(ax, 7.2, 1.6, "Выбрать\nдействие", C.green)
box(ax, 0, 0, "Избегание", C.red)
box(ax, 3.6, 0, "Временное\nоблегчение", C.gray)
box(ax, 7.2, 0, "Дело\nотложено", C.red)
for y in (2.05, 0.45):
    arrow(ax, (2.85, y), (3.5, y))
    arrow(ax, (6.45, y), (7.1, y))
save(fig, "pause-or-avoid")

fig, ax = canvas((8.2, 2.2))
box(ax, 0, 1, "Условие\nзадачи", C.blue)
box(ax, 3.6, 1, "Принцип\nи его условия", C.green)
box(ax, 7.2, 1, "Метод\nрешения", C.blue)
arrow(ax, (2.85, 1.45), (3.5, 1.45))
arrow(ax, (6.45, 1.45), (7.1, 1.45))
save(fig, "principle-first")

fig, ax = canvas((8.2, 3.4))
box(ax, 0, 1, "Большое\nзадание", C.gray)
for y, label in [(2, "1. Прочитать условие"), (1, "2. Выписать данные"), (0, "3. Нарисовать схему")]:
    box(ax, 5.1, y, label, C.green if y == 2 else C.gray, w=4.7, h=0.75)
    arrow(ax, (2.9, 1.45), (4.95, y + 0.375))
ax.text(7.45, 2.86, "Сейчас: только первый шаг", ha="center", color=C.green, fontsize=13)
save(fig, "microtask")

fig, ax = canvas((8.2, 2.8))
box(ax, 0, 1, "Уведомления\nвыключены", C.gray)
box(ax, 3.6, 1, "Одна задача\n25 минут", C.blue)
box(ax, 7.2, 1, "Перерыв", C.green)
arrow(ax, (2.85, 1.45), (3.5, 1.45))
arrow(ax, (6.45, 1.45), (7.1, 1.45))
ax.text(5, 0.35, "На время таймера остаёмся с выбранной задачей", ha="center", fontsize=13, color=C.ink)
save(fig, "focus-block")
