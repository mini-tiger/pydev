import os


def r():
    a = dict()
    val_a = os.system('ipconfig')

    a["df"] = val_a
    return a


if __name__ == "__main__":
    a = r()
    print(a)
