# -*-coding:Latin-1 -*

import sys
import random
from PIL import Image

from kanas import ALPHABETS, KANAS_SUBSETS, SIMPLE_KANAS_ROMA, DAKUON_ROMA, HANDAKUON_ROMA, COMBOS_KANAS_ROMA


def initListsFromKanasDicts():
    global simpleKanasList
    global dakuonList
    global handakuonList
    global combosKanasList
    global everyKanasList

    simpleKanasList = []
    for line in SIMPLE_KANAS_ROMA:
        for kana in SIMPLE_KANAS_ROMA[line]:
            simpleKanasList.append(kana)

    dakuonList = []
    for line in DAKUON_ROMA:
        for kana in DAKUON_ROMA[line]:
            dakuonList.append(kana)

    handakuonList = []
    for line in HANDAKUON_ROMA:
        for kana in HANDAKUON_ROMA[line]:
            handakuonList.append(kana)

    combosKanasList = []
    for line in COMBOS_KANAS_ROMA:
        for kana in COMBOS_KANAS_ROMA[line]:
            combosKanasList.append(kana)

    everyKanasList = simpleKanasList+dakuonList+handakuonList+combosKanasList


def randomRomajiToKana(alphabet, kanasSubsetIdx):
    global KANAS_SUBSETS

    global simpleKanasList
    global dakuonList
    global handakuonList
    global combosKanasList

    # The order must match with the input of selectKanasSubset
    # KANASSUBSETS = ["simple", "Dakuon", "Handakuon", "combo"]

    kanasSubsetString = KANAS_SUBSETS[kanasSubsetIdx-1]

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
    incorrectKanas = []
    while not select1:
        print(
            f"# How many {kanasSubsetString} for the game? (1-{len(usedKanasList)})\n")
        try:
            nbKanas = int(input("> "))
            if nbKanas >= 1 and nbKanas <= len(usedKanasList):
                select1 = True

                randKanasList = random.sample(usedKanasList, nbKanas)
                print("For each step, please draw the Kana written, then press Enter.\nThen, Enter 1 if you drew correctly. Eventually, press Enter to continue to the next Kana.")
                for idxKana in range(0, nbKanas):
                    kana = randKanasList[idxKana]
                    input(f"\n#{idxKana+1}\n {kana}")
                    image = Image.open("{}/{}.png".format(alphabet, kana))
                    image.show(title="Kana #{}".format(idxKana))
                    image.close()
                    point = input("Correct? ")
                    if point == '1':
                        score += 1
                    else:
                        incorrectKanas.append(kana)

                # Score
                print(
                    f"\n Score: {score}/{nbKanas}, {(100.0*score/nbKanas):.01f}%\n")
                print("List of every incorrect Kanas:")
                for incorrectKana in incorrectKanas:
                    # TODO: improve this by writing the Japanese character?
                    print(f" {incorrectKana}")

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
