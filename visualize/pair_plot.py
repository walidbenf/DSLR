import sys
import pandas as pd
import os
import matplotlib.pyplot as plt 
import seaborn as sn 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from describe import *

students = importData("../datasets/dataset_train.csv")

data_frame = pd.DataFrame.from_dict(students, orient='index')

data_frame = data_frame.dropna()

g = sn.pairplot(data_frame, hue="House", plot_kws={'alpha':0.5, 'edgecolor': 'k'})
g.fig.set_size_inches(18, 18)
g.fig.suptitle("Pair Plot des Matières", y=1.02)
g.savefig("pairplot_maison.png")  # 1-charms, 2 - magic, 3-flying, 4-ancient runes
