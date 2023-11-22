import random
import time
from concurrent.futures import ThreadPoolExecutor


def target_func1(t):
    print(t, time.time())
    time.sleep(t)
    return t


def target_func3(name):
    t = random.randint(0, 3)
    result = target_func1(t)
    return name, t, result


def run1():
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(target_func3, ['A', 'B', 'C']))

    for result in results:
        print(result)


if __name__ == '__main__':
    run1()
