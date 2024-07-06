from pandas import *

from elefanpy import regex

def create(data, standard):
  result = None
  if (standard == 'metatrader'):
    result = DataFrame(data)
    result.rename(columns = { 'tick_volume': 'volume' }, inplace = True)
    result.drop(columns = 'real_volume', inplace = True)
  return result

def summary(frame, limit = 5):
  result = None
  if (result == None):
    result = concat([frame.head(limit), frame.tail(limit)])
    result = regex.sub('^\s', '#', result.to_string())
  return result
