import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df

import scipy.stats as ss
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm


means = df.mean(axis=1)
std = df.std(axis=1)

n = df.shape[1]

yerr = std/np.sqrt(n) * ss.norm.ppf(1-0.05/2)
conf_ints = [ss.norm.interval(0.95, loc=mu, scale=se) for mu, se in zip(means, std/np.sqrt(n))]

def compute_probs(y, conf_int):
    if y < np.min(conf_int):
        result = 1.0
    elif y > np.max(conf_int):
        result = 0.0
    else:
        result = (np.max(conf_int) - y)/(np.max(conf_int) - np.min(conf_int))
    return result

y=43000


probs = [compute_probs(y, ci) for ci in conf_ints]

cmap = cm.get_cmap('coolwarm')
cpick = cm.ScalarMappable(cmap=cmap, norm=col.Normalize(vmin=0, vmax=1.0))
cpick.set_array([])


rects = plt.bar(range(len(df.T.columns)), means, yerr=yerr, color = cpick.to_rgba(probs))

plt.axhline(y=y, zorder=1, color='g')
yt = plt.gca().get_yticks()
yt = np.append(yt, y)
plt.gca().set_yticks(yt)


plt.xticks(range(len(df.T.columns)), df.T.columns)

cbar = plt.colorbar(cpick, orientation="horizontal")


[plt.gca().spines[loc].set_visible(False) for loc in ['top', 'right']]

plt.show()