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

result = {
    "subject": [],
    "grade" : [],
}

for subject in subjects:
    filtered = [s[subject] for s in students.values() if s[subject] is not None]
    result["subject"].append(subject)
    result["grade"].append(filtered)
    
plt.figure(figsize=(12, 6))
sns.swarmplot(x=data["Subject"], y=data["Grade"], palette="Set2")
plt.xticks(rotation=45)
plt.title("Distribution des notes par matière (Swarmplot)")
plt.ylabel("Note")
plt.xlabel("Matière")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()
