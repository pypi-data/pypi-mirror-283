from os import *

def env(name, default = None, evaluate = None):
  result = None
  if ((name != None) and (isinstance(default, str) != True) and (evaluate == None)):
    evaluate = True
  else:
    evaluate = False
  if (evaluate == True):
    result = (eval(environ[name]) if (name in environ) else default)
  else:
    result = (environ[name] if (name in environ) else default)
  return result

def log(data, show = True):
  result = None
  if (result == None):
    print(data) if show else None
  return result
