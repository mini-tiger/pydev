def abc(a, b: int) -> int:
    return a + b


from typing import List, Dict, Tuple
from typing import Any

Vector = List[float]  # todo Vector 是 List[float] 的别名

'''
其它例子
ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]
'''


def scale(scalar: float, vector: list) -> list:  # 这里也能返回，类型注释 不是 强制要求
    # return [scalar + num for num in vector]
    return 1


def scale1(scalar: float, vector: Vector) -> Vector:
    return [scalar + num for num in vector]


def foo(item: Any) -> int:  # todo 任何类型都可以传入
    # Typechecks; 'item' could be any type,
    # and that type might have a 'bar' method
    print(item)


from typing import TypeVar, Generic
from logging import Logger

T = TypeVar('T')
S = TypeVar('S', int, str)


class LoggedVar(Generic[T, S]):
    def __init__(self, value: T, name: S, logger: Logger) -> None:  # 每个类型要单独定义，T,S
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('%s: %s', self.name, message)


from typing import Iterable


def zero_all_vars(vars: Iterable[LoggedVar[int, str]]) -> None:
    for var in vars:
        print(var.get())
        var.set(0)
        print(var.get())
        print("===="*20)


if __name__ == "__main__":
    print(abc(1, 2))
    # typechecks; a list of floats qualifies as a Vector.
    print(scale(2.0, [1.0, -4.2, 5.4, 1]))
    print(scale1(2.0, [1.0, -4.2, 5.4, 1]))
    foo(1)
    foo("1")
    foo([1])
    foo({"a": 2})
    a = Logger("abc")

    zero_all_vars([LoggedVar(1, "1", a),LoggedVar(2, "2", a)])
