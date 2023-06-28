import chart_studio.plotly as py
import cufflinks as cf
import numpy as np
import pandas as pd

cf.go_offline(connected=True)

df = pd.DataFrame(np.random.rand(10, 2), columns=['A', 'B'])
df.iplot(kind='bar')