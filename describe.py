import sys
import csv
import math

def parse_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def importData(path:str):
    students = {}
    with open(path, "r", encoding="utf-8") as csvfile:
        read = csv.DictReader(csvfile, delimiter=",")
        print(read.fieldnames)
        for line in read:
            name = line["First Name"]
            students[name] = {
                "House" : line["Hogwarts House"],
                "Arithmancy" : parse_float(line["Arithmancy"]),
                "Astronomy" : parse_float(line["Astronomy"]),
                "Herbology" : parse_float(line["Herbology"]),
                "Defense" : parse_float(line["Defense Against the Dark Arts"]),
                "Divination" : parse_float(line["Divination"]),
                "Muggle" : parse_float(line["Muggle Studies"]),
                "Ancient Runes" : parse_float(line["Ancient Runes"]),
                "History of Magic" : parse_float(line["History of Magic"]),
                "Transfiguration" : parse_float(line["Transfiguration"]),
                "Potions" : parse_float(line["Potions"]),
                "Magical Creatures" : parse_float(line["Care of Magical Creatures"]),
                "Charms" : parse_float(line["Charms"]),
                "Flying" : parse_float(line["Flying"]),
            }
    return students

def meanData(students, subject:str):
    if isinstance(students, dict):
        iterable = students.values()
    else:
        iterable = students
    mean = [x[subject] for x in iterable if x[subject] is not None]
    return sum(mean) / len(mean)


def stdData(students, subject:str):
    if isinstance(students, dict):
        iterable = students.values()
    else:
        iterable = students
    mean = meanData(students, subject)
    ecarts = [(x[subject] - mean)**2 for x in iterable if x[subject] is not None] #on mets la racine carrer pour eviter les annulations ex:(1, 0, -1)
    variance = sum(ecarts) / len(ecarts)
    std = math.sqrt(variance)
    return std

def firstQuartile(students, subject:str):
    sortData = [x[subject] for x in students.values() if x[subject] is not None]
    sortData.sort()
    pos = (len(sortData) + 1) / 4
    if pos.is_integer():
        return sortData[int(pos) - 1]
    else:
        lower_index = int(pos) -1
        upper_index = lower_index + 1
        fraction = pos - int(pos)

        lower_value = sortData[lower_index]
        upper_value = sortData[upper_index] if upper_index < len(sortData) else lower_value

        return lower_value + fraction * (upper_value - lower_value)

def secondQuartile(students, subject:str):
    sortData = [x[subject] for x in students.values() if x[subject] is not None]
    sortData.sort()
    pos = (len(sortData) + 1) / 2
    if pos.is_integer():
        return sortData[int(pos) - 1]
    else:
        lower_index = int(pos) - 1
        upper_index = int(pos)
        fraction = pos - int(pos)

        lower_value = sortData[lower_index]
        upper_value = sortData[upper_index] if upper_index < len(sortData) else lower_value
        
        return lower_value + fraction * (upper_value - lower_value)

def thirdQuartile(students, subject:str):
    sortData = [x[subject] for x in students.values() if x[subject] is not None]
    sortData.sort()
    pos = (len(sortData) + 1) / 4 * 3

    if pos.is_integer():
        return sortData[int(pos) - 1]
    else:
        lower_index = int(pos) - 1
        upper_index = int(pos)
        fraction = pos - int(pos)

        lower_value = sortData[lower_index]
        upper_value = sortData[upper_index] if upper_index < len(sortData) else lower_value

        return lower_value + fraction * (upper_value - lower_value)

def maxValue(students, subject:str):
    sortData = [x[subject] for x in students.values() if x[subject] is not None]
    sortData.sort()
    return sortData[-1]

def minValue(students, subject:str):
    sortData = [x[subject] for x in students.values() if x[subject] is not None]
    sortData.sort()
    return sortData[0]


def describe(students):
    # Garder seulement les colonnes avec des valeurs float ou None (les matières)
    first_student = next(iter(students.values()))
    subjects = [k for k, v in first_student.items() if isinstance(v, float) or v is None]

    header = [""] + subjects

    rows = [
        ["Count"] + [sum(1 for x in students.values() if x[s] is not None) for s in subjects],
        ["Mean"] + [round(meanData(students, s), 6) if meanData(students, s) is not None else None for s in subjects],
        ["Std"] + [round(stdData(students, s), 6) if stdData(students, s) is not None else None for s in subjects],
        ["Min"] + [minValue(students, s) for s in subjects],
        ["25%"] + [firstQuartile(students, s) for s in subjects],
        ["50%"] + [secondQuartile(students, s) for s in subjects],
        ["75%"] + [thirdQuartile(students, s) for s in subjects],
        ["Max"] + [maxValue(students, s) for s in subjects],
    ]

    col_width = 15
    print("".join(str(h).ljust(col_width) for h in header))
    for row in rows:
        print("".join(str(round(x, 6) if isinstance(x, float) else x).ljust(col_width) for x in row))


def main():
    students = importData("datasets/dataset_train.csv")
    describe(students)
    # print(f"{firstQuartile(students, 'Charms')}")


if __name__ == "__main__":
    main()