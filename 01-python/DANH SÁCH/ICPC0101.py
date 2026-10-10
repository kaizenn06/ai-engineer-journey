if __name__ == "__main__" :
    n = int(input())
    a = list(map(int, input().split()))
    st = []
    for i in range(n) :
        if st and (st[-1] + a[i]) % 2 == 0 :
            st.pop()
        else : 
            st.append(a[i])
    print(len(st)) 
