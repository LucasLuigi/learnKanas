# -*-coding:utf-8 -*
import logging
import sys
import random

# FIXME
import config

import kanas
import words


# Select the translation between both directions
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


# Exercise: French word to Japanese word
def randomFrenchToJapaneseWord():
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
                                if config.NOT_IMPLEMENTED_YET == False:
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
                                if config.NOT_IMPLEMENTED_YET == False:
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


# Exercise: Japanese word to French word
def randomJapaneseToFrenchWord():
    print("")
    logging.info(
        "Japanese to French words exercises not yet implemented, please come back soon!")
    print("")

    # FIXME WIP, delete the above lines when implemented
    return False
