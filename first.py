import itertools

s1 = 'AAABBBCCAAA'  # todo groupby 之前要排序 相同元素在一起
for key, group in itertools.groupby(sorted(s1)):  ## 返回分组, 连续相同的 元素，以及元素出现的生成器
    print(key, list(group))
    # if 1==1:
    break
