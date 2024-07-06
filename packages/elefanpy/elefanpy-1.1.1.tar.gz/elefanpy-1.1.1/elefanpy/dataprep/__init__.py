from sklearn.preprocessing import *

from elefanpy import numpy

def build_transformer(name, *args, **kwargs):
  result = None
  if (name == 'none'):
    result = FunctionTransformer(*args, **kwargs)
  if (name == 'power'):
    result = PowerTransformer(*args, **kwargs)
  if (name == 'quantile'):
    result = QuantileTransformer(*args, **kwargs)
  if (name == 'spline'):
    result = SplineTransformer(*args, **kwargs)
  return result

def build_scaler(name, *args, **kwargs):
  result = None
  if (name == 'none'):
    result = FunctionTransformer(*args, **kwargs)
  if (name == 'standard'):
    result = StandardScaler(*args, **kwargs)
  if (name == 'robust'):
    result = RobustScaler(*args, **kwargs)
  if (name == 'maxabs'):
    result = MaxAbsScaler(*args, **kwargs)
  if (name == 'minmax'):
    result = MinMaxScaler(*args, **kwargs)
  return result

def split_portion(array, split, portion):
  result = None
  if (result == None):
    result = numpy.array_split(array, split)[portion]
  return result

def split_sequence(data, input, output):
  result = None
  ind, dep = list(), list()
  for index in range(len(data)):
    limit = index + input + output
    if (limit > len(data)):
      break
    if (input == 1):
      ind.append(data[index])
    elif (input > 1):
      ind.append(data[index:(index + input)])
    if (output == 1):
      dep.append(data[index + input])
    elif (output > 1):
      dep.append(data[(index + input):limit])
  result = numpy.array(ind), numpy.array(dep)
  return result
