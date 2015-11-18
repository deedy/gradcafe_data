import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from IPython.core.debugger import Tracer
import csv

csv_name = 'all.csv'
dedup_file = '../college_dedup.csv'

f = open('../college_dedup.csv', 'r')
cont = csv.reader(f, dialect=csv.Dialect.lineterminator)
trans = {c[0].lower():c[1] for c in cont}
valids = set(trans.values())
valids = sorted(list(valids), key=lambda x:-len(x))

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
      extra_dat.append(dat)
      # print(dat)
  else:
    dl[i][0] = trans[dat.lower()]
  count += 1
Tracer()()
df = pd.DataFrame(dl)
df.to_csv('all_clean.csv')

