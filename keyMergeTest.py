from random import *
from string import ascii_lowercase as a_l

def pprint(key):
  print(key.values())

def genKey():
  return dict(zip(a_l, sample(a_l, len(a_l))))



def mergeKeys(key1, key2):
  rem = set(a_l)
  s1 = ''.join(key1.values())
  s2 = ''.join(key2.values())
  s3 = ''
  l = len(key1)

  for i in range(len(key1)):
    # t = (s1[i], s2[i])
    j, k = (s1[i], s2[i])
    # j, k = shuffle((s1[i], s2[i]))
    print(j)
    print(k)
    if (j in rem):
      s3 += j
    elif (k in rem):
      s3 += k
    else:
      s3 += sample(rem, 1)[0]
    print(s3)
    print('------')
    rem.remove(s3[-1])

k1 = genKey()
k2 = genKey()
pprint(k1)
pprint(k2)
print('------')
mergeKeys(k1, k2)