import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from IPython.core.debugger import Tracer
import csv
from collections import Counter

csv_name = 'cs.csv'
dedup_file = '../college_dedup.csv'

f = open('../college_dedup.csv', 'r')
cont = csv.reader(f, dialect=csv.Dialect.lineterminator)
trans = {c[0]:c[1] for c in cont}

data = pd.read_csv(csv_name, sep=',', header = None, names = ['rowid', 'uni_name', 'major', 'degree', 'season', 'decision', 'decision_method', 'decision_date', 'decision_timestamp', 'ugrad_gpa','gre_verbal','gre_quant','gre_writing', 'is_new_gre', 'gre_subject', 'status', 'post_date', 'post_timestamp', 'comments'])
Tracer()()
