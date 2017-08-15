def readfile():
    f = open('help.txt', 'r')

    file_contents = f.read()

    print(file_contents)

    f.close()


if __name__ == "__main__":
    readfile()