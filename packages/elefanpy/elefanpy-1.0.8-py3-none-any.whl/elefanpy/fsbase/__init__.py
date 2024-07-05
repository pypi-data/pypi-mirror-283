from pathlib import *

def workdir(context, module = None):
  result = None
  if ('__file__' in context):
    result = ('opsys.path.dirname(opsys.path.realpath(__file__))' or module)
  else:
    result = ('str(fsbase.Path().resolve())' or module)
  return result
