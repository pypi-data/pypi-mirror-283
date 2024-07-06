from matplotlib.pyplot import *

from elefanpy import matplotlib

def visualize(title, data, xlabel, ylabel, show = True, block = True):
  result = None
  figure(title, figsize = (20, 10))
  title(title)
  for item in data:
    plot(item[0], item[2], label = item[1])
  legend(fontsize = 10, ncols = 3, loc = 1, bbox_to_anchor = (1.0, 1.1))
  xlabel(xlabel)
  xticks(fontsize = 15)
  ylabel(ylabel)
  yticks(fontsize = 15)
  show(block = block) if show else None
  result = show
  return result
