from IPython.display import display
import matplotlib.pyplot as plt
#matplotlib inline
import numpy as np
import os
import shutil

import wfdb

import numpy as np
import urllib

targeturl = "http://physionet.org/physiobank/database/macecgdb/test01_00s.dat"
urllib.request.urlretrieve(targeturl, "test.dat")
data = np.fromfile("test.dat")