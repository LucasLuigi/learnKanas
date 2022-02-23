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
                        decipheredAndCorrect, rebuiltAndCorrectWord = decipherJapaneseWordsFromRomajiTranscription(
                            inputJapaWord, correctJapaWordsList)

                        if decipheredAndCorrect:
                            # FIXME behavior to validate
                            print(f" {rebuiltAndCorrectWord}\nCORRECT")
                            score += 1
                        else:
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


# Split a romaji word without space into the list of each its romaji
def splitRomajiWord(romajiWord):
    # TODO to implement
    # FIXME handle long consumns (new kanas? better: if double consums, consider it's っ+kana)

    romajiList = []
    return romajiList


# Because one romaji may be two different kana, the transcripted kana word is a matrix.
# For each character of the word (first level), every possibility (second level) will be explored and compared with the correct list
# This function must be called with the Hiraganas and the Katakana matrix
# FIXME this method does not work: i do not have 001
# FIXME handle long consumns (new kanas? better: if one item kanaWordMatrix begins with double consums, consider it's っ+kana)
def compareEveryCombinationWithTheCorrectList(kanaWordMatrix, correctJapaWordsList, possibleRebuiltWords):
    # This list will contain the index where get each kana from each list of kanaWordMatrix.
    # If the romaji word is "a ji ju", giving then two possibilities for each two last romaji, kanaWordIndices
    # will have these values: 000, 010, 011
    kanaWordIndices = [
        0] * len(kanaWordMatrix)
    for combination in range(possibleRebuiltWords):
        # TODO Build word from matrixes

        kanaWordRebuilt = ""
        for idxLetter in range(len(kanaWordMatrix)):
            chosenKana = kanaWordMatrix[idxLetter][kanaWordIndices[idxLetter]]
            kanaWordRebuilt += chosenKana

        incrementingDone = False
        # Smartly increment the indices to browse every possibility
        for idxLetter in range(len(kanaWordIndices)):
            if not incrementingDone:
                if kanaWordIndices[idxLetter] + 1 < len(kanaWordMatrix[idxLetter]):
                    # Continue to explore the possibility by just incrementing the first letter that we want
                    kanaWordIndices[idxLetter] += 1
                    incrementingDone = True
                else:
                    # We will increment the next "letter"
                    pass

        if kanaWordRebuilt in correctJapaWordsList:
            return kanaWordRebuilt

    return None


# Sometimes, the player can input a Japanese word only using romaji.
# This function tries to decipher it (transcript in into Japanese) and return if it is in the list of correct word for this exercise's step
def decipherJapaneseWordsFromRomajiTranscription(inputJapaWord, correctJapaWordsList):
    # FIXME Add robustness when a romaji in input does not exit

    decipheredAndCorrect = False
    rebuiltAndCorrectWord = None

    # In inputJapaWord is not readable, return deciphered=False
    if inputJapaWord != None and inputJapaWord != "":
        # Try to decipher romaji inputs
        # Romaji splitted by space
        romajiList = inputJapaWord.split(" ")

        if len(romajiList) == 1:
            romajiList = splitRomajiWord(inputJapaWord)

        # These 2 variables are not directly strings to support the possibility to have several kana for one romaji (ji, ju).
        # The combinatory will be explored below
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

            # Used to maximize the combinatory search below to rebuild the possible words from the matrix
            possibleRebuiltWords *= len(potentialRomajis)

            # From everyKanasHira, extract the hira translating the potential romaji using the index of everyKanasRoma
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

        # Compare the hiragana matrix's combinations with correctJapaWordsList
        returnedCorrectWord = compareEveryCombinationWithTheCorrectList(
            hiraganaWordMatrix, correctJapaWordsList, possibleRebuiltWords)

        if returnedCorrectWord == None:
            # If there is no result, compare the hiragana matrix's combinations with correctJapaWordsList
            returnedCorrectWord = compareEveryCombinationWithTheCorrectList(
                katakanaWordMatrix, correctJapaWordsList, possibleRebuiltWords)

        # Found a word in correctJapaWordsList
        if returnedCorrectWord != None:
            decipheredAndCorrect = True
            rebuiltAndCorrectWord = returnedCorrectWord
        # else: return False, None

    return decipheredAndCorrect, rebuiltAndCorrectWord


# Exercise: Japanese word to French word
def randomJapaneseToFrenchWord():
    print("")
    logging.info(
        "Japanese to French words exercises not yet implemented, please come back soon!")
    print("")

    # FIXME WIP, delete the above lines when implemented
    return False
