from mtnetbri import *

from elefanpy import horology

def connect(host = '0.0.0.0', port = 18512, *args, **kwargs):
  result = None
  if (result == None):
    result = MetaTrader(host, port, *args, **kwargs)
  return result

def disconnect(instance, session = 'DEFAULT', *args, **kwargs):
  result = None
  if (result == None):
    result = (instance.deinitialize(session, *args, **kwargs) or instance)
  return result

class MetaTraderExtension(MetaTrader):

  def fetch(self, symbol, period, begin, end):
    result = None
    if (isinstance(period, str) == True):
      period = eval('self' + '.' + 'TIMEFRAME' + '_' + period)
    if (isinstance(begin, str) == True):
      begin = horology.parse(begin)
    if (isinstance(end, str) == True):
      end = horology.parse(end)
    result = self.copy_rates_range(symbol, period, begin, end)
    return result

MetaTrader = MetaTraderExtension
