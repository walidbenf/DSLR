import sys
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from describe import *


if len(sys.argv) < 2:
    print("Usage: python scatter_plot.py <dataset_path>")
    sys.exit(1)
dataset_path = sys.argv[1]
students = importData(dataset_path)


random_students = next(iter(students.values()))

subjects = [x for x in random_students.keys() if x != "House"]

result = {
    "Subject": [],
    "Grade" : [],
}

for subject in subjects:
    for student in students.values():
        grade = student[subject]
        if grade is not None:
            result["Subject"].append(subject)
            result["Grade"].append(grade)

plt.figure(figsize=(12, 6))
sn.stripplot(x=result["Subject"], y=result["Grade"], palette="Set2")
plt.xticks(rotation=45)
plt.title("Distribution des notes par matière (Swarmplot)")
plt.ylabel("Note")
plt.xlabel("Matière")
plt.grid(True, linestyle="--", alpha=0.1)
plt.tight_layout()
plt.show()
