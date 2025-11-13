import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

print("=" * 60)
print("РАСПРЕДЕЛЕНИЕ ПУАССОНА")
print("=" * 60)

# условие
print("ЗАДАЧА: Система обслуживания вызовов")
print("В колл-центр интернет-магазина в среднем поступает 4 звонка в час.")
print("Найти закон распределения числа звонков за час и вероятность того,")
print("что за час поступит более 6 звонков.\n")

# параметр распределения 
lmbda = 4  # среднее количество звонков в час

# объект распределения Пуассона
poisson_dist = poisson(lmbda)

# возможные значения
X = np.arange(0, 16)
probabilities = poisson_dist.pmf(X)

# печать закона распределения
print("ЗАКОН РАСПРЕДЕЛЕНИЯ:")
for i, (x, prob) in enumerate(zip(X, probabilities)):
    print(f"P(X = {x}) = {prob:.4f}")

print()
print(f"Математическое ожидание: M(X) = {poisson_dist.mean():.4f}")
print(f"Дисперсия: D(X) = {poisson_dist.var():.4f}")
print(f"Среднее квадратическое отклонение: σ(X) = {poisson_dist.std():.4f}")

max_prob = probabilities.max()
mode_indices = [x for x, prob in zip(X, probabilities) if abs(prob - max_prob) < 1e-6]
print(f"Мода: {X[mode_indices]}")

# второй вопрос задачи
prob_more_than_6 = 1 - poisson_dist.cdf(6)
print(f"\nВероятность получить более 6 звонков: {prob_more_than_6:.4f}")
print()


# многоугольник распределения
plt.figure(figsize=(10, 6))
plt.plot(X, probabilities, 'ro-', linewidth=2, markersize=8)
plt.title('Распределение Пуассона\nЧисло звонков в колл-центр за час')
plt.xlabel('Число звонков')
plt.ylabel('Вероятность')
plt.grid(True, alpha=0.3)
plt.xticks(X)

for x, prob in zip(X, probabilities):
    if prob >= 0.001:  # только значимые вероятности
        plt.annotate(f'{prob:.3f}', (x, prob), textcoords="offset points", 
                     xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()