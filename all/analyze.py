import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from IPython.core.debugger import Tracer
import csv
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from scipy.stats import rv_discrete
from collections import Counter
import re

csv_name = '../all_uisc_clean.csv'
data = pd.read_csv(csv_name, sep=',', header = None, names = ['rowid', 'uni_name', 'major', 'degree', 'season', 'decision', 'decision_method', 'decision_date', 'decision_timestamp', 'ugrad_gpa','gre_verbal','gre_quant','gre_writing', 'is_new_gre', 'gre_subject', 'status', 'post_date', 'post_timestamp', 'comments'])



def plot_gre_verb_math():
  grev = data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True]
  grem = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True]
  (sns.jointplot(grev, grem, stat_func=None, kind='kde', size=9, xlim=(130,170), ylim=(130,170)).set_axis_labels('GRE Verbal','GRE Quantitative'))
  plt.show()

def plot_gre_verb_gpa():
  grev = data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True]
  gpa = data['ugrad_gpa'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True]
  (sns.jointplot(grev, gpa, stat_func=None, kind='kde', size=9, xlim=(130,170), ylim=(2,4.3)).set_axis_labels('GRE Verbal','Undergraduate GPA'))
  plt.show()

def plot_from_prob(vals, pdf, lab, col):
  dist = rv_discrete(values=(vals,np.array(map(float,pdf))/sum(pdf)))
  vals = [dist.rvs() for i in xrange(10000)]
  sns.distplot(np.array(vals), bins=41, label=lab, color=col)
  avg = np.array(vals).mean()
  plt.axvline(avg, color=col, linestyle='dashed', linewidth=2)
  plt.annotate('{0:.1f}'.format(avg), (avg, 0), fontsize = 12, va='bottom', ha='center')
  return vals


def gre_percentile_vs_actual():
  cc = Counter(data['gre_quant'][data['is_new_gre'] == True])
  cc1 = Counter(data['gre_verbal'][data['is_new_gre'] == True])
  cum_q = [i[1] for i in sorted([(j, cc[j]) for j in cc],key= lambda x:x[0])]
  cum_v = [i[1] for i in sorted([(j, cc1[j]) for j in cc1],key= lambda x:x[0])]
  perc_q = [100*float(sum(cum_q[:i]))/sum(cum_q) for i in xrange(len(cum_q))]
  perc_v = [100*float(sum(cum_v[:i]))/sum(cum_v) for i in xrange(len(cum_v))]
  quant_act = [98, 97, 95, 94, 93, 90, 88, 86, 83, 80, 78, 75, 71, 68, 64, 60, 56, 52, 48, 45, 40, 37, 32, 28, 25, 21, 18, 15, 12, 10, 8, 6, 4, 3, 2, 2, 1, 1, 0, 0, 0][::-1]
  verb_act = [99, 99, 98, 97, 96, 95, 94, 92, 90, 87, 85, 81, 79, 74, 71, 67, 63, 59, 54, 50, 45, 41, 37, 33, 29, 25, 22, 18, 16, 13, 10, 8, 7, 5, 3, 3, 2, 1, 1, 1, 0][::-1]
  act_q_dist = ([100 - quant_act[-1]] + [(quant_act[-i]-quant_act[-i-1]) for i in xrange(1,len(quant_act))])[::-1]
  act_q_dist = gaussian_filter1d(map(float,act_q_dist),1)
  gc_q_dist = ([100 - perc_q[-1]] + [(perc_q[-i]-perc_q[-i-1]) for i in xrange(1,len(perc_q))])[::-1]
  act_v_dist = ([100 - verb_act[-1]] + [(verb_act[-i]-verb_act[-i-1]) for i in xrange(1,len(verb_act))])[::-1]
  act_v_dist = gaussian_filter1d(map(float,act_v_dist),1)
  gc_v_dist = ([100 - perc_v[-1]] + [(perc_v[-i]-perc_v[-i-1]) for i in xrange(1,len(perc_v))])[::-1]
  current_palette = sns.color_palette()
  gc_v_vals = plot_from_prob(range(130,171), gc_v_dist, 'Grad School Applicants (Reported)', current_palette[0])
  act_v_vals = plot_from_prob(range(130,171), act_v_dist, 'All GRE Test Takers', current_palette[1])
  plt.xlim((130,170))
  plt.ylabel('Probability')
  plt.xlabel('GRE Verbal')
  plt.title('GRE Quantitative Difference amongst Grad School Applicants and All Test Takers')
  plt.legend()
  plt.show()
  gc_q_vals = plot_from_prob(range(130,171), gc_q_dist, 'Grad School Applicants (Reported)', current_palette[2])
  act_q_vals = plot_from_prob(range(130,171), act_q_dist, 'All GRE Test Takers', current_palette[3])
  plt.xlim((130,170))
  plt.ylabel('Probability')
  plt.xlabel('GRE Quantitative')
  plt.title('GRE Quantitative Difference amongst Grad School Applicants and All Test Takers')
  plt.legend()
  plt.show()

# degree = 'MS'/'PhD'
# gre_type = 'all'/'verbal'/'quant'/'gpa'
def plot_gpa_diffs_ar_for_college(num = 25, degree = 'PhD', x_type='all', y_type='gpa'):
  min_apps = 50
  cut_off = 100
  most_comm = Counter(data['uni_name'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]).most_common(cut_off)
  if x_type =='verbal':
    grev = data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  elif x_type =='quant':
    grev = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  elif x_type=='all':
    grev = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree] + data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  else:
    grev = data['ugrad_gpa'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]

  if y_type =='verbal':
    grem = data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  elif y_type =='quant':
    grem = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  elif y_type=='all':
    grem = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree] + data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  else:
    grem = data['ugrad_gpa'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]

  grem2 = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree][data['decision'] == 'Accepted'] + data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree][data['decision'] == 'Accepted']
  lgrev, lgrem = list(grev), list(grem)
  uni_phds = sorted([(most_comm[i][0], most_comm[i][1], grem2[data['uni_name'] == most_comm[i][0]].mean()) for i in xrange(len(most_comm)) if most_comm[i][1] >= min_apps], key=lambda x:-(x[-1]))[:num]
  content = []
  colors = sns.color_palette("Set2", num)
  colors_ar = sum([[c, c] for c in colors], [])
  colors_ar2 = sum([[sns.color_palette()[1], sns.color_palette()[2]] for c in colors], [])
  for name, size, gre_tot in uni_phds:
    grev_ca = grev[data['uni_name'] == name][data['decision'] == 'Accepted']
    grev_cr = grev[data['uni_name'] == name][data['decision'] == 'Rejected']
    grem_ca = grem[data['uni_name'] == name][data['decision'] == 'Accepted']
    grem_cr = grem[data['uni_name'] == name][data['decision'] == 'Rejected']
    abbr = re.search("\(([^\)]{1,})\)",name)
    if abbr:
      name = abbr.groups(1)[0]
    name = name.replace('University', '').strip()
    name = name.replace('Of', '').strip()
    name = name.replace('The', '').strip()
    name = name.replace(',', '').strip()
    content.append((grev_ca.mean(), grem_ca.mean(), len(grev_ca), name))
    content.append((grev_cr.mean(), grem_cr.mean(), len(grev_cr), name))


  fig = plt.figure(figsize=(9, 9))
  plt.scatter(x=[i[0] for i in content],y=[i[1] for i in content], s= [2.*i[2] for i in content], alpha=0.5, c=colors_ar2, edgecolor='none')
  if x_type =='verbal':
    plt.xlim((155, 170))
  elif x_type =='quant':
    plt.xlim((155, 170))
  elif x_type == 'all':
    plt.xlim((300, 340))
  elif x_type == 'gpa':
    plt.xlim((3.5, 4.0))
  if y_type =='verbal':
    plt.ylim((155, 170))
  elif y_type =='quant':
    plt.ylim((155, 170))
  elif y_type == 'all':
    plt.ylim((300, 340))
  elif y_type == 'gpa':
    plt.ylim((3.5, 4.0))
  if x_type =='verbal':
    plt.xlabel('GRE Verbal')
  elif x_type =='quant':
    plt.xlabel('GRE Quantitative')
  elif x_type == 'all':
    plt.xlabel('GRE Total')
  elif x_type == 'gpa':
    plt.xlabel('Undergrad GPA')
  if y_type =='verbal':
    plt.ylabel('GRE Verbal')
  elif y_type =='quant':
    plt.ylabel('GRE Quantitative')
  elif y_type == 'all':
    plt.ylabel('GRE Total')
  elif y_type == 'gpa':
    plt.ylabel('Undergrad GPA')
  plt.title('College by {0} Acceptances and Rejection GRE Verbal and Undergrad Score '.format(degree))
  anno =  [plt.annotate(i[3], (i[0], i[1]), fontsize = max(.3*math.sqrt(i[2]), 8) , va='center', ha='center') for i in content]
  plt.show()


def plot_gre_diffs_for_college(num = 20, degree = 'PhD', gre_type='all'):
  uni_phds = Counter(data['uni_name'][data['is_new_gre'] == True][data['degree']==degree]).most_common(num)
  if gre_type =='verbal':
    grev = data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  elif gre_type =='quant':
    grev = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  else:
    grev = data['gre_quant'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree] + data['gre_verbal'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  grem = data['ugrad_gpa'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  content = []
  colors = sns.color_palette("Set2", num)
  colors_ar = sum([[c, c] for c in colors], [])
  for name, size in uni_phds:
    grev_c = grev[data['uni_name'] == name].mean()
    grem_c = grem[data['uni_name'] == name].mean()
    abbr = re.search("\(([^\)]{1,})\)",name)
    if abbr:
      name = abbr.groups(1)[0]
    name = name.replace('University', '').strip()
    name = name.replace('Of', '').strip()
    name = name.replace('The', '').strip()
    name = name.replace(',', '').strip()
    content.append((grev_c, grem_c, size, name))


  fig = plt.figure(figsize=(9, 9))
  for i in content:
    anno = plt.annotate(i[3], (i[0], i[1]), fontsize = max(.3*math.sqrt(i[2]), 8) , va='center', ha='center')
  points  = plt.scatter(x=[i[0] for i in content],y=[i[1] for i in content], s= [i[2] for i in content], alpha=0.7, c=colors, edgecolor='none')
  if gre_type =='verbal':
    plt.xlim((156, 167))
  elif gre_type =='quant':
    plt.xlim((158, 170))
  else:
    plt.xlim((300, 340))
  plt.ylim((3.5, 4.0))
  if gre_type =='verbal':
    plt.xlabel('GRE Verbal')
  elif gre_type =='quant':
    plt.xlabel('GRE Quantitative')
  else:
    plt.xlabel('GRE Total')
  plt.ylabel('Undergrad GPA')
  plt.title('Colleges by {0} Applicant Scores'.format(degree))
  plt.show()

def aggregate_and_find_by_major(major = None):
  min_gre_gpa_data = 30
  if major:
    common_majors= set({f[0] for f in Counter(data['major']).most_common(50)})
    if not major in common_majors:
      print("Not enough data")
      return None
    tabu = [
      (i[0],
      i[1],
      len(data['uni_name'][data['degree']=='PhD'][data['major']==major][data['uni_name'] == i[0]][data['decision']=='Rejected']) + len(data['uni_name'][data['degree']=='PhD'][data['major']==major][data['uni_name'] == i[0]][data['decision']=='Accepted']),
      float(len(data['uni_name'][data['degree']=='PhD'][data['major']==major][data['uni_name'] == i[0]][data['decision']=='Accepted']))/(len(data['uni_name'][data['degree']=='PhD'][data['major']==major][data['uni_name'] == i[0]][data['decision']=='Rejected']) + len(data['uni_name'][data['degree']=='PhD'][data['major']==major][data['uni_name'] == i[0]][data['decision']=='Accepted'])),
      len(data['uni_name'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['major']==major]),
      data['ugrad_gpa'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['major']==major][data['decision']=='Accepted'].quantile([0.25, 0.5, 0.75]),
      data['gre_verbal'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['major']==major][data['decision']=='Accepted'].quantile([0.25, 0.5, 0.75]),
      data['gre_quant'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['major']==major][data['decision']=='Accepted'].quantile([0.25, 0.5, 0.75]))
      for i in Counter(data['uni_name'][data['degree']=='PhD'][data['major']==major]).most_common(250) if len(data['uni_name'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['major']==major]) >= min_gre_gpa_data]
  else:
    tabu = [
      (i[0],
      i[1],
      len(data['uni_name'][data['degree']=='PhD'][data['major']==major][data['uni_name'] == i[0]][data['decision']=='Rejected']) + len(data['uni_name'][data['degree']=='PhD'][data['uni_name'] == i[0]][data['decision']=='Accepted']),
      float(len(data['uni_name'][data['degree']=='PhD'][data['uni_name'] == i[0]][data['decision']=='Accepted']))/(len(data['uni_name'][data['degree']=='PhD'][data['uni_name'] == i[0]][data['decision']=='Rejected']) + len(data['uni_name'][data['degree']=='PhD'][data['uni_name'] == i[0]][data['decision']=='Accepted'])),
      len(data['uni_name'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD']),
      data['ugrad_gpa'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['decision']=='Accepted'].quantile([0.25, 0.5, 0.75]),
      data['gre_verbal'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['decision']=='Accepted'].quantile([0.25, 0.5, 0.75]),
      data['gre_quant'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD'][data['decision']=='Accepted'].quantile([0.25, 0.5, 0.75]))
      for i in Counter(data['uni_name'][data['degree']=='PhD']).most_common(250) if len(data['uni_name'][data['uni_name'] == i[0]][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']=='PhD']) >= min_gre_gpa_data]

  tabu2 = [sum([list(i[:5]), list(i[5]), list(i[6]), list(i[7])], []) for i in tabu]
  df = pd.DataFrame(tabu2)
  df.to_csv('../college_agg_phd_{0}.csv'.format(major.lower().replace(' ','_')), header =None)

def plot_by_major(num = 25, degree='PhD', x_type='all', y_type='gpa'):
  min_count = 30
  trans = {'Speech-Language Pathology': 'Speech Pathology', 'Commuicative Disorders/ Speech Pathology': 'Speech Pathology', 'Speech Pathology': 'Speech Pathology', 'Computer Scicence': 'Computer Science', 'Communcation Disorders Speech Language Pathology': 'Speech Pathology', 'Communcation Disorders/ Speech Language Pathology': 'Speech Pathology', 'Communication Disorders / Speech Language Pathology': 'Speech Pathology', 'Communication Science And Disorders / Speech Language Pathology': 'Speech Pathology', 'Communication Disorders /  Speech Language Pathology' : 'Speech Pathology', 'Speech Language Pathology': 'Speech Pathology', 'Communication Disorders / Speech Pathology': 'Speech Pathology', 'Communication Disorders / Speech-Language Pathology': 'Speech Pathology', 'Communicative Disorders / Speech Language Pathology': 'Speech Pathology', 'Architecture (3 Yr) M.Arch': 'Architecture', 'Architecture (M. Arch 1)': 'Architecture', 'Electrical And Computer Engineering': 'ECE', 'ECE (Electrical & Computer Engineering)': 'ECE', 'International Affairs': 'International Relations', 'City And Regional Planning': 'Urban Planning', 'Communication Sciences And Disorders / Speech Language Pathology': 'Speech Pathology', 'Communications Disorders/Speech Language Pathology': 'Speech Pathology', 'Civil Engineering (Structural)': 'Civil Engineering', 'ECE (Electrical And Computer Engineering)': 'ECE', 'Urban And Regional Planning': 'Urban Planning', '(ECE) Electrical And Computer Engineering': 'ECE','Master In Public Policy': 'Master In Public Policy (MPP)', 'Civil & Environmental Engineering': 'Civil Engineering', 'Library And Information Science': 'Information Science'}
  data['major'] = [d if not d in trans else trans[d] for d in data['major']]

  majors = Counter(data['major'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == False][data['degree']==degree][data['decision']=='Accepted']).most_common(num)
  res = data[['major','ugrad_gpa', 'gre_verbal', 'gre_quant']][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree][data['decision']=='Accepted']
  finres = [(major, count, res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['major']==major].mean()) for major, count in majors if count >= min_count]

  finres2 = []
  for i in finres:
    name = i[0]
    name = name.replace('Engineering', 'Engg').replace('Mathematics', 'Math').replace('Psychology', 'Psych').replace('Department Of', '').strip()
    abbr = re.search("\(([^\)]{1,})\)",name)
    if abbr:
      name = abbr.groups(1)[0]
    finres2.append((name, i[1], i[2]))
  finres = finres2

  xlims, x_data, xlabel, ylims, y_data, ylabel = [None] * 6
  if x_type == 'all':
    x_data = [i[2][1] + i[2][2] for i in finres]
    xlims = (300, 340)
    xlabel = 'GRE Total'
  elif x_type == 'verbal':
    x_data = [i[2][1] for i in finres]
    xlims = (150, 170)
    xlabel = 'GRE Verbal'
  elif x_type == 'quant':
    x_data = [i[2][2] for i in finres]
    xlims = (150, 170)
    xlabel = 'GRE Quantitative'
  elif x_type == 'gpa':
    x_data = [i[2][0] for i in finres]
    xlims = (3.2, 4.0)
    xlabel = 'Undergrad GPA'
  if y_type == 'all':
    y_data = [i[2][1] + i[2][2] for i in finres]
    ylims = (300, 340)
    ylabel = 'GRE Total'
  elif y_type == 'verbal':
    y_data = [i[2][1] for i in finres]
    ylims = (150, 170)
    ylabel = 'GRE Verbal'
  elif y_type == 'quant':
    y_data = [i[2][2] for i in finres]
    ylims = (150, 170)
    ylabel = 'GRE Quantitative'
  elif y_type == 'gpa':
    y_data = [i[2][0] for i in finres]
    ylims = (3.2, 4.0)
    ylabel = 'Undergrad GPA'
  fig = plt.figure(figsize=(9, 9))
  colors = sns.color_palette("Set2", num)
  plt.scatter(x=x_data,y=y_data, s= [4.*i[1] for i in finres], alpha=0.5, c=colors, edgecolor='none')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.xlim(xlims)
  plt.ylim(ylims)
  plt.title('Majors of Study to {0} Programs '.format(degree))
  anno =  [plt.annotate(finres[i][0], (x_data[i], y_data[i]), fontsize = max(.5*math.sqrt(finres[i][1]), 8) , va='center', ha='center') for i in xrange(len(finres))]
  plt.show()


def plot_anim_applicants_ar(num=25, degree='PhD', x_type='all', y_type='gpa', frames = 60, file_suffix=''):
  min_count = 30
  unis = Counter(data['uni_name'][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == False][data['degree']==degree][data['decision']=='Accepted']).most_common(num)
  res = data[['uni_name','ugrad_gpa', 'gre_verbal', 'gre_quant']][data['ugrad_gpa'] <= 4.3][data['ugrad_gpa'] >= 2.0][data['is_new_gre'] == True][data['degree']==degree]
  def process_name(name):
    abbr = re.search("\(([^\)]{1,})\)",name)
    if abbr:
      name = abbr.groups(1)[0]
    name = name.replace('University', '').strip()
    name = name.replace('Of', '').strip()
    name = name.replace('The', '').strip()
    name = name.replace(',', '').strip()
    return name

  overall = {uni: (process_name(uni), len(res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['uni_name']==uni]), res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['uni_name']==uni].mean()) for uni, count in unis if count >= min_count}
  uniar = {uni: (process_name(uni), len(res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['uni_name']==uni][data['decision']=='Accepted']), len(res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['uni_name']==uni][data['decision']=='Rejected']), res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['uni_name']==uni][data['decision']=='Accepted'].mean(), res[['ugrad_gpa', 'gre_verbal', 'gre_quant']][data['uni_name']==uni][data['decision']=='Rejected'].mean()) for uni, count in unis if count >= min_count}
  uniorder = uniar.keys()

  if x_type =='verbal':
    minx = min([uniar[u][4][1] for u in uniorder])
    maxx = max([uniar[u][3][1] for u in uniorder])
  elif x_type =='quant':
    minx = min([uniar[u][4][2] for u in uniorder])
    maxx = max([uniar[u][3][2] for u in uniorder])
  elif x_type == 'all':
    minx = min([uniar[u][4][1] + uniar[u][4][2] for u in uniorder])
    maxx = max([uniar[u][3][1] + uniar[u][3][2] for u in uniorder])
  elif x_type == 'gpa':
    minx = min([uniar[u][4][0] for u in uniorder])
    maxx = max([uniar[u][3][0] for u in uniorder])
  minx = minx - (maxx - minx)*0.05
  maxx = maxx + (maxx - minx)*0.05
  xlims = (minx, maxx)
  if y_type =='verbal':
    miny = min([uniar[u][4][1] for u in uniorder])
    maxy = max([uniar[u][3][1] for u in uniorder])
  elif y_type =='quant':
    miny = min([uniar[u][4][2] for u in uniorder])
    maxy = max([uniar[u][3][2] for u in uniorder])
  elif y_type == 'all':
    miny = min([uniar[u][4][1] + uniar[u][4][2] for u in uniorder])
    maxy = max([uniar[u][3][1] + uniar[u][3][2] for u in uniorder])
  elif y_type == 'gpa':
    miny = min([uniar[u][4][0] for u in uniorder])
    maxy = max([uniar[u][3][0] for u in uniorder])
  miny = miny - (maxy - miny)*0.05
  maxy = maxy + (maxy - miny)*0.05
  ylims = (miny, maxy)


  for fr in xrange(frames+1):
    prop = float(fr)/frames
    x_data, xlabel, y_data, ylabel, size = [None] * 5
    sizes = sum([[4.*(uniar[uni][1]*prop + overall[uni][1]*(1-prop)), 4.*(uniar[uni][2]*prop + overall[uni][1]*(1-prop))]  for uni in uniorder], [])
    if x_type == 'all':
      x_data = sum([[(uniar[uni][3][1] + uniar[uni][3][2])*prop + (overall[uni][2][1] + overall[uni][2][2])*(1-prop), (uniar[uni][4][1] + uniar[uni][4][2])*prop + (overall[uni][2][1] + overall[uni][2][2])*(1-prop)]  for uni in uniorder], [])
      xlabel = 'GRE Total'
    elif x_type == 'verbal':
      x_data = sum([[(uniar[uni][3][1])*prop + (overall[uni][2][1])*(1-prop), (uniar[uni][4][1])*prop + (overall[uni][2][1])*(1-prop)]  for uni in uniorder], [])
      xlabel = 'GRE Verbal'
    elif x_type == 'quant':
      x_data = sum([[(uniar[uni][3][2])*prop + (overall[uni][2][2])*(1-prop), (uniar[uni][4][2])*prop + (overall[uni][2][2])*(1-prop)]  for uni in uniorder], [])
      xlabel = 'GRE Quantitative'
    elif x_type == 'gpa':
      x_data = sum([[(uniar[uni][3][0])*prop + (overall[uni][2][0])*(1-prop), (uniar[uni][4][0])*prop + (overall[uni][2][0])*(1-prop)]  for uni in uniorder], [])
      xlabel = 'Undergrad GPA'
    if y_type == 'all':
      y_data = sum([[(uniar[uni][3][1] + uniar[uni][3][2])*prop + (overall[uni][2][1] + overall[uni][2][2])*(1-prop), (uniar[uni][4][1] + uniar[uni][4][2])*prop + (overall[uni][2][1] + overall[uni][2][2])*(1-prop)]  for uni in uniorder], [])
      ylabel = 'GRE Total'
    elif y_type == 'verbal':
      y_data = sum([[(uniar[uni][3][1])*prop + (overall[uni][2][1])*(1-prop), (uniar[uni][4][1])*prop + (overall[uni][2][1])*(1-prop)]  for uni in uniorder], [])
      ylabel = 'GRE Verbal'
    elif y_type == 'quant':
      y_data = sum([[(uniar[uni][3][2])*prop + (overall[uni][2][2])*(1-prop), (uniar[uni][4][2])*prop + (overall[uni][2][2])*(1-prop)]  for uni in uniorder], [])
      ylabel = 'GRE Quantitative'
    elif y_type == 'gpa':
      y_data = sum([[(uniar[uni][3][0])*prop + (overall[uni][2][0])*(1-prop), (uniar[uni][4][0])*prop + (overall[uni][2][0])*(1-prop)]  for uni in uniorder], [])
      ylabel = 'Undergrad GPA'
    fig = plt.figure(figsize=(9, 9))
    colors = sum([[sns.color_palette()[1], sns.color_palette()[2]] for c in uniorder], [])
    plt.scatter(x=x_data,y=y_data, s=sizes, alpha=0.5, c=colors, edgecolor='none')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(xlims)
    plt.ylim(ylims)
    plt.title('College by {0} Acceptances and Rejection GRE Verbal and Undergrad Score '.format(degree))
    anno =  [plt.annotate(uniar[uniorder[i/2]][0], (x_data[i], y_data[i]), fontsize = max(.2*math.sqrt(sizes[i]), 8) , va='center', ha='center') for i in xrange(len(y_data))]
    plt.savefig('{0}-{1}'.format(fr, file_suffix))



































Tracer()()
