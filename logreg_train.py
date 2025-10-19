from describe import *
import sys
import csv
import math
import json

def train_house(students, house_name, initial_weights, l_rate=0.000001, iterations=10000):
    """
    Entraîne un modèle de régression logistique pour une maison spécifique.

    Args:
        students: Dictionnaire des étudiants
        house_name: Nom de la maison à entraîner
        initial_weights: Poids initiaux pour les features
        l_rate: Taux d'apprentissage
        iterations: Nombre d'itérations

    Returns:
        Les poids entraînés
    """
    weights = initial_weights.copy()
    proba = 0

    for i in range(iterations):
        total = 0
        for student in students.values():
            produit_ponderes = 0
            for key, weight in weights.items():
                valeur = student.get(key, 1 if key.lower() == "biais" else 0)
                if valeur is not None:
                    produit_ponderes += weight * valeur   # calcule de tous les poids * la note de l'étudiant

            if produit_ponderes >= 0:
                # sigmoide permet de donner un chiffre entre 0 et 1
                proba = 1 / (1 + math.exp(-produit_ponderes))
            else:
                # sert à gérer les négatifs trop petits pour éviter les overflow
                proba = math.exp(produit_ponderes) / (1 + math.exp(produit_ponderes))

            proba = max(min(proba, 1 - 1e-15), 1e-15)

            y = 1 if student["House"] == house_name else 0  # vérifie si l'élève est dans la maison voulue
            erreur = -(y * math.log(proba) + (1 - y) * math.log(1 - proba))
            total += erreur

            for key, weight in weights.items():
                valeur = student.get(key, 1 if key.lower() == "biais" else 0)
                if valeur is not None:
                    weights[key] = weight - l_rate * (proba - y) * valeur

        if i % 100 == 0:
            print(f"[{house_name}] itération {i} : erreur moyenne = {total / len(students)}")

    return weights


def train_gryffindor(students):
    """Entraîne le modèle pour Gryffindor."""
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
    return train_house(students, "Gryffindor", weights, l_rate=0.000001)


def train_ravenclaw(students):
    """Entraîne le modèle pour Ravenclaw."""
    weights = {
        "Charms" : 0.02,
        "Defense" : 0.05,
        "History og Magic" : -0.04,
        "Ancient Runes" : 0.02,
        "Magie" : -0.02,
        "Biais" : 0.4,
    }
    return train_house(students, "Ravenclaw", weights, l_rate=0.0000009)



def train_slytherin(students):
    """Entraîne le modèle pour Slytherin."""
    weights = {
        "Potions" : 0.03,
        "Herbology" : -0.02,
        "Defense" : 0.04,
        "Care of Magical Creatures" : 0.01,
        "Divination" : -0.03,
        "biais" : 0.06,
    }
    return train_house(students, "Slytherin", weights, l_rate=0.000001)


def train_hufflepuff(students):
    """Entraîne le modèle pour Hufflepuff."""
    weights = {
        "Herbology" : 0.02,
        "Defense" : 0.05,
        "History of Magic" : -0.04,
        "Ancient Runes" : 0.02,
        "Magie" : -0.02,
        "Biais" : 0.4,
    }
    return train_house(students, "Ravenclaw", weights, l_rate=0.0000009)

def save_weights(weights_dict, filename="weights.json"):
    """
    weights_dict = {
        "Gryffindor": {"Flying": 0.03, "Defense": 0.02, ...},
        "Ravenclaw": {"Charms": 0.02, "Defense": 0.05, ...},
        ...
    }
    """
    with open(filename, 'w') as f:
        json.dump(weights_dict, f, indent=4)

def main():
    if len(sys.argv) < 2:
        print("Usage: python logreg_train.py <dataset_path>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    students = importData(dataset_path)
    all_weights = {
    "Gryffindor": train_gryffindor(students),
    "Ravenclaw": train_ravenclaw(students),
    "Slytherin": train_slytherin(students),
    "Hufflepuff": train_hufflepuff(students)
}
    save_weights(all_weights)

if __name__ == "__main__":
    main()
