from datetime import *

def parse(data):
  result = None
  if (data != None):
    result = datetime.fromisoformat(data)
  else:
    result = datetime.now()
  return result
