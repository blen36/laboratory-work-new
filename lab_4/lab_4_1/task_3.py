import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(6, 7))

# Цвет обводки
outline = "#3E0A6A"

# --- Ноги ---
leg_left = patches.Rectangle((-3, -13), 1.5, 4, facecolor="#7D4CAF", edgecolor=outline, lw=2)
leg_right = patches.Rectangle((1.5, -13), 1.5, 4, facecolor="#7D4CAF", edgecolor=outline, lw=2)
ax.add_patch(leg_left)
ax.add_patch(leg_right)

# --- Шапка ---
hat = patches.Polygon([[-3, 9], [3, 9], [0, 14.5]], closed=True, facecolor="#E65100", edgecolor=outline, lw=2)
ax.add_patch(hat)

# --- Помпон ---
pom = patches.Circle((0, 14.5), 1.2, facecolor="#AD1457", edgecolor=outline, lw=2)
ax.add_patch(pom)

# --- Тело ---
body = patches.Circle((0, 0), 10, facecolor="#7D4CAF", edgecolor=outline, lw=2)
ax.add_patch(body)

# --- Уши ---
ear_left = patches.Polygon([[-7.58, 6.52], [-3.97, 9.16], [-7, 11.55]], closed=True, facecolor="#7D4CAF", edgecolor=outline, lw=2)
ear_right = patches.Polygon([[7.58, 6.52], [3.97, 9.16], [7, 11.55]], closed=True, facecolor="#7D4CAF", edgecolor=outline, lw=2)
ax.add_patch(ear_left)
ax.add_patch(ear_right)

# --- Глаза ---
eye_left = patches.Ellipse((-3.5, 3), 5, 6, facecolor="white", edgecolor="black", lw=2)
eye_right = patches.Ellipse((3.5, 3), 5, 6, facecolor="white", edgecolor="black", lw=2)
ax.add_patch(eye_left)
ax.add_patch(eye_right)

# --- Зрачки ---
pupil_left = patches.Circle((-3, 3.5), 0.8, facecolor="black", edgecolor="black", lw=1)
pupil_right = patches.Circle((3, 3.5), 0.8, facecolor="black", edgecolor="black", lw=1)
ax.add_patch(pupil_left)
ax.add_patch(pupil_right)

# --- Нос ---
beak = patches.Ellipse((0, 0), 3.5, 2.5, facecolor="#F57C00", edgecolor="darkred", lw=2)
ax.add_patch(beak)

# --- Крылья ---
wing_left = patches.Ellipse((-10, -2), 3, 7, facecolor="#9B59B6", edgecolor=outline, lw=2)
wing_right = patches.Ellipse((10, -2), 3, 7, facecolor="#9B59B6", edgecolor=outline, lw=2)
ax.add_patch(wing_left)
ax.add_patch(wing_right)

# --- Живот ---
stomach = patches.Ellipse((0, -5), 10, 5, facecolor="#9B59B6", edgecolor=outline, lw=2)
ax.add_patch(stomach)

# --- Surprise ---
heart_left = patches.Circle((9.5, 14.3), 0.55, color="red")
heart_right = patches.Circle((10.5, 14.3), 0.55, color="red")
ax.add_patch(heart_left)
ax.add_patch(heart_right)

triangle = patches.Polygon([[9, 14.1], [11, 14.1], [10, 12.8]], closed=True, color="red")
ax.add_patch(triangle)
ax.text(8.2, 11.5, "Ирина Николаевна,\nэто Вам.", fontsize=6, color="black", ha="left")

# --- Настройки отображения ---
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 18)
ax.axis("off")
ax.set_title("Что-то типо Совуньи")

plt.show()
