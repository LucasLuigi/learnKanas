# -*-coding:utf-8 -*

# set PYTHONIOENCODING=UTF-8 - useless
# chcp 936

import logging
import sys
import random
from PIL import Image

from kanas import ALPHABETS, KANAS_SUBSETS
from kanas import SIMPLE_KANAS_ROMA, DAKUON_ROMA, HANDAKUON_ROMA, COMBOS_KANAS_ROMA
from kanas import SIMPLE_KANAS_HIRA, DAKUON_HIRA, HANDAKUON_HIRA, COMBOS_KANAS_HIRA

# True to display Kanas in the CLI, False to open a picture of it
kanasDisplayedExternally = False


def initListsFromKanasDicts():
    global rootKanasRoma
    global rootKanasHira
    global rootKanasKata

    global simpleKanasRoma
    global simpleKanasHira
    global dakuonRoma
    global dakuonHira
    global handakuonRoma
    global handakuonHira
    global combosKanasRoma
    global combosKanasHira
    global everyKanasRoma
    global everyKanasHira

    # Flattening each multi-level constant kanas lists

    # Simple Kanas
    simpleKanasRoma = []
    for line in SIMPLE_KANAS_ROMA:
        for kana in SIMPLE_KANAS_ROMA[line]:
            simpleKanasRoma.append(kana)

    simpleKanasHira = []
    for line in SIMPLE_KANAS_HIRA:
        for kana in SIMPLE_KANAS_HIRA[line]:
            simpleKanasHira.append(kana)

    simpleKanasKata = []

    # Dakuon ゛
    dakuonRoma = []
    for line in DAKUON_ROMA:
        for kana in DAKUON_ROMA[line]:
            dakuonRoma.append(kana)

    dakuonHira = []
    for line in DAKUON_HIRA:
        for kana in DAKUON_HIRA[line]:
            dakuonHira.append(kana)

    dakuonKata = []

    # Handakuon ゜
    handakuonRoma = []
    for line in HANDAKUON_ROMA:
        for kana in HANDAKUON_ROMA[line]:
            handakuonRoma.append(kana)

    handakuonHira = []
    for line in HANDAKUON_HIRA:
        for kana in HANDAKUON_HIRA[line]:
            handakuonHira.append(kana)

    handakuonKata = []

    # Combos Kanas
    combosKanasRoma = []
    for line in COMBOS_KANAS_ROMA:
        for kana in COMBOS_KANAS_ROMA[line]:
            combosKanasRoma.append(kana)

    combosKanasHira = []
    for line in COMBOS_KANAS_HIRA:
        for kana in COMBOS_KANAS_HIRA[line]:
            combosKanasHira.append(kana)

    combosKanasKata = []

    # Every Kanas (combining every previous ones)
    everyKanasRoma = simpleKanasRoma + dakuonRoma + handakuonRoma + combosKanasRoma
    everyKanasHira = simpleKanasHira + dakuonHira + handakuonHira + combosKanasHira
    everyKanasKata = simpleKanasKata + dakuonKata + handakuonKata + combosKanasKata

    # List of lists
    rootKanasRoma = [simpleKanasRoma, dakuonRoma,
                     handakuonRoma, combosKanasRoma, everyKanasRoma]
    rootKanasHira = [simpleKanasHira, dakuonHira,
                     handakuonHira, combosKanasHira, everyKanasHira]
    rootKanasKata = [simpleKanasKata, dakuonKata,
                     handakuonKata, combosKanasKata, everyKanasKata]


def randomRomajiToKana(alphabet, kanasSubsetIdx):
    global KANAS_SUBSETS

    global kanasDisplayedExternally

    global rootKanasRoma
    global rootKanasHira
    global rootKanasKata

    try:
        # kanasSubsetIdx start with 1, as 0 is the exit input in the menu
        usedKanasRoma = rootKanasRoma[kanasSubsetIdx-1]
        if alphabet == 'Hiragana':
            usedKanasJapo = rootKanasHira[kanasSubsetIdx-1]
        elif alphabet == 'Katakana':
            usedKanasJapo = rootKanasKata[kanasSubsetIdx-1]
        else:
            logging.error(
                f"[X] randomRomajiToKana: alphabet {alphabet} not recognized")
            return -1
    except IndexError as err:
        logging.error(
            f"[X] randomRomajiToKana: kanasSubsetIdx {kanasSubsetIdx} out of rootKanasRoma's range\n{err}")
        return -1

     # The order must match the input of selectKanasSubset
    kanasSubsetString = KANAS_SUBSETS[kanasSubsetIdx-1]

    select1 = False
    score = 0
    incorrectKanasRoma = []
    while not select1:
        print(
            f"# How many {kanasSubsetString} for the game? (1-{len(usedKanasRoma)})\n")
        try:
            nbKanas = int(input("> "))
            if nbKanas >= 1 and nbKanas <= len(usedKanasRoma):
                select1 = True

                randKanasRoma = random.sample(usedKanasRoma, nbKanas)
                print("For each step, please draw the written Kana, then press Enter.\nThen, Enter 1 if you drew correctly. Eventually, press Enter to continue to the next Kana.")
                for idxExercise in range(0, nbKanas):
                    kanaRoma = randKanasRoma[idxExercise]
                    input(f"\n#{idxExercise+1}\n {kanaRoma}")
                    if kanasDisplayedExternally:
                        with Image.open(f"{alphabet}/{kanaRoma}.png") as im:
                            im.show(title=f"Kana #{idxExercise}")
                    else:
                        kanaJapo = usedKanasJapo[usedKanasRoma.index(kanaRoma)]
                        print(f" {kanaJapo}")
                    point = input("Correct? ")
                    if point == '1':
                        score += 1
                    else:
                        incorrectKanasRoma.append(kanaRoma)

                # Score
                print(
                    f"\nScore: {score}/{nbKanas}, {(100.0*score/nbKanas):.01f}%\n")
                print("List of every incorrect Kanas:")
                for incorrectKana in incorrectKanasRoma:
                    print(
                        f" {incorrectKana:<4} - {usedKanasJapo[usedKanasRoma.index(incorrectKana)]:>2}")

            else:
                raise ValueError()
        except ValueError as err:
            print(f"Wrong choice (must be 1-{len(usedKanasRoma)})\n")
        except FileNotFoundError as err:
            print(f"SHOULD BE SOLVED SOON: missing image files: {err}\n")


def selectKanasSubset(alphabet):
    selected = False
    while not selected:
        print(
            f"# Which {alphabet} do you want to write?\n 1- Simple {alphabet}\n 2- Dakuon\n 3- Handakuon\n 4- Combo {alphabet}\n 5- Every Kanas\n 0- Return\n")
        choice2 = input("> ")
        selected = True

        if choice2 >= '1' and choice2 <= '5':
            randomRomajiToKana(alphabet, int(choice2))
        elif choice2 == '0':
            return 0
        else:
            selected = False
            print("Wrong choice\n")


def main():
    logger = logging.getLogger()
    logger.setLevel('DEBUG')

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
    print('- learnKanas - \n\nようこそ！\n\nIf the sentence above was only blank squares instead of Japanese Hiragana, something is wrong with your terminal.\nRun chcp 936 (or chcp 932) before launching learnKanas again\n')
    main()
