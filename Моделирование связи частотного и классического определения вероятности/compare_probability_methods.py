import matplotlib.pyplot as plt
import random
import math

# условия задачи
total_balls = 12  # всего шаров
red_balls = 6     # сколько из них красных
blue_balls = 6    # сколько из них синих
sample_size = 6   # нужно достать
target_red = 3    # сколько красных должно быть среди извлеченных

# классическая вероятность (комбинаторика)
def classical_probability():
    # расчет по формуле C(red_balls, target_red) * C(blue_balls, sample_size - target_red) / C(total_balls, sample_size)
    c_red = math.comb(red_balls, target_red)                 # комбинации (сочетания) нужного количества красных
    c_blue = math.comb(blue_balls, sample_size - target_red) # комбинации (сочетания) синих в оставшихся после красных местах
    c_total = math.comb(total_balls, sample_size)            # всего комбинаций 
    return c_red * c_blue / c_total

# моделирование одного эксперимента (возвращается булево значение - успех (нужное количество красных шаров) или нет)
def simulate_experiment():
    urn = ['red'] * red_balls + ['blue'] * blue_balls  # создать коробку по условию 
    sample = random.sample(urn, sample_size)           # взять случайный образец нужного размера
    return sample.count('red') == target_red           # проверить успех эксперимента

# эксперименты
classical_p = classical_probability() # классическая вероятность
print("=" * 50)
print("СВЯЗЬ ЧАСТОТНОГО И КЛАССИЧЕСКОГО ОПРЕДЕЛЕНИЯ")
print("=" * 50)

# условия задачи
print(f"Коробка: {red_balls} красных, {blue_balls} синих шаров")
print(f"Выбираем {sample_size} шаров, хотим {target_red} красных")
print(f"Классическая вероятность: {classical_p:.4f}")
print()

# эксперименты с разным количеством испытаний
experiment_sizes = [10, 50, 100, 500, 1000, 5000, 10_000, 100_000]
frequencies = []

print("Результаты экспериментов:")
print(f"{'N':>8} | {'Частотная ':>8}| {'Отклонение':>10}")
print("-" * 35)

# для каждого указанного количества экспериментов 
for N in experiment_sizes:
    successes = 0
    for _ in range(N): # провести столько экспериментов 
        if simulate_experiment(): # подсчитать успешные
            successes += 1
    
    freq = successes / N            # найти частотную вероятность
    frequencies.append(freq)        # записать (для графика)
    deviation = abs(freq - classical_p)     # отклонение от классической вероятности
    print(f"{N:>8} | {freq:>8.4f} | {deviation:>10.4f}")    # вывести строку таблицы
print("-" * 35)


# график
plt.figure(figsize=(10, 6))
plt.plot(experiment_sizes, frequencies, 'bo-', linewidth=2, markersize=6, label='Частотная вероятность')
plt.axhline(y=classical_p, color='red', linestyle='--', linewidth=2, label='Классическая вероятность')

# настройки графика
plt.xscale('log')
plt.xlabel('Количество испытаний (N)')
plt.ylabel('Вероятность')
plt.title('Стремление частотной вероятности к классической')
plt.grid(True, alpha=0.3)
plt.legend()
plt.text(experiment_sizes[0], classical_p + 0.02, f'Классическая вероятность: {classical_p:.4f}', 
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.tight_layout()
plt.show()
