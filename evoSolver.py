from string import ascii_lowercase as a_l
import random
from collections import defaultdict, Counter
from statistics import mean
import signal
import sys

# probability distribution for modern english
pdf = Counter({'a': 0.08166999999999999, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06326999999999999, 't': 0.09055999999999999, 'u': 0.02758, 'v': 0.00978, 'w': 0.0236, 'x': 0.0015, 'y': 0.01974, 'z': 0.00074})
wordListFile = 'words.txt'
with open(wordListFile, 'r') as f:
  wordlist = {word.strip().lower() for word in f.read().split('\n') if len(word.strip()) > 0}

def decode(key):
  global cypherText
  return ''.join(map(lambda c: key.get(c) if c in key else c, cypherText))

def fitness(key):
  global cypherText
  score = 0

  rawText = decode(key)

  # compute the fraction of unique words in the decoded text which are english
  words = set(rawText.split())
  engWords = words & wordlist
  fracEngWords = len(engWords)/len(words)
  # this fraction accounts for  50% of the fitness score
  score += fracEngWords*4

  freqs = Counter(rawText.replace(' ', ''))
  totLen = len(rawText)
  dist = mean([abs(freq/totLen - pdf[c]) for c, freq in freqs.items()])
  score -= dist*16

  return score

def scramble(key):
  letterSeq = random.sample(a_l, 10)
  temp = key[letterSeq[0]]
  for letter in letterSeq[1:]:
    key[letter], temp = (temp, key[letter])
  key[letterSeq[0]] = temp

def mixKeys(key1, key2):
  attemptCount = 0
  newKey = {}
  newKey = {letter:random.choice((key1[letter], key2[letter])) for letter in a_l}
  # for letter in a_l:
  #   newKey[letter] = random.choice((key1[letter], key2[letter]))
  scramble(newKey)

  return newKey

def intHandler(sig, frame):
  global keys
  print(f"""best solution: {keys[0]}
best decode:\n{decode(keys[0])}""")
  sys.exit(0)

def isBijection(key):
  return len(set(key.values())) == len(key.values())

cypherText = ''
def main():
  global cypherText

  genSize = 500
  samplePopSize = 25 # must be less than genSize
  # cypherText = input()
  if cypherText == '':
      cypherText = 'jiovqr dgvohfzr siulrgo if ogshfhfz gjyhur vr pgnn vr riag uiaaif rqrjgar is gjyhur hf pyvj hr gjyhur jyg vljyidr ogshfg gjyhur vr kghfz v rgj is hogvr jyvj ohujvjg pyvj bgibng ryilno vfo ryilno fij oi jygdg vdg ikxhilrnq avfq ohssgdgfj ruyiinr is jyilzyj vkilj yip ji vbbdivuy gjyhur pyhuy vdg ohrulrrgo hf pyvj pilno vf vxgfzgd oi avdw o pyhjg hf jyg dgvohfz yg ogshfgr ljhnhjvdhvfrha ogifjinizq vfo xhdjlg gjyhur vr jydgg ohssgdgfj klj dgnvjgo ruyiinr is jyilzyj yipgxgd hxg fgxgd sgnj jyvj jyhr rgbvdvjhif avwgr vfq rgfrg'

  keys = [dict(zip(a_l, random.sample(a_l, 26))) for i in range(genSize)]

  bestFitness = 0
  generation = 0

  while True:
    keys.sort(key=fitness, reverse=True)
    newBestFitness = fitness(keys[0])
    if newBestFitness > bestFitness:
      bestFitness = newBestFitness
      print(f"""Generation {generation}:
      Best fitness: {fitness(keys[0])}
      Best key: {keys[0]}
      Result Sample: {decode(keys[0])}""")
      
    generation += 1
    signal.signal(signal.SIGINT, intHandler)
    sampleKeys = keys[:samplePopSize]

    # for key in keys:
    #   if (isBijection(key)):
    #     sampleKeys.append(key)
    #   if (len(sampleKeys) == samplePopSize):
    #     break
    # else:
    #   raise Exception('Error: No bijections could be found')

    keys = sampleKeys + [mixKeys(*random.sample(sampleKeys, 2)) for i in range(genSize-samplePopSize)]

if __name__=='__main__':
  main()
