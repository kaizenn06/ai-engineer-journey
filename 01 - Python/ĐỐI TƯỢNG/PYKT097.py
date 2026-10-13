import re

if __name__ == "__main__" :
    a = []
    while True :
        try :
            s = ' '.join(input().strip().lower().split()).capitalize()
            s = re.sub(r'\s+([.,!?;:])', r'\1', s)
            if s and s[-1] not in '.!?':
                s += '.'
            a.append(s)
        except EOFError :
            break
    print(*a, sep= '\n')
        