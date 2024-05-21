import numpy as np


def printN(sep, v):
    fmt = "%s"
    if v == 0:
        fmt = fmt + "%4d"
    else:
        fmt = fmt + "%3.2f"
    s = fmt % (sep, v)
    print(s, end='')


def num_format(loadtxt, outputText):
    data = np.loadtxt(loadtxt)
    # print(data.shape)
    # width, height = range(213), range(213)
    width, height = range(data.shape[0]), range(data.shape[1])
    for i in width:
        print()
        for j in height:
            if j == i:
                data[i][j] = 1.00
            if j == 0:
                printN("", data[i][j])
            else:
                printN(" ", data[i][j])
    # Modify the data
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if j == i:
                data[i][j] = 1.00

    # Define the output file path
    output_file_path = outputText

    # Open the output file for writing
    with open(output_file_path, "w") as output_file:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if j == 0:
                    output_file.write("{:.2f}".format(data[i][j]))
                else:
                    output_file.write(" {:.2f}".format(data[i][j]))
            output_file.write("\n")


if __name__ == "__main__":
    num_format("/mnt/score.txt", "/mnt/modified_score.txt")
    # np.savetxt("C:\\Users\\zhang.hu5\\Desktop\\score2.txt", data, fmt=fmt)
