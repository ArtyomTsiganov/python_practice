import time

import matplotlib.pyplot as plt
from pygments.lexer import words

import async_phil
import phil


def timer(words, method):
    start_time = time.time()
    method(words)
    end_time = time.time()
    return end_time-start_time


def get_times(words):
    async_phil_data = []
    phil_data= []
    for word in words:
        phil_data.append(timer(word, phil.main))
        print("done 1")
        async_phil_data.append(timer(word, async_phil.main))
        print("done 2")
    return phil_data, async_phil_data


def main():
    words = ["Наука", "Математика", "Самолёт"]
    sync_times, async_times = get_times(words)
    print(sync_times, async_times)
    plt.xlabel('Кол-во слов')
    plt.ylabel('Время выполнения')
    plt.title('Сравнение двух методов')
    plt.plot(words, sync_times, color='green', marker='o', markersize=7, label="sync")
    plt.plot(words, async_times, color='blue', marker='o', markersize=7, label="async")
    plt.show()


if __name__ == '__main__':
    main()
