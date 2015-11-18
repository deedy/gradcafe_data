from bs4 import BeautifulSoup
import datetime, time
from IPython.core.debugger import Tracer
import sys, re
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
PROGS = [
    ('Computer Engineering', 'ECE'),
    ('Computer Enginnerin', 'ECE'),
    ('Electrical', 'ECE'),
    ('ECE', 'ECE'),
    ('Computer Sc', 'CS'),
    ('Computer  Sc', 'CS'),
    ('Computer Sicen', 'CS'),
    ('Computer Sien', 'CS'),
    ('Computer S Cience', 'CS'),
    ('Computer,', 'CS'),
    ('Computers,', 'CS'),
    ('ComputerScience', 'CS'),
    ('Human Computer Interaction', 'HCI'),
    ('Human-Computer Interaction', 'HCI'),
    ('Human-computer Interaction', 'HCI'),
    ('software engineering', 'CS'),
    ('Embedded', 'ECE'),
    ('Computer Eng', 'ECE'),
    ('Computer Vision', 'CS'),
    ('Information', 'IS'),
    ('Infomation', 'IS'),]

    # ('computer graphics', 'Game Development'),
    # ('computer gam', 'Game Development'),
    # ('Computer Systems', 'Computer Systems Engineering'),
    # ('Computer And Systems', 'Computer Systems Engineering'),
    # ('Computer & Systems', 'Computer Systems Engineering'),
    # ('Information Technology', 'IT'),
    # ('Communication', 'Computers and Communication'),
    # ('Computer Network', 'Computer Networking'),
    # ('Computer And Computational Sciences', 'Computer And Computational Sciences'),
    # ('Computer Music', 'Computer Music'),
    # ('Computer Control And Automation', 'Computer Control And Automation'),
    # ('Computer Aided Mechanical Engineering', 'CAME'),
    # ('Computer Art', 'Computer Art'),
    # ('Computer Animation', 'Computer Art'),
    # ('composition and computer technologies', 'Computer Art'),
    # ('computer forensics', 'Computer Art')]

DEGREE = [
  (' MFA', 'MFA'),
  (' M Eng', 'MEng'),
  (' MEng', 'MEng'),
  (' M.Eng', 'MEng'),
  (' MS', 'MS'),
  (' MA', 'MA'),
  (' Masters', 'MS'),
  (' PhD', 'PhD'),
  (' MBA', 'MBA'),
  (' Other', 'Other'),
  (' EdD', 'Other'),
]

STATUS = {
  'A': 'American',
  'U': 'International with US Degree',
  'I': 'International',
  'O': 'Other',
}

# 28722 records,
# major - 17 parse errors
# general - 87 parse errors
# subject - 31 parse errors
errlog = {'major': [], 'gpa': [], 'general': [], 'subject': []}
def process(index, col):
  global err
  inst, major, degree, season, decision, status, date_add, date_add_ts, comment = None, None, None, None, None, None, None, None, None

  if len(col) != 6:
    Tracer()()
  try:
    inst = col[0].text.strip().encode('ascii', 'ignore')
  except:
    Tracer()()
  try:
    major = None
    progtext = col[1].text.strip().encode('ascii', 'ignore')
    if not ',' in progtext:
      print 'no caomma'
      Tracer()()
      errlog['major'].append((index, col))
    else:
      parts = progtext.split(',')
      major = parts[0].strip()
      progtext = ' '.join(parts[1:])


    degree = None
    for (d, deg) in DEGREE:
      if d in progtext:
        degree = deg
        break
    if not degree:
      degree = 'Other'

    season = None
    mat = re.search('\([SF][01][0-9]\)', progtext)
    if mat:
      season = mat.group()[1:-1]
    else:
      mat = re.search('\(\?\)', progtext)
      if mat:
        season = None
  except NameError  as e:
    print e
    Tracer()()
  except:
    print "Unexpected error:", sys.exc_info()[0]
    Tracer()()
  try:
    extra = col[2].find(class_='extinfo')
    gpafin, grev, grem, grew, new_gre, sub = None, None, None, None, None, None
    if extra:
      gre_text = extra.text.strip().encode('ascii', 'ignore')
      gpa = re.search('Undergrad GPA: ((?:[0-9]\.[0-9]{1,2})|(?:n/a))', gre_text)
      general = re.search('GRE General \(V/Q/W\): ((?:1[0-9]{2}/1[0-9]{2}/(?:(?:[0-6]\.[0-9]{2})|(?:99\.99)|(?:56\.00)))|(?:n/a))', gre_text)
      new_gref = True
      subject = re.search('GRE Subject: ((?:[2-9][0-9]0)|(?:n/a))', gre_text)

      if gpa:
        gpa = gpa.groups(1)[0]
        if not gpa == 'n/a':
          try:
            gpafin = float(gpa)
          except:
            Tracer()()
      else:
        errlog['gpa'].append((index, gre_text))
      if not general:
        general = re.search('GRE General \(V/Q/W\): ((?:[2-8][0-9]0/[2-8][0-9]0/(?:(?:[0-6]\.[0-9]{2})|(?:99\.99)|(?:56\.00)))|(?:n/a))', gre_text)
        new_gref = False

      if general:
        general = general.groups(1)[0]
        if not general == 'n/a':
          try:
            greparts = general.split('/')
            if greparts[2] == '99.99' or greparts[2] == '0.00' or greparts[2] == '56.00':
              grew = None
            else:
              grew = float(greparts[2])
            grev = int(greparts[0])
            grem = int(greparts[1])
            new_gre = new_gref
            if new_gref and (grev > 170 or grev < 130 or grem > 170 or grem < 130 or (grew and (grew < 0 or grew > 6))):
              errlog['general'].append((index, gre_text))
              grew, grem, grev, new_gre = None, None, None, None
            elif not new_gref and (grev > 800 or grev < 200 or grem > 800 or grem < 200 or (grew and (grew < 0 or grew > 6))):
              errlog['general'].append((index, gre_text))
              grew, grem, grev, new_gre = None, None, None, None
          except Exception as e:
            Tracer()()
      else:
        errlog['general'].append((index, gre_text))


      if subject:
        subject = subject.groups(1)[0]
        if not subject == 'n/a':
          sub = int(subject)
      else:
        errlog['subject'].append((index, gre_text))

      extra.extract()
    decision = col[2].text.strip().encode('ascii', 'ignore')
    try:
      decisionfin, method, decdate, decdate_ts = None, None, None, None
      (decisionfin, method, decdate)  = re.search('((?:Accepted)|(?:Rejected)|(?:Wait listed)|(?:Other)|(?:Interview))? ?via ?((?:E-[mM]ail)|(?:Website)|(?:Phone)|(?:Other)|(?:Postal Service)|(?:Unknown))? ?on ?([0-9]{1,2} [A-Z][a-z]{2} [0-9]{4})?' , decision).groups()
      if method and method == 'E-Mail':
        method = 'E-mail'
      if method and method=='Unknown':
        method = 'Other'
      if decdate:
        try:
          decdate_date = datetime.datetime.strptime(decdate, '%d %b %Y')
          decdate_ts = decdate_date.strftime('%s')
          decdate = (decdate_date.day, decdate_date.month, decdate_date.year)
        except Exception as e:
          decdate_date, decdate_ts, decdate = None, None, None
    except Exception as e:
      Tracer()()
  except Exception as e:
    Tracer()()
  try:
    statustxt = col[3].text.strip().encode('ascii', 'ignore')
    if statustxt in STATUS:
      status = STATUS[statustxt]
    else:
      status = None
  except:
    Tracer()()
  try:
    date_addtxt = col[4].text.strip().encode('ascii', 'ignore')
    date_add_date = datetime.datetime.strptime(date_addtxt, '%d %b %Y')
    date_add_ts = date_add_date.strftime('%s')
    date_add = (date_add_date.day, date_add_date.month, date_add_date.year)
  except:
    # print(col[4].text.strip().encode('ascii', 'ignore'))
    Tracer()()
  try:
    comment = col[5].text.strip().encode('ascii', 'ignore')
  except:
    Tracer()()
  res = [inst, major, degree, season, decisionfin, method, decdate, decdate_ts, gpafin, grev, grem, grew, new_gre, sub, status, date_add, date_add_ts,  comment]
  print res
  return res

data = []
for year in range(1, 1093):
  with open('data/{0}.html'.format(year), 'r') as f:
    soup = BeautifulSoup(f.read())
    tables = soup.findAll('table', class_='results')
    for tab in tables:
      rows = tab.findAll('tr')
      for row in rows[1:]:
        cols = row.findAll('td')
        pro = process(year, cols)
        if len(pro) > 0:
          data.append(pro)
    print(year)
Tracer()()
for d in data:
  d[1] = d[1].encode('ascii', 'ignore')
Tracer()()
