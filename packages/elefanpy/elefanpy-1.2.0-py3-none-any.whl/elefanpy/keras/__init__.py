from keras import *

from elefanpy import onnxkit

def publish(model, folder, name, format):
  result = None
  if (format != None):
    result = []
  if ((format == 'entire') or (format == 'keras')):
    output = folder + '/' + name + '.' + 'keras'
    result.append(output)
    model.save(output)
  if ((format == 'entire') or (format == 'onnx')):
    output = folder + '/' + name + '.' + 'onnx'
    result.append(output)
    onnxkit.convert.from_keras(model, output_path = output)
  return result
