import multiprocessing


def func_int(num):
    num.value = 10.78  # 子进程改变数值的值，主进程跟着改变


def func_Array(num):
    num[2] = 9999  # 子进程改变数组，主进程跟着改变


def func_listdict(mydict, mylist):
    mydict["index1"] = "aaaaaa"  # 子进程改变dict,主进程跟着改变
    mydict["index2"] = "bbbbbb"
    mylist.append(11)  # 子进程改变List,主进程跟着改变
    mylist.append(22)
    mylist.append(33)


if __name__ == "__main__":
    num = multiprocessing.Value("d", 10.0)  # d表示数值,主进程与子进程共享这个value。（主进程与子进程都是用的同一个value）
    print(num.value)

    p = multiprocessing.Process(target=func_int, args=(num,))
    p.start()
    p.join()

    print(num.value)

    print("-"*50)
    num = multiprocessing.Array("i", [1, 2, 3, 4, 5])  # 主进程与子进程共享这个数组
    print(num[:])

    p = multiprocessing.Process(target=func_Array, args=(num,))
    p.start()
    p.join()

    print(num[:])

    print("-"*50)

    with multiprocessing.Manager() as MG:  # 重命名
        mydict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        mylist = multiprocessing.Manager().list(range(5))  # 主进程与子进程共享这个List

        p = multiprocessing.Process(target=func_listdict, args=(mydict, mylist))
        p.start()
        p.join()

        print(mylist)
        print(mydict)
