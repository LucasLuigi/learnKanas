# -*-coding:utf-8 -*

import logging
import sys
import random

import kanas
import words


def randomRomajiToKana(alphabet, kanasSubsetIdx):
    try:
        # kanasSubsetIdx start with 1, as 0 is the exit input in the menu
        usedKanasRoma = kanas.rootKanasRoma[kanasSubsetIdx-1]
        if alphabet == 'Hiragana':
            usedKanasJapa = kanas.rootKanasHira[kanasSubsetIdx-1]
        elif alphabet == 'Katakana':
            usedKanasJapa = kanas.rootKanasKata[kanasSubsetIdx-1]
        else:
            logging.error(
                f"[X] randomRomajiToKana: alphabet {alphabet} not recognized")
            return -1
    except IndexError as err:
        logging.error(
            f"[X] randomRomajiToKana: kanasSubsetIdx {kanasSubsetIdx} out of rootKanasRoma's range\n{err}")
        return -1

     # The order must match the input of selectKanasSubset
    kanasSubsetString = kanas.KANAS_SUBSETS[kanasSubsetIdx-1]

    select1 = False
    score = 0
    incorrectKanasRoma = [None] * len(usedKanasRoma)
    while not select1:
        print(
            f"# How many {kanasSubsetString} for the game? (1-{len(usedKanasRoma)}, enter 0 for all)\n")
        try:
            nbKanas = int(input("> "))
            # 0 : select every kanas
            if nbKanas == 0:
                nbKanas = len(usedKanasRoma)
            if nbKanas >= 1 and nbKanas <= len(usedKanasRoma):
                select1 = True

                randKanasRoma = random.sample(usedKanasRoma, nbKanas)
                print("- IMPORTANT -\n- SCORE     -\n\nFor each step, please draw the written Kana on a sheet besides, then press Enter.\nThen, Enter 1 if you drew correctly. Eventually, press Enter to continue to the next Kana.")
                for idxExercise in range(0, nbKanas):
                    kanaRoma = randKanasRoma[idxExercise]
                    input(
                        f"\n#{idxExercise+1}/{nbKanas}\n {kanaRoma}")
                    kanaJapa = usedKanasJapa[usedKanasRoma.index(kanaRoma)]
                    print(f" {kanaJapa}")
                    point = input("Correct? ")
                    if point == '1':
                        score += 1
                    else:
                        incorrectKanasRoma[usedKanasRoma.index(
                            kanaRoma)] = kanaRoma

                # Score
                print(
                    f"\nScore: {score}/{nbKanas}, {(100.0*score/nbKanas):.01f}%\n")

                print("List of every incorrect Kanas:")
                # Using List comprehension to remove none values
                incorrectKanasRomaCompacted = [
                    elem for elem in incorrectKanasRoma if elem is not None]
                for incorrectKana in incorrectKanasRomaCompacted:
                    print(
                        f" {incorrectKana:<4} - {usedKanasJapa[usedKanasRoma.index(incorrectKana)]:>2}")

            else:
                raise ValueError()
        except ValueError as err:
            print(f"Wrong choice (must be 1-{len(usedKanasRoma)})\n")


def randomKanaToRomaji(alphabet, kanasSubsetIdx):
    try:
        # kanasSubsetIdx start with 1, as 0 is the exit input in the menu
        usedKanasRoma = kanas.rootKanasRoma[kanasSubsetIdx-1]
        if alphabet == 'Hiragana':
            usedKanasJapa = kanas.rootKanasHira[kanasSubsetIdx-1]
        elif alphabet == 'Katakana':
            usedKanasJapa = kanas.rootKanasKata[kanasSubsetIdx-1]
        else:
            logging.error(
                f"[X] randomRomajiToKana: alphabet {alphabet} not recognized")
            return -1
    except IndexError as err:
        logging.error(
            f"[X] randomRomajiToKana: kanasSubsetIdx {kanasSubsetIdx} out of rootKanasRoma's range\n{err}")
        return -1

     # The order must match the input of selectKanasSubset
    kanasSubsetString = kanas.KANAS_SUBSETS[kanasSubsetIdx-1]

    select1 = False
    score = 0
    incorrectKanasJapa = [None] * len(usedKanasJapa)
    while not select1:
        print(
            f"# How many {kanasSubsetString} for the game? (1-{len(usedKanasJapa)}, enter 0 for all)\n")
        try:
            nbKanas = int(input("> "))
            # 0 : select every kanas
            if nbKanas == 0:
                nbKanas = len(usedKanasJapa)
            if nbKanas >= 1 and nbKanas <= len(usedKanasJapa):
                select1 = True

                randKanasJapa = random.sample(usedKanasJapa, nbKanas)
                print(
                    "- IMPORTANT -\n- SCORE     -\n\nFor each step, enter the correct Romaji, then press Enter.")
                for idxExercise in range(0, nbKanas):
                    kanaJapa = randKanasJapa[idxExercise]
                    inputKanaRoma = input(
                        f"\n#{idxExercise+1}/{nbKanas}\n {kanaJapa}\n ").lower()
                    correctKanaRoma = usedKanasRoma[usedKanasJapa.index(
                        kanaJapa)]

                    # Duplicated Romaji (such as the combo kana ju=じゅ and the dakuon ju=づ) have different names: a prefix <consomn_key>_ is added
                    # It is not interesting in this exercise to write the prefixed Romaji. [-1] is used to not overflow when correctKanaRoma have no prefix
                    if inputKanaRoma == correctKanaRoma.split('_')[-1]:
                        print("CORRECT")
                        score += 1
                    else:
                        print(
                            f"INCORRECT, it was {correctKanaRoma.split('_')[-1]}")
                        incorrectKanasJapa[usedKanasJapa.index(
                            kanaJapa)] = kanaJapa

                # Score
                print(
                    f"\nScore: {score}/{nbKanas}, {(100.0*score/nbKanas):.01f}%\n")

                print("List of every incorrect Kanas:")
                # Using List comprehension to remove none values
                incorrectKanasJapaCompacted = [
                    elem for elem in incorrectKanasJapa if elem is not None]
                for incorrectKana in incorrectKanasJapaCompacted:
                    print(
                        f" {incorrectKana:<4} - {usedKanasRoma[usedKanasJapa.index(incorrectKana)]:>2}")

            else:
                raise ValueError()
        except ValueError as err:
            print(f"Wrong choice (must be 1-{len(usedKanasJapa)})\n")


# alphabet: a string to select the Japanese alphabet (must match ALPHABETS)
# way: 0 for Romaji to Kana, 1 for Kana to Romajo
def selectKanasSubset(alphabet, way):
    # way = 0: write Kanas
    # way = 1: guess Kanas
    possibleActions = ['write', 'guess']

    selected = False
    if alphabet not in kanas.ALPHABETS or way < 0 or way > 1:
        logging.error(f"selectKanasSubset: wrong options {alphabet} or {way}")
        sys.exit(-1)

    if alphabet == 'Katakana':
        logging.warning("[!] Katakana not yet implemented, coming soon...")

    while not selected:
        print(
            f"# Which {alphabet} do you want to {possibleActions[way]}?\n 1- Simple {alphabet}\n 2- Dakuon\n 3- Handakuon\n 4- Combo {alphabet}\n 5- Every Kanas\n 0- Return\n")
        choice2 = input("> ")
        selected = True

        if choice2 >= '1' and choice2 <= '5':
            if way == 0:
                randomRomajiToKana(alphabet, int(choice2))
            else:
                randomKanaToRomaji(alphabet, int(choice2))
        elif choice2 == '0':
            return False
        else:
            selected = False
            print("Wrong choice\n")
    return True


def main():
    logger = logging.getLogger()
    logger.setLevel('DEBUG')

    random.seed()

    kanas.initFlattenedKanas()
    words.initWords()
    selected = False

    while not selected:
        print(
            "# Select mode\n 1- Random Romaji->Hiragana\n 2- Random Hiragana->Romaji\n 3- Random Romaji->Katakana\n 4- Random Katakana->Romaji\n 0- Exit\n")
        choice1 = input("> ")
        selected = True

        if choice1 == '1':
            selected = selectKanasSubset(alphabet='Hiragana', way=0)
        elif choice1 == '2':
            selected = selectKanasSubset(alphabet='Hiragana', way=1)
        elif choice1 == '3':
            selected = selectKanasSubset(alphabet='Katakana', way=0)
        elif choice1 == '4':
            selected = selectKanasSubset(alphabet='Katakana', way=1)
        elif choice1 == '0':
            sys.exit(0)
        else:
            selected = False
            print("Wrong choice\n")


if __name__ == '__main__':
    print('- learnKanas - \n\nようこそ！\n\nIf the sentence above is only blank squares instead of Japanese Hiragana, something is wrong with your terminal.\nOn Windows run chcp 936 (or chcp 932) before launching learnKanas again\n')
    main()
