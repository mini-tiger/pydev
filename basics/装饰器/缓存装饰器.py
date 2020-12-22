from basics.clockdeco import clock
import functools


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


# @functools.lru_cache(maxsize=128, typed=True)
@functools.lru_cache() # 使用缓存
@clock
def fibonacci_cache(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == '__main__':
    print(fibonacci(6))
    print(fibonacci_cache(6))