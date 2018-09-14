# coding:utf-8
import itertools

print list(itertools.combinations(range(3), 2)) #[0,1,2]这三个数，排序集合的可能，不包含重复，[(0, 1), (0, 2), (1, 2)]
print list(itertools.combinations_with_replacement(range(3), 2))  # [0,1,2]这三个数，排序集合的可能，包含重复，[(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]

print list(itertools.dropwhile(lambda x: x < 5, range(10)))  # 小于的元素被drop  [5, 6, 7, 8, 9]

print list(itertools.combinations("abc",2)) # [('a', 'b'), ('a', 'c'), ('b', 'c')]   不包含重复，两两组合，（元素一样，顺序不一样，算重复）
print list(itertools.permutations("abc",2)) # [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')] 每个元素和另外两个，两两组合 （元素一样，顺序不一样，不算重复）

print list(itertools.product("abc","123")) # 类似excel表里 列的定义 [('a', '1'), ('a', '2'), ('a', '3'), ('b', '1'), ('b', '2'), ('b', '3'), ('c', '1'), ('c', '2'), ('c', '3')]


