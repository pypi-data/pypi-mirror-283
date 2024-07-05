from numpy import *

def calculate_change(data, filter, step = 1):
  result = None
  if (result == None):
    result = list()
    content = data[filter].values
    for index in range(len(content)):
      if (index < step):
        result.append(content[index] - content[index])
      else:
        result.append(content[index] - content[index - step])
  return result
