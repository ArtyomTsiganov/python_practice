import time

import matplotlib.pyplot as plt
from subpref import fast, brutforce
from generator import generate


def timer(words, method):
    start_time = time.time()
    method(words)
    end_time = time.time()
    return end_time-start_time


def get_times(counts):
    fast_times = []
    brutforce_times = []
    for count in counts:
        words = generate(length=10, total=count, equals=True, answer="Python")
        brutforce_times.append(timer(words, brutforce))
        fast_times.append(timer(words, fast))
    return brutforce_times, fast_times


def main():
    min_count = 5
    max_count = 100
    step = 5
    counts = [x for x in range(min_count,max_count+step,step)]
    brutforce_times, fast_times = get_times(counts)
    plt.xlabel('Кол-во слов')
    plt.ylabel('Время выполнения')
    plt.title('Сравнение двух методов')
    plt.plot(counts, brutforce_times, color='green', marker='o', markersize=7, label="brutforce")
    plt.plot(counts, fast_times, color='blue', marker='o', markersize=7, label="fast_and_clever")
    plt.show()


if __name__ == '__main__':
    main()
