aa = 1


def abc():
    return aa + 1


sw = {"A": 1, "B": abc()}

print(sw["B"])

#


args="C"

print(sw.get(args,"default value"))
