from describe import *
import sys
import csv
import math

def train_gryffindor(students):
    weights = {
        "Charms" : 0.01,
        "Magic" : -0.02,
        "Flying" : 0.03,
        "Ancient Runes" : -0.04,
        "biais" : 0.05,
    }
    proba = 0
    eulere = math.e
    l_rate = 0.015
    for i in range(100000):

        for student in students.values():
            produit_ponderes = 0
            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                produit_ponderes += weight * valeur  #calcule de tous les poids * la note de letudiant

            proba = 1 / (1 + math.exp(-produit_ponderes)) # calcule de lexponentielle de eulere pour -prodits, permet d'avoir un chiffre positif egale a la probabilite que x eleve soit dans x maisn
            y = 1 if student["Hogwarts House"] == "Gryffindor" else 0  # verifie si leleve est dans la maison voulue
            erreur = -(y * math.log(proba) + (1 - y) * math.log(1 - proba))
            total += erreur
            if i % 1000 == 0:
                print(f"iteraion {i} : erreur moyenne = {total / len(students)}")

            for key, weight in weights.items():
                valeur = student.get(key, 1 if key == "biais" else 0)
                weights[key] = weight - l_rate * (proba - y) * valeur
    
    return weights
        


def  train_huflepuffle(students):

def train_slytherin(students):

def train_ravenclaw(students):

def main():
    students = importData('datasets/dataset_test.csv')

if __name__ == "__main__":
    main()