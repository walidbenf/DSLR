from describe import *
import sys
import csv
import math

def train_gryffindor(students):
    weights = {
        # "Charms" : 0.01,
        # "History of Magic" : 0.02,
        "Flying" : 0.03,
        "Transfiguration" : 0.04,
        "Defense" : 0.02,
        # "Herbology" : 0.03,
        "Potions": -0.02,
        "biais" : 0.05,
    }
    proba = 0
    eulere = math.e
    l_rate = 0.000001
    for i in range(10000):
        total=0
        # print("-------------------------------------------------------")
        for student in students.values():
            produit_ponderes = 0
            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                if valeur is not None:
                    produit_ponderes += weight * valeur   #calcule de tous les poids(impact de la note sur la somme) * la note de letudiant = poids_pondere
                
            if produit_ponderes >= 0:
                # sigmoide prmet de donner un chiffre entre 0 et 1 = 1 / (1 + (1 / e puissance -produit_ponderes))
                #et la puissance d'n negatif reviens a diviser 1 par e puissance le positif du nombre donner
                #en gros math.exp() calcule la puissance de eulere pour le nombre donner
                proba = 1 / (1 + math.exp(-produit_ponderes)) # sigmoevient a dire 1 / (1 + (1 / e puissance -produit_ponderes))ide de nos produits ponderes qui r
            else:
                #sert a gerer les negatifs trop petit pour eviter les overflow fais exactement le meme calcul
                proba = math.exp(produit_ponderes) / (1 + math.exp(produit_ponderes)) 
            # if proba < 0.01:
            #     proba = 0.0
            proba = max(min(proba, 1 - 1e-15), 1e-15)
            # if proba > 0.5 or student["House"] == "Gryffindor":
            #     print(f"proba = {proba} pour letudiant de la maison {student['House']}")
            y = 1 if student["House"] == "Gryffindor" else 0  # verifie si leleve est dans la maison voulue
            erreur = -(y * math.log(proba) + (1 - y) * math.log(1 - proba))
            total += erreur

            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                if valeur is not None:
                    weights[key] = weight - l_rate * (proba - y) * valeur 
        if i % 100 == 0:
            print(f"iteraion {i} : erreur moyenne = {total / len(students)}")
            # print(f"{weights}")
    
    
    return weights
        

def  train_ravenclaw(students):
    weights = {
        "Charms" : 0.02,
        "Defense" : 0.01,
        "Defense" : 0.05,
        "History og Magic" : -0.04,
        "Ancient Runes" : 0.02,
        "Magie" : -0.02,
        "Biais" : 0.4,
    }

    proba = 0
    l_rate = 0.0000009
    for i in range(10000):
        total = 0
        # print("lol")
        for student in students.values():
            produits_ponderes = 0
            for key, weight in weights.items():
                valeur = student.get(key, 0 if key != "Biais" else 1)
                if valeur is not None:
                    produits_ponderes += weight * valeur
        
            if produits_ponderes >= 0:
                proba = 1 / (1 + math.exp(-produits_ponderes))
            else:
                proba = math.exp(produits_ponderes) / (1 + math.exp(produits_ponderes))

            proba = max(min(proba, 1 - 1e-15), 1e-15)
            # if (student["House"] == "Ravenclaw" or proba > 0.5):
            #     print(f"Proba = {proba} pour un eleve de {student['House']}")
            y = 1 if student["House"] == "Ravenclaw" else 0
            erreur = -(y * math.log(proba) + (1 - y) * math.log(1 - proba))
            total += erreur

            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                if valeur is not None:
                    weights[key] = weight - l_rate * (proba - y) * valeur
        if i % 100 == 0:
            print(f"iteraion {i} : erreur moyenne = {total / len(students)}")
        
    return weights

    

# def train_slytherin(students):


# def train_ravenclaw(students):

def main():
    students = importData('datasets/dataset_train.csv')
    train_gryffindor(students)

if __name__ == "__main__":
    main()