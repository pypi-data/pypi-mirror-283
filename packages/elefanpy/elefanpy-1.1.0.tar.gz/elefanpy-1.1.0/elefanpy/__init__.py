import os
import io

os.environ['AZ_BUFFER_SIZE'] = str(io.DEFAULT_BUFFER_SIZE)
os.environ['TF_BUFFER_SIZE'] = str(io.DEFAULT_BUFFER_SIZE)

os.environ['AZ_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if ((not ('KERAS_BACKEND' in os.environ)) or (os.environ['KERAS_BACKEND'] == '')):
  os.environ['KERAS_BACKEND'] = 'tensorflow'

if ((not ('KERAS_DOWNEND' in os.environ)) or (os.environ['KERAS_DOWNEND'] == '')):
  os.environ['KERAS_DOWNEND'] = 'tensorflow'

from .opsys import *
from .fsbase import *
from .rtenv import *
from .horology import *
from .calendar import *
from .regex import *
from .math import *
from .randna import *
from .gensysco import *
from .mtnetbri import *
from .tensorflow import *
from .keras import *
from .hptuner import *
from .sklearn import *
from .dataprep import *
from .pandas import *
from .numpy import *
from .matplotlib import *
from .pyplot import *
from .tawizard import *
from .onnxkit import *

os.environ['AZ_CPP_MIN_LOG_LEVEL'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
