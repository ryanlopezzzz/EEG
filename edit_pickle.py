import pickle
import numpy as np
import collections
import matplotlib.pyplot as plt

filename = input('Please enter filename to read: ')

data_dict = collections.OrderedDict()

data_dict['10'] = 0.866
data_dict['20'] =0.599
data_dict['30'] = 0.292
data_dict['40'] = 0.109
data_dict['50'] =0.0157
data_dict['60'] =0.0029
data_dict['70'] =0.0405
data_dict['80'] =0.101
data_dict['90'] =0.172
data_dict['100'] =0.244
data_dict['110'] =0.3177
data_dict['120'] =0.376
data_dict['130'] =0.397
data_dict['140'] =0.447


file = open(filename, 'wb')
pickle.dump(data_dict, file)
file.close()
input('Press <Enter> to end')