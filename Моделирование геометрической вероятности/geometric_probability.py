import matplotlib.pyplot as plt
import random
import math

# параметры
square_side = 2  # сторона квадрата
circle_radius = 1  # радиус круга
N = 1_000  # количество дротиков (экспериментов)

points = [] # массив случайных точек
hits = 0    # счетчик попаданий в круг

# симуляция N экспериментов
for i in range(N):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    points.append((x, y))
    
    # проверка попадания
    if x**2 + y**2 <= circle_radius**2:
        hits += 1


empirical_prob = hits / N   # эмпирическая вероятность (по симуляции)
theoretical_prob = math.pi * circle_radius**2 / square_side**2 # теоретическая вероятность (отношение площадей)

# результаты
print("=" * 50)
print("ГЕОМЕТРИЧЕСКАЯ ВЕРОЯТНОСТЬ")
print("=" * 50)
print(f"Количество точек: {N}")
print(f"Попаданий в круг: {hits}")
print(f"Эмпирическая вероятность: {empirical_prob:.4f}")
print(f"Теоретическая вероятность: π * {circle_radius**2} / {square_side**2}  = {theoretical_prob:.4f}")
print("=" * 50)

# картинка
plt.figure(figsize=(8, 8))

# квадрат
square = plt.Rectangle((-1, -1), 2, 2, fill=False, color='black', linewidth=2)
plt.gca().add_patch(square)

# круг
circle = plt.Circle((0, 0), 1, fill=False, color='red', linewidth=2)
plt.gca().add_patch(circle)

# точки в разные группы -> попадания и промахи
hits_x = [p[0] for p in points if p[0]**2 + p[1]**2 <= 1]
hits_y = [p[1] for p in points if p[0]**2 + p[1]**2 <= 1]
miss_x = [p[0] for p in points if p[0]**2 + p[1]**2 > 1]
miss_y = [p[1] for p in points if p[0]**2 + p[1]**2 > 1]

# расставить точки
plt.scatter(hits_x, hits_y, color='green', s=10, alpha=0.7, label='Попадания в круг')
plt.scatter(miss_x, miss_y, color='blue', s=10, alpha=0.7, label='Промахи')

# настройки графика
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)
plt.gca().set_aspect('equal')
plt.grid(True, alpha=0.3)
plt.legend()
plt.title(f'Геометрическая вероятность (N={N})')
plt.xlabel('X')
plt.ylabel('Y')
plt.text(-1.1, 1.1, f'Теоретическая: π * {circle_radius**2} / {square_side**2} ≈ {theoretical_prob:.4f}\nЭмпирическая: {empirical_prob:.4f}', 
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()