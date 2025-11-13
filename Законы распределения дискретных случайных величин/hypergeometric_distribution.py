import numpy as np
from scipy.stats import hypergeom
import matplotlib.pyplot as plt

print("=" * 60)
print("ГИПЕРГЕОМЕТРИЧЕСКОЕ РАСПРЕДЕЛЕНИЕ")
print("=" * 60)

# условие
print("ЗАДАЧА: Отбор кандидатов на собеседование")
print("Из 25 резюме, поступивших на вакансию, 10 - от кандидатов с опытом")
print("работы более 5 лет. HR случайным образом отбирает 6 резюме для")
print("приглашения на собеседование. Найти закон распределения числа")
print("кандидатов с большим опытом среди отобранных и вероятность не отобрать ни одного кандидата с опытом. \n")

# параметры распределения
N = 25  # общее количество резюме
M = 10  # количество резюме с большим опытом
n = 6   # количество отобранных резюме

# объект гипергеометрического распределения
hypergeom_dist = hypergeom(N, M, n)

# возможные значения
X = np.arange(0, n + 1)
probabilities = hypergeom_dist.pmf(X)

# печать закона распределения
print("ЗАКОН РАСПРЕДЕЛЕНИЯ:")
for i, (x, prob) in enumerate(zip(X, probabilities)):
    print(f"P(X = {x}) = {prob:.4f}")

print()
print(f"Математическое ожидание: M(X) = {hypergeom_dist.mean():.4f}")
print(f"Дисперсия: D(X) = {hypergeom_dist.var():.4f}")
print(f"Среднее квадратическое отклонение: σ(X) = {hypergeom_dist.std():.4f}")

max_prob = probabilities.max()
mode_indices = [x for x, prob in zip(X, probabilities) if abs(prob - max_prob) < 1e-6]
print(f"Мода: {X[mode_indices]}")

# второй вопрос задачи
prob_no_experience = hypergeom_dist.pmf(0)
print(f"\nВероятность не отобрать ни одного кандидата с опытом: {prob_no_experience:.4f}")
print()

# многоугольник распределения
plt.figure(figsize=(10, 6))
plt.plot(X, probabilities, 'mo-', linewidth=2, markersize=8)
plt.title('Гипергеометрическое распределение\nКандидаты с опытом среди отобранных')
plt.xlabel('Число кандидатов с большим опытом')
plt.ylabel('Вероятность')
plt.grid(True, alpha=0.3)
plt.xticks(X)

for x, prob in zip(X, probabilities):
    plt.annotate(f'{prob:.3f}', (x, prob), textcoords="offset points", 
                 xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()