import random 
from math import factorial


def c(n, k):
    if k < 0 or k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n-k))


def calculate_probability(white1, black1, white2, black2, moves, extract):
    N1 = white1 + black1
    N2 = white2 + black2
    total = 0.0
    for x in range(max(0, moves - black1), min(moves, white1) + 1):
        p_transfer = c(white1, x) * c(black1, moves - x) / c(N1, moves)
        
        if white2 + x < extract:
            p_draw = 0.0
        else:
            p_draw = c(white2 + x, extract) / c(N2 + moves, extract)

        total += p_transfer * p_draw
    return total



white1 = int(input("Введите количество белых шаров в первой коробке "))
black1 = int(input("Введите количество черных шаров в первой коробке "))
white2 = int(input("Введите количество белых шаров во второй коробке "))
black2 = int(input("Введите количество черных шаров во второй коробке "))
moves = int(input("Сколько перекладывать на первом шаге "))
extract = int(input("Сколько белых должно быть в итоге "))
success = 0
experiments = 1_000_000

print(f"Вероятность вытащить {extract} белых шаров на втором шаге (по формуле): ", calculate_probability(white1, black1, white2, black2, moves, extract))


for i in range(experiments):
    box1 = ['b'] * black1 + ['w'] * white1
    box2 = ['b'] * black2 + ['w'] * white2
    res = []

    for _ in range(moves):
        box2.append(box1.pop(random.randint(0, len(box1)-1)))

    for _ in range(extract):
        res.append(box2.pop(random.randint(0, len(box2)-1)))

    if all([x == 'w' for x in res]):
        success += 1

print(f"Вероятность вытащить {extract} белых шаров на втором шаге (полная симуляция): ", success/experiments)


    



