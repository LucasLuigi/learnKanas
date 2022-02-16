# -*-coding:utf-8 -*

import logging
import sys
import random

import kanas
import words

# FIXME
NOT_IMPLEMENTED_YET = True

DEBUG_LEVEL = 'DEBUG'


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

                if score < nbKanas:
                    print("List of every incorrect Kanas:")
                    # Using List comprehension to remove none values
                    incorrectKanasRomaCompacted = [
                        elem for elem in incorrectKanasRoma if elem is not None]
                    for incorrectKana in incorrectKanasRomaCompacted:
                        print(
                            f" {incorrectKana:<4} - {usedKanasJapa[usedKanasRoma.index(incorrectKana)]:>2}")
                    print("")

            else:
                raise ValueError()
        except ValueError:
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

    selected = False
    score = 0
    incorrectKanasJapa = [None] * len(usedKanasJapa)
    while not selected:
        print(
            f"# How many {kanasSubsetString} for the game? (1-{len(usedKanasJapa)}, enter 0 for all)\n")
        try:
            nbKanas = int(input("> "))
            # 0 : select every kanas
            if nbKanas == 0:
                nbKanas = len(usedKanasJapa)
            if nbKanas >= 1 and nbKanas <= len(usedKanasJapa):
                selected = True

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

                if score < nbKanas:
                    print("List of every incorrect Kanas:")
                    # Using List comprehension to remove none values
                    incorrectKanasJapaCompacted = [
                        elem for elem in incorrectKanasJapa if elem is not None]
                    for incorrectKana in incorrectKanasJapaCompacted:
                        print(
                            f" {incorrectKana:<4} - {usedKanasRoma[usedKanasJapa.index(incorrectKana)]:>2}")
                    print("")

            else:
                raise ValueError()
        except ValueError:
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
        choice3 = input("> ")
        selected = True

        if choice3 >= '1' and choice3 <= '5':
            if way == 0:
                randomRomajiToKana(alphabet, int(choice3))
            else:
                randomKanaToRomaji(alphabet, int(choice3))
        elif choice3 == '0':
            return False
        else:
            selected = False
            print("Wrong choice\n")
    return True


def selectKanasExercise():
    selected2 = False
    while not selected2:
        print(
            "# Select mode\n 1- Random Romaji->Hiragana\n 2- Random Hiragana->Romaji\n 3- Random Romaji->Katakana\n 4- Random Katakana->Romaji\n 0- Return\n")
        choice2 = input("> ")
        selected2 = True

        if choice2 == '1':
            selected2 = selectKanasSubset(alphabet='Hiragana', way=0)
        elif choice2 == '2':
            selected2 = selectKanasSubset(alphabet='Hiragana', way=1)
        elif choice2 == '3':
            selected2 = selectKanasSubset(alphabet='Katakana', way=0)
        elif choice2 == '4':
            selected2 = selectKanasSubset(alphabet='Katakana', way=1)
        elif choice2 == '0':
            return False
        else:
            selected2 = False
            print("Wrong choice\n")

    return True


def randomFrenchToJapaneseWord():
    # FIXME
    global NOT_IMPLEMENTED_YET

    select1 = False
    score = 0
    frenchWordsNumber = len(words.frenchToJapaWordsDict)
    incorrectFrenchWords = []

    while not select1:
        print(
            f"# How many words for the game? (1-{frenchWordsNumber}, enter 0 for all)\n")
        try:
            nbWords = int(input("> "))
            # 0 : select every word
            if nbWords == 0:
                nbWords = frenchWordsNumber
            if nbWords >= 1 and nbWords <= frenchWordsNumber:
                select1 = True

                randFrenchWords = random.sample(
                    list(words.frenchToJapaWordsDict.keys()), nbWords)
                print(
                    "- IMPORTANT -\n- SCORE     -\n\nFor each word, enter the correct translation, then press Enter.")
                print(
                    "WARNING - For the moment, you must use a Japanese keyboard to answer. This limitation will be fixed soon.")
                for idxExercise in range(0, nbWords):
                    frenchWord = randFrenchWords[idxExercise]
                    inputJapaWord = input(
                        f"\n#{idxExercise+1}/{nbWords}\n {frenchWord}\n ").strip(" ").lower()
                    correctJapaWordsList = words.frenchToJapaWordsDict[frenchWord]

                    if inputJapaWord in correctJapaWordsList:
                        print("CORRECT")
                        score += 1
                    else:
                        if inputJapaWord != None and inputJapaWord != "":
                            # Try to decrypt romaji inputs
                            # Romaji splitted by space
                            romajiList = inputJapaWord.split(" ")

                            # These 2 variables are not directly strings to support the possibility to have several kana for one romaji (ji, ju).
                            # The combinatory will be browsed below
                            hiraganaWordMatrix = [None] * len(romajiList)
                            katakanaWordMatrix = [None] * len(romajiList)

                            idxLetter = 0
                            possibleRebuiltWords = 1

                            for romaji in romajiList:
                                if romaji in kanas.AMBIGUOUS_ROMAJI_LIST:
                                    # Ambiguous case when a Romaji can be several hira/katakana
                                    potentialRomajis = kanas.AMBIGUOUS_ROMAJI_DICT[kanas.AMBIGUOUS_ROMAJI_LIST.index(
                                        romaji)][romaji]
                                else:
                                    # Not ambiguous: the potential romajis are in fact the only one
                                    potentialRomajis = [romaji]

                                # Used to maximize the loop used below to rebuild the possible words from the matrix
                                possibleRebuiltWords *= len(potentialRomajis)

                                # From everyKanasHira, extract the hira translating the romaji using the index of everyKanasRoma

                                potentialHira = [kanas.rootKanasHira[-1][kanas.rootKanasRoma[-1].index(
                                    roma)] for roma in potentialRomajis]
                                hiraganaWordMatrix[idxLetter] = potentialHira

                                # FIXME
                                if NOT_IMPLEMENTED_YET == False:
                                    logging.error("NOT_IMPLEMENTED_YET")
                                    potentialKata = [kanas.rootKanasKata[-1][kanas.rootKanasRoma[-1].index(
                                        roma)] for roma in potentialRomajis]
                                    katakanaWordMatrix[idxLetter] = potentialKata

                                idxLetter += 1

                            oneOfTheCombinationIsCorrect = False
                            # This list will contain the index where get each hiraganas from each list of hiraganaWordMatrix.
                            # If the romaji word is "a ji ju", giving then two possibilities for each two last romaji, hiraganaWordIndices
                            # will have these values: 000, 010, 011
                            hiraganaWordIndices = [
                                0] * len(hiraganaWordMatrix)

                            # FIXME this method does not work: i do not have 001
                            for combination in range(possibleRebuiltWords):
                                # TODO Build word from matrixes

                                hiraganaWordRebuilt = ""
                                for idxLetter in range(len(hiraganaWordMatrix)):
                                    chosenKana = hiraganaWordMatrix[idxLetter][hiraganaWordIndices[idxLetter]]
                                    hiraganaWordRebuilt += chosenKana

                                incrementingDone = False
                                # Smartly increment the indices to browse every possibility
                                for idxLetter in range(len(hiraganaWordIndices)):
                                    if not incrementingDone:
                                        if hiraganaWordIndices[idxLetter] + 1 < len(hiraganaWordMatrix[idxLetter]):
                                            # Continue to explore the possibility by just incrementing the first letter that we want
                                            hiraganaWordIndices[idxLetter] += 1
                                            incrementingDone = True
                                        else:
                                            # We will increment the next "letter"
                                            pass

                                if hiraganaWordRebuilt in correctJapaWordsList:
                                    correctCombination = hiraganaWordRebuilt
                                    oneOfTheCombinationIsCorrect = True

                                # FIXME
                                if NOT_IMPLEMENTED_YET == False:
                                    logging.error("NOT_IMPLEMENTED_YET")
                                    katakanaWordRebuilt = ""
                                    if 1 == 0:
                                        pass
                                    elif katakanaWordRebuilt in correctJapaWordsList:
                                        correctCombination = katakanaWordRebuilt
                                        oneOfTheCombinationIsCorrect = True

                            if oneOfTheCombinationIsCorrect:
                                print(f" {correctCombination}\nCORRECT")
                                score += 1
                            else:

                                # Romaji not splitted by space
                                # TODO

                                # Definitely incorrect
                                incorrectAnswerString = "INCORRECT, it was "

                                if len(correctJapaWordsList) == 1:
                                    incorrectAnswerString += correctJapaWordsList[0]
                                elif len(correctJapaWordsList) == 2:
                                    for word in correctJapaWordsList[:-1]:
                                        incorrectAnswerString += word
                                    incorrectAnswerString += " or " + \
                                        correctJapaWordsList[-1]
                                else:
                                    for word in correctJapaWordsList[:-2]:
                                        incorrectAnswerString += word + ", "
                                    incorrectAnswerString += correctJapaWordsList[-2] + \
                                        " or " + correctJapaWordsList[-1]
                                print(incorrectAnswerString)
                                incorrectFrenchWords.append(frenchWord)

                        else:
                            # FIXME Dirty, to refacto

                            # Definitely incorrect
                            incorrectAnswerString = "INCORRECT, it was "

                            if len(correctJapaWordsList) == 1:
                                incorrectAnswerString += correctJapaWordsList[0]
                            elif len(correctJapaWordsList) == 2:
                                for word in correctJapaWordsList[:-1]:
                                    incorrectAnswerString += word
                                incorrectAnswerString += " or " + \
                                    correctJapaWordsList[-1]
                            else:
                                for word in correctJapaWordsList[:-2]:
                                    incorrectAnswerString += word + ", "
                                incorrectAnswerString += correctJapaWordsList[-2] + \
                                    " or " + correctJapaWordsList[-1]
                            print(incorrectAnswerString)
                            incorrectFrenchWords.append(frenchWord)

                # Score
                print(
                    f"\nScore: {score}/{nbWords}, {(100.0*score/nbWords):.01f}%\n")

                if score < nbWords:
                    print("List of every incorrect translation:")
                    for incorrectWord in incorrectFrenchWords:
                        print(
                            f" {incorrectWord} - {words.frenchToJapaWordsDict[incorrectWord]}")
                    print("")

            else:
                raise ValueError()
        except ValueError:
            print(f"Wrong choice (must be 1-{frenchWordsNumber})\n")

    return True


def randomJapaneseToFrenchWord():
    print("")
    logging.info(
        "Japanese to French words exercises not yet implemented, please come back soon!")
    print("")

    # FIXME WIP, delete the above lines when implemented
    return False


def selectWordsExercise():
    selected2 = False
    while not selected2:
        print(
            "# Select mode\n 1- Random French word->Japanese word\n 2- Random Japanese word->French word\n 0- Return\n")
        choice1 = input("> ")
        selected2 = True

        if choice1 == '1':
            selected2 = randomFrenchToJapaneseWord()
        elif choice1 == '2':
            selected2 = randomJapaneseToFrenchWord()
        elif choice1 == '0':
            return False
        else:
            selected2 = False
            print("Wrong choice\n")

    return True


def main():
    global DEBUG_LEVEL

    logger = logging.getLogger()
    logger.setLevel(DEBUG_LEVEL)

    random.seed()

    kanas.initFlattenedKanas()
    words.initWords()

    selected1 = False
    while not selected1:
        print(
            "# Select category\n 1- Kanas exercises (characters)\n 2- Words exercises\n 0- Exit\n")
        choice1 = input("> ")
        selected1 = True

        if choice1 == '1':
            selected1 = selectKanasExercise()
        elif choice1 == '2':
            selected1 = selectWordsExercise()
        elif choice1 == '0':
            sys.exit(0)
        else:
            selected1 = False
            print("Wrong choice\n")


if __name__ == '__main__':
    print('- learnKanas - \n\nようこそ！\n\nIf the sentence above is only blank squares instead of Japanese Hiragana, something is wrong with your terminal.\nOn Windows run chcp 936 (or chcp 932) before launching learnKanas again\n')
    main()
    print('Thank you for playing!\nGame made by LucasLuigi - https://github.com/LucasLuigi/learnKanas')
