import random
from sys import argv, stderr
from string import ascii_lowercase as lower

def fmtKey(key):
    s = ''
    for k, v in key.items():
        s += f'{k}:{v}\n'
    return s[:-1]

def main():
    key = {k:v for k, v in zip(lower, random.sample(lower, len(lower)))}
    r = ''
    print(argv[1])
    with open(argv[1], 'r') as f:
        r = list(f.read())
        for i, ch in enumerate(r):
            if ch != ' ':
                r[i] = key[ch]
        r = ''.join(r)

    print(fmtKey(key), file=stderr)
    print(r)

if __name__=='__main__':
    main()
