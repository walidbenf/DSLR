from describe import *
import sys
import csv
import math
import json

def train_house(students, house_name, initial_weights, l_rate=0.000001, iterations=10000): # j'ai fait une fonction pour toutes les maisons pour éviter la redondance
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
                    produit_ponderes += weight * valeur   #calcule de tous les poids(impact de la note sur la somme) * la note de letudiant = poids_pondere

            if produit_ponderes >= 0:
                # sigmoide prmet de donner un chiffre entre 0 et 1 = 1 / (1 + (1 / e puissance -produit_ponderes))
                #et la puissance d'n negatif reviens a diviser 1 par e puissance le positif du nombre donner
                #en gros math.exp() calcule la puissance de eulere pour le nombre donner
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


def get_all_subjects(): # j'ai mis toutes les matieres dans une liste pour éviter la redondance
    """Retourne toutes les matières disponibles."""
    return [
        "Arithmancy",
        "Astronomy",
        "Herbology",
        "Defense Against the Dark Arts",
        "Divination",
        "Muggle Studies",
        "Ancient Runes",
        "History of Magic",
        "Transfiguration",
        "Potions",
        "Care of Magical Creatures",
        "Charms",
        "Flying"
    ]


def train_gryffindor(students):
    """Entraîne le modèle pour Gryffindor."""
    weights = {subject: 0.0 for subject in get_all_subjects()}
    weights["biais"] = 0.0
    return train_house(students, "Gryffindor", weights, l_rate=0.000001)


def train_ravenclaw(students):
    """Entraîne le modèle pour Ravenclaw."""
    weights = {subject: 0.0 for subject in get_all_subjects()}
    weights["biais"] = 0.0
    return train_house(students, "Ravenclaw", weights, l_rate=0.000001)


def train_slytherin(students):
    """Entraîne le modèle pour Slytherin."""
    weights = {subject: 0.0 for subject in get_all_subjects()}
    weights["biais"] = 0.0
    return train_house(students, "Slytherin", weights, l_rate=0.000001)


def train_hufflepuff(students):
    """Entraîne le modèle pour Hufflepuff."""
    weights = {subject: 0.0 for subject in get_all_subjects()}
    weights["biais"] = 0.0
    return train_house(students, "Hufflepuff", weights, l_rate=0.000001)

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
