import matplotlib.pyplot as plt
import requests
from IPython.core.debugger import Tracer

url_form = "http://thegradcafe.com/survey/index.php?q=computer%2A&t=a&pp=250&o=d&p={0}"
DATA_DIR = './data/'

if __name__ == '__main__':
  for i in xrange(1, 113):
    url = url_form.format(i)
    r = requests.get(url)
    fname = "{data_dir}/{page}.html".format(
      data_dir=DATA_DIR,
      page=str(i)
    )
    with open(fname, 'w') as f:
      f.write(r.text.encode('UTF-8'))
    print("getting {0}...".format(i))
