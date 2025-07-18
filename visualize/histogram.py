import sys
import pandas as pd
import os
import matplotlib.pyplot as plt 
import seaborn as sn 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from describe import *


students = importData("../datasets/dataset_train.csv")

random_students = next(iter(students.values()))

subjects = [x for x in random_students.keys() if x != "House"]

houses = set(student["House"] for student in students.values())

result = []

for house in houses:
    filtered = [s for s in students.values() if s["House"] == house]
    for subject in subjects:
        std = stdData(filtered, subject)
        print(f"l'ecart pour la matiere {subject} de la maison {house} est de {std}")
        result.append({
            "House" : house,
            "Subject" : subject,
            "Std" : std
        })

df = pd.DataFrame(result)

plt.figure(figsize=(100, 100))
sn.barplot(data=df, x="Subject", y="Std", hue="House", palette="Set2")
plt.title("Deviation in homogeneity of the different materials for the different houses")
plt.ylabel("gap")
plt.grid(True)
plt.show()

