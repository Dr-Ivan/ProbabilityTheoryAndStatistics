import numpy as np
from scipy.stats import geom
import matplotlib.pyplot as plt

print("=" * 60)
print("ГЕОМЕТРИЧЕСКОЕ РАСПРЕДЕЛЕНИЕ")
print("=" * 60)

# условие
print("ЗАДАЧА: Поиск редкого растения")
print("Биолог ищет редкое растение в лесу. Вероятность найти растение")
print("на одном участке составляет 0.15. Найти закон распределения числа")
print("обследованных участков до первого нахождения растения и вероятность найти растение не ранее 5-го участка. \n")

# параметр распределения
p = 0.15

# объект геометрического распределения
geom_dist = geom(p)

# возможные значения
K = np.arange(1, 21)
probabilities = geom_dist.pmf(K)

# печать закона распределения
print("ЗАКОН РАСПРЕДЕЛЕНИЯ:")
for i, (k, prob) in enumerate(zip(K, probabilities)):
    print(f"P(X = {k}) = {prob:.4f}")

print()
print(f"Математическое ожидание: M(X) = {geom_dist.mean():.4f}")
print(f"Дисперсия: D(X) = {geom_dist.var():.4f}")
print(f"Среднее квадратическое отклонение: σ(X) = {geom_dist.std():.4f}")

max_prob = probabilities.max()
mode_indices = [k for k, prob in zip(K, probabilities) if abs(prob - max_prob) < 1e-6]
print(f"Мода: {K[mode_indices]}")

# второй вопрос задачи
prob_at_least_5 = 1 - geom_dist.cdf(4)
print(f"\nВероятность найти растение не ранее 5-го участка: {prob_at_least_5:.4f}")
print()


# многоугольник распределения
plt.figure(figsize=(10, 6))
plt.plot(K, probabilities, 'go-', linewidth=2, markersize=8)
plt.title('Геометрическое распределение\nЧисло участков до нахождения растения')
plt.xlabel('Номер участка, где найдено растение')
plt.ylabel('Вероятность')
plt.grid(True, alpha=0.3)
plt.xticks(K)

for k, prob in zip(K, probabilities):
    plt.annotate(f'{prob:.3f}', (k, prob), textcoords="offset points", 
                 xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()