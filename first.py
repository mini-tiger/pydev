def func1(func):
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs) * 2
    return wrapper

@func1
def foo(a):
    return a * 3

f=foo(2)
print(f)




