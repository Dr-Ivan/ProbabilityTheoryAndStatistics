import matplotlib.pyplot as plt
import random


# Симуляция одной игры
def simulate_monty_hall(switch_choice):
    doors = ['goat', 'goat', 'car'] # создать три двери с одним выигрышем
    random.shuffle(doors)           # перемешать

    player_choice = random.randint(0, 2) # случайный выбор игрока
    
    # ведущий открывает дверь с козлом, не выбранную игроком
    host_choice = None
    for i in range(3):
        if i != player_choice and doors[i] == 'goat':
            host_choice = i
            break
    
    # если игрок меняет выбор, он выбирает оставшуюся дверь
    if switch_choice:
        for i in range(3):
            if i != player_choice and i != host_choice:
                player_choice = i
                break
    
    # проверка результата на выигрыш
    return doors[player_choice] == 'car'


# запуск нужного количества экспериментов и сбор статистики
def run_experiment(num_trials):
    wins_switch = 0     # побед при смене выбора
    wins_no_switch = 0  # побед без смены выбора
    
    for _ in range(num_trials):        # провести эксперименты и подсчитать победы
        if simulate_monty_hall(True):  # если выбор менять
            wins_switch += 1
        if simulate_monty_hall(False): # если выбор не менять
            wins_no_switch += 1
    
    prob_switch = wins_switch / num_trials      # вероятность при смене выбора
    prob_no_switch = wins_no_switch / num_trials    # вероятность при отсутствии смены выбора
    
    return prob_switch, prob_no_switch


# визуализация теоретической вероятности и экспериментальных данных
def visualize_results(prob_switch, prob_no_switch):
    strategies = ['Не менять', 'Менять']            # подписи диаграмм
    probabilities = [prob_no_switch, prob_switch]   # высота столбцов по экспериментальным данным
    theoretical = [1/3, 2/3]        # теоретические вероятности посчитаны из условия и не зависят от количества испытаний
    
    # график
    plt.figure(figsize=(8, 6))
    bars = plt.bar(strategies, probabilities, alpha=0.7, color=['red', 'green'])
    plt.axhline(y=theoretical[0], color='red', linestyle='--', alpha=0.7, label='Теоретическая 1/3')
    plt.axhline(y=theoretical[1], color='green', linestyle='--', alpha=0.7, label='Теоретическая 2/3')
    for bar, prob in zip(bars, probabilities):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{prob:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # настройки графика
    plt.ylabel('Вероятность выигрыша')
    plt.title('Парадокс Монти Холла')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 0.8)
    plt.tight_layout()
    plt.show()



def main():
    num_trials = 10_000 # количество испытаний
    
    print("=" * 40)
    print("Парадокс Монти Холла")
    print("=" * 40)
    
    prob_switch, prob_no_switch = run_experiment(num_trials)  # запуск нужного количества экспериментов 
    
    # вывод статистики 
    print(f"Количество испытаний: {num_trials}")
    print(f"Вероятность победы при смене выбора: {prob_switch:.4f} \nТеоретическая вероятность победы при смене выбора: 0.6667")
    print(f"Вероятность победы без смены: {prob_no_switch:.4f} \nТеоретическая вероятность победы без смены выбора: 0.3333")
    
    # визуализация на диаграмме
    visualize_results(prob_switch, prob_no_switch)



if __name__ == "__main__":
    main()