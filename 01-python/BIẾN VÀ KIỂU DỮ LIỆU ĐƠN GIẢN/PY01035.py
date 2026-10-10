if __name__ == "__main__" :
    binary = input()
    s = ""
    while binary :
        x = binary[-3:]
        binary = binary[:-3]
        s += str(int(x, 2))
    print(s[::-1])

