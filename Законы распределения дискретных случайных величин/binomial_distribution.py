import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

print("=" * 60)
print("БИНОМИАЛЬНОЕ РАСПРЕДЕЛЕНИЕ")
print("=" * 60)

# условие 
print("ЗАДАЧА: Контроль качества на производстве")
print("На заводе производится сборка смартфонов. Вероятность того, что")
print("собранный смартфон будет иметь дефект, составляет 0.1. За день")
print("собирается 8 смартфонов. Найти закон распределения числа дефектных")
print("смартфонов среди собранных за день.\n")

# параметры распределения
n = 8       # количество испытаний
p = 0.1     # вероятность дефекта

# объект биномиального распределения
binom_dist = binom(n, p)

# возможные значения
X = np.arange(0, n + 1)
probabilities = binom_dist.pmf(X)

# печать закона распределения
print("ЗАКОН РАСПРЕДЕЛЕНИЯ:")
for i, (x, prob) in enumerate(zip(X, probabilities)):
    print(f"P(X = {x}) = {prob:.4f}")

print()
print(f"Математическое ожидание: M(X) = {binom_dist.mean():.4f}")
print(f"Дисперсия: D(X) = {binom_dist.var():.4f}")
print(f"Среднее квадратическое отклонение: σ(X) = {binom_dist.std():.4f}")

max_prob = probabilities.max()
mode_indices = [x for x, prob in zip(X, probabilities) if abs(prob - max_prob) < 1e-6]
print(f"Мода: {X[mode_indices]}")
print()


# многоугольник распределения
plt.figure(figsize=(10, 6))
plt.plot(X, probabilities, 'bo-', linewidth=2, markersize=8)
plt.title('Биномиальное распределение\nЧисло дефектных смартфонов за день')
plt.xlabel('Число дефектных смартфонов')
plt.ylabel('Вероятность')
plt.grid(True, alpha=0.3)
plt.xticks(X)

for x, prob in zip(X, probabilities):
    plt.annotate(f'{prob:.3f}', (x, prob), textcoords="offset points", 
                 xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()