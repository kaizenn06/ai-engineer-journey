if __name__ == "__main__" :
    t = int(input())
    for test in range(t) :
        print(f"Test {test + 1}:", end = " ")
        s1 = input()
        s2 = input()
        s1 = sorted(s1)
        s2 = sorted(s2)
        print("YES" if s1 == s2 else "NO")
