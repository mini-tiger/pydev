import warnings
warnings.simplefilter(action='ignore')

import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
ts = pd.Series(np.random.randn(20),
               index=pd.date_range('1/1/2000', periods=20)
              )

ts.plot()
plt.show()
