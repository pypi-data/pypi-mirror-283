from matplotlib.pyplot import *

from elefanpy import matplotlib

def visualize(title, data, xlabel, ylabel, show = True, block = True):
  result = None
  if (matplotlib != None):
    result = vrender(title, data, xlabel, ylabel, show, block)
  return result

def vrender(vtitle, vdata, vxlabel, vylabel, vshow = True, vblock = True):
  result = None
  figure(vtitle, figsize = (20, 10))
  title(vtitle)
  for item in vdata:
    plot(item[0], item[2], label = item[1])
  legend(fontsize = 10, ncols = 3, loc = 1, bbox_to_anchor = (1.0, 1.1))
  xlabel(vxlabel)
  xticks(fontsize = 15)
  ylabel(vylabel)
  yticks(fontsize = 15)
  show(block = vblock) if vshow else None
  result = vshow
  return result
