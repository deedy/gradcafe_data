import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from IPython.core.debugger import Tracer
import csv
from difflib import SequenceMatcher

csv_name = 'all.csv'
dedup_file = '../college_dedup.csv'

f = open('../college_dedup.csv', 'r')
cont = csv.reader(f, dialect=csv.Dialect.lineterminator)
trans = {c[0].lower():c[1] for c in cont}
cont = csv.reader(open('../college_dedup.csv', 'r'), dialect=csv.Dialect.lineterminator)
trans2 = {c[0]:c[1] for c in cont}
alls = set(trans2.values() + trans2.keys())
validset = set(trans.values())
valids = sorted(list(validset), key=lambda x:-len(x))

def get_best_match(word):
  bests = sorted([(v if not v in trans2 else trans2[v] , SequenceMatcher(None, word, v).ratio()) for v in alls], key=lambda x: -x[1])
  top = bests[0][0]
  next = None
  for i, b in enumerate(bests):
    if not b[0] == top:
      next = b
      break
  print(bests[0], i, next)
  print('\n')
  return (bests[0], i, next)

data = pd.read_csv(csv_name, sep=',', header = None, names = ['rowid', 'uni_name', 'major', 'degree', 'season', 'decision', 'decision_method', 'decision_date', 'decision_timestamp', 'ugrad_gpa','gre_verbal','gre_quant','gre_writing', 'is_new_gre', 'gre_subject', 'status', 'post_date', 'post_timestamp', 'comments'])
dl = map(list, data.values)

extra_dat = []
count = 0
for i, dat in enumerate(data['uni_name']):
  del dl[i][0]
  if not dat.lower() in trans:
    flag = False
    for v in valids:
      if not len(v) >= 3:
        continue
      if v in dat:
        flag = True
        dl[i][0] = v
        # print("{0}\t\t-->\t\t{1}".format(dat, v))
        break
    if not flag:
      best_match = get_best_match(dl[i][0])
      if best_match[0][1] >= 0.9 or (best_match[0][1] >= 0.8 and best_match[1] > 5) or (best_match[0][1] >= 0.85 and (best_match[0][1] - best_match[2][1]) > 0.1):
        print("{0}\t\t-->\t\t{1}".format(dat, best_match[0][0]))
        dl[i][0] = best_match[0][0]
      else:
        extra_dat.append(dat)
      # print(dat)
  else:
    dl[i][0] = trans[dat.lower()]
  count += 1
Tracer()()
df = pd.DataFrame(dl)
df.to_csv('all_clean.csv', header = None)

