from describe import *
import sys
import csv
import math

def train_gryffindor(students):
    weights = {
        "Charms" : 0.01,
        "History of Magic" : 0.02,
        "Flying" : 0.03,
        "Transfiguration" : 0.04,
        "Defense" : 0.02,
        "Herbology" : 0.03,
        "Potions": -0.02,
        "biais" : 0.05,
    }
    proba = 0
    eulere = math.e
    l_rate = 0.0000015
    for i in range(5000):
        total=0
        # print("-------------------------------------------------------")
        for student in students.values():
            produit_ponderes = 0
            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                if valeur is not None:
                    produit_ponderes += weight * valeur   #calcule de tous les poids(impact de la note sur la somme) * la note de letudiant = poids_ponderes
                else:
                    continue
                
            if produit_ponderes >= 0:
                proba = 1 / (1 + math.exp(-produit_ponderes)) # sigmoide de nos produits ponderes qui revient a dire 1 / (1 + (1 / e puissance produit_ponderes))
            else:
                proba = math.exp(produit_ponderes) / (1 + math.exp(produit_ponderes))
            # if proba < 0.01:
            #     proba = 0.0
            proba = max(min(proba, 1 - 1e-15), 1e-15)
            if proba > 0.5 or student["House"] == "Gryffindor":
                print(f"proba = {proba} pour letudiant de la maison {student['House']}")
            y = 1 if student["House"] == "Gryffindor" else 0  # verifie si leleve est dans la maison voulue
            erreur = -(y * math.log(proba) + (1 - y) * math.log(1 - proba))
            total += erreur

            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                if valeur is not None:
                    weights[key] = weight - l_rate * (proba - y) * valeur 
        if i % 10 == 0:
            print(f"iteraion {i} : erreur moyenne = {total / len(students)}")
            # print(f"{weights}")
    
    
    return weights
        
# def predict_gryffindor(students):
#     with open("/json_file/gryffindor.json", "r") as f:
#         data = json.load(f)
    


# def  train_huflepuffle(students):
    

# def train_slytherin(students):

# def train_ravenclaw(students):

def main():
    students = importData('datasets/dataset_train.csv')
    train_gryffindor(students)

if __name__ == "__main__":
    main()