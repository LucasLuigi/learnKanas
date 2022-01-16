# -*-coding:Latin-1 -*

import sys
import random
from PIL import Image

ALPHABETS = ['Hiragana', 'Katakana', 'Kanji']

# The order must match with the input of selectKanasSubset
KANASSUBSETS = ["simple kanas", "Dakuon", "Handakuon", "combo kanas"]

SIMPLEKANAS = {
    "": ["a", "i", "u", "e", "o"],
    "K": ["ka", "ki", "ku", "ke", "ko"],
    "S": ["sa", "shi", "su", "se", "so"],
    "T": ["ta", "chi", "tsu", "te", "to"],
    "N": ["na", "ni", "nu", "ne", "no"],
    "H": ["ha", "hi", "fu", "he", "ho"],
    "M": ["ma", "mi", "mu", "me", "mo"],
    "Y": ["ya", "yu", "yo"],
    "R": ["ra", "ri", "ru", "re", "ro"],
    "W": ["wa", "wo"],
    "n": ["n"]
}

DAKUON = {
    "G": ["ga", "gi", "gu", "ge", "go"],
    "Z": ["za", "z_ji", "zu", "ze", "zo"],
    "D": ["da", "d_ji", "ju", "de", "do"],
    "B": ["ba", "bi", "bu", "be", "bo"]
}

HANDAKUON = {
    "P": ["pa", "pi", "pu", "pe", "po"]
}

COMBOSKANAS = {
    "K": ["kya", "kyu", "kyo"],
    "G": ["gya", "gyu", "gyo"],
    "S": ["sha", "shu", "sho"],
    "J": ["ja", "ju", "jo"],
    "C": ["cha", "chu", "cho"],
    "N": ["nya", "nyu", "nyo"],
    "H": ["hya", "hyu", "hyo"],
    "B": ["bya", "byu", "byo"],
    "P": ["pya", "pyu", "pyo"],
    "M": ["mya", "myu", "myo"],
    "R": ["rya", "ryu", "ryo"]
}


def initListsFromKanasDicts():
    global simpleKanasList
    global dakuonList
    global handakuonList
    global combosKanasList
    global everyKanasList

    simpleKanasList = []
    for line in SIMPLEKANAS:
        for kana in SIMPLEKANAS[line]:
            simpleKanasList.append(kana)

    dakuonList = []
    for line in DAKUON:
        for kana in DAKUON[line]:
            dakuonList.append(kana)

    handakuonList = []
    for line in HANDAKUON:
        for kana in HANDAKUON[line]:
            handakuonList.append(kana)

    combosKanasList = []
    for line in COMBOSKANAS:
        for kana in COMBOSKANAS[line]:
            combosKanasList.append(kana)

    everyKanasList = simpleKanasList+dakuonList+handakuonList+combosKanasList


def randomRomajiToKana(alphabet, kanasSubsetIdx):
    global KANASSUBSETS

    global simpleKanasList
    global dakuonList
    global handakuonList
    global combosKanasList

    # The order must match with the input of selectKanasSubset
    # KANASSUBSETS = ["simple", "Dakuon", "Handakuon", "combo"]

    kanasSubsetString = KANASSUBSETS[kanasSubsetIdx-1]

    if kanasSubsetIdx == 1:
        usedKanasList = simpleKanasList
    elif kanasSubsetIdx == 2:
        usedKanasList = dakuonList
    elif kanasSubsetIdx == 3:
        usedKanasList = handakuonList
    elif kanasSubsetIdx == 4:
        usedKanasList = combosKanasList

    select1 = False
    score = 0
    while not select1:
        print(
            f"# How many {kanasSubsetString} for the game? (1-{len(usedKanasList)})\n")
        try:
            nbKanas = int(input("> "))
            if nbKanas >= 1 and nbKanas <= len(usedKanasList):
                select1 = True

                randKanasList = random.sample(usedKanasList, nbKanas)
                for idxKana in range(0, nbKanas):
                    kana = randKanasList[idxKana]
                    input(f"\n#{idxKana+1}\n Draw {kana}")
                    image = Image.open("{}/{}.png".format(alphabet, kana))
                    image.show(title="Kana #{}".format(idxKana))
                    image.close()
                    point = input("Press 1 if it is correct, 0 otherwise: ")
                    if point == '1':
                        score += 1

                # Score
                print(
                    f"\n Score: {score}/{nbKanas}, {(100.0*score/nbKanas):.01f}%")

            else:
                raise ValueError()
        except ValueError as err:
            print(f"Wrong choice (must be 1-{len(usedKanasList)})\n")
        except FileNotFoundError as err:
            print(f"WILL BE SOLVED SOON: missing image files: {err}\n")


def selectKanasSubset(alphabet):
    selected = False
    while not selected:
        print(
            f"# Which {alphabet} do you want to write?\n 1- Simple {alphabet}\n 2- Dakuon\n 3- Handakuon\n 4- Combo {alphabet}\n 0- Return\n")
        choice2 = input("> ")
        selected = True

        if choice2 == '1' or choice2 == '2' or choice2 == '3' or choice2 == '4':
            randomRomajiToKana(alphabet, int(choice2))
        elif choice2 == '0':
            return 0
        else:
            selected = False
            print("Wrong choice\n")


def main():
    random.seed()

    initListsFromKanasDicts()
    selected = False

    while not selected:
        print(
            "# Select mode\n 1- Random Romaji->Hiragana\n 2- Random Romaji->Katakana\n 0- Exit\n")
        choice1 = input("> ")
        selected = True

        if choice1 == '1':
            selectKanasSubset(alphabet='Hiragana')
        elif choice1 == '2':
            selectKanasSubset(alphabet='Katakana')
        elif choice1 == '0':
            sys.exit(0)
        else:
            selected = False
            print("Wrong choice\n")


if __name__ == '__main__':
    print('- learnKanas - \n')
    main()
