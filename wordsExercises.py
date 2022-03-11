# -*-coding:utf-8 -*

import logging
import re
import sys
import random

# FIXME
import config

import kanas
import words


# Exception when it is not correct that a specific romaji follows a っ
class LittleTsuError(SyntaxError):
    pass


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
                # FIXME to change
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
                            print(f"{rebuiltAndCorrectWord}\nCORRECT")
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
    # FIXME handle long consonant (new kanas? better: if double consonant, consider it's っ+kana)

    romajiList = [romajiWord]
    return romajiList


# Because one romaji may transcript two different kana, the transcripted kana word is a matrix.
# For each character of the word (first level), every possibility (second level) will be explored and compared with the correct list
# This function must be called with the Hiraganas and the Katakana matrix
def compareEveryCombinationWithTheCorrectList(kanaWordMatrix, correctJapaWordsList, rebuiltWord="", matrixIndex=0):
    # This list will contain the index where get each kana from each list of kanaWordMatrix.
    # If the romaji word is "a ji ju", giving then two possibilities for each two last romaji, kanaWordIndices
    # will have these values: 000, 010, 011

    # Should not occur
    if len(kanaWordMatrix) == 0:
        logging.error(
            "Something went wrong, no romaji were detected in your input")
        return False, None

    idxPossibleKana = 0
    for possibleKana in kanaWordMatrix[matrixIndex]:
        logging.debug(
            f'[compareEveryCombinationWithTheCorrectList] #{matrixIndex}#{idxPossibleKana}: {rebuiltWord}+{possibleKana}')

        rebuiltWordWithCurrentKana = rebuiltWord+possibleKana
        if matrixIndex == len(kanaWordMatrix)-1:
            # Check rebuilt word (end condition)
            if rebuiltWordWithCurrentKana in correctJapaWordsList:
                logging.debug(
                    '[compareEveryCombinationWithTheCorrectList] SUCCESS')
                return True, rebuiltWordWithCurrentKana
            else:
                logging.debug(
                    '[compareEveryCombinationWithTheCorrectList] FAILED')
                return False, None
        else:
            # Iterate
            returnedStatus, returnedWord = compareEveryCombinationWithTheCorrectList(
                kanaWordMatrix, correctJapaWordsList, rebuiltWordWithCurrentKana, matrixIndex+1)
            # Stop the search and return True, returnedWord
            if returnedStatus:
                return returnedStatus, returnedWord
            # Else, continue the search

        idxPossibleKana += 1

    return False, None


# Sometimes, the player can input a Japanese word only using romaji.
# This function tries to decipher it (transcript in into Japanese) and return if it is in the list of correct words for this exercise's step
def decipherJapaneseWordsFromRomajiTranscription(inputJapaWord, correctJapaWordsList):
    decipheredAndCorrect = False
    rebuiltAndCorrectWord = None

    try:
        # In inputJapaWord is not readable, return deciphered=False
        # If inputJapaWord is made of Kanas, we should not try to decipher it: return False
        if inputJapaWord != None and inputJapaWord != "" and inputJapaWord.strip(" ")[0] < "z" and inputJapaWord.strip(" ")[0] > "0":
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

            for romaji in romajiList:
                if romaji in kanas.AMBIGUOUS_ROMAJI_LIST:
                    # Ambiguous case when a Romaji can be several hira/katakana
                    potentialRomajis = kanas.AMBIGUOUS_ROMAJI_DICT[kanas.AMBIGUOUS_ROMAJI_LIST.index(
                        romaji)][romaji]
                else:
                    # Not ambiguous: the potential romajis are in fact just the only one here
                    potentialRomajis = [romaji]

                # From everyKanasHira, extract the hira translating the potential romaji using the index of everyKanasRoma
                potentialHira = [""] * len(potentialRomajis)
                idxPotentialRoma = 0
                for roma in potentialRomajis:
                    # Double consonant
                    if len(roma) > 2 and roma[0] == roma[1]:
                        logging.debug(
                            f"[decipherJapaneseWordsFromRomajiTranscription] Hira: double consonant '{roma[0]}'")

                        potentialHira[idxPotentialRoma] += "っ"
                        # Checking if the rest of the romaji is authorized to be prefixed by っ
                        if roma[1:] in kanas.ROMAJI_AUTHORIZING_LITTLE_TSU_PREFIX_LIST:
                            consolidatedRoma = roma[1:]
                        else:
                            raise LittleTsuError(roma[1:])
                    else:
                        consolidatedRoma = roma

                    potentialHira[idxPotentialRoma] += kanas.rootKanasHira[-1][kanas.rootKanasRoma[-1].index(
                        consolidatedRoma)]
                    idxPotentialRoma += 1
                hiraganaWordMatrix[idxLetter] = potentialHira

                # FIXME
                if config.NOT_IMPLEMENTED_YET == False:
                    logging.error("NOT_IMPLEMENTED_YET")
                    # From everyKanasKata, extract the kata translating the potential romaji using the index of everyKanasRoma
                    potentialKata = [""] * len(potentialRomajis)
                    idxPotentialRoma = 0
                    for roma in potentialRomajis:
                        # Double consonant
                        if len(roma) > 2 and roma[0] == roma[1]:
                            logging.debug(
                                f"[decipherJapaneseWordsFromRomajiTranscription] Kana: double consonant '{roma[0]}'")

                            potentialKata[idxPotentialRoma] += "っ"
                            # Checking if the rest of the romaji is authorized to be prefixed by っ
                            if roma[1:] in kanas.ROMAJI_AUTHORIZING_LITTLE_TSU_PREFIX_LIST:
                                consolidatedRoma = roma[1:]
                            else:
                                raise LittleTsuError(roma[1:])
                        else:
                            consolidatedRoma = roma

                        potentialKata[idxPotentialRoma] += kanas.rootKanasKata[-1][kanas.rootKanasRoma[-1].index(
                            consolidatedRoma)]
                        idxPotentialRoma += 1
                    katakanaWordMatrix[idxLetter] = potentialKata

                idxLetter += 1

            # Compare the Hiragana matrix's combinations with correctJapaWordsList
            returnedStatus, returnedWord = compareEveryCombinationWithTheCorrectList(
                hiraganaWordMatrix, correctJapaWordsList)

            if not returnedStatus:
                # FIXME
                if config.NOT_IMPLEMENTED_YET == False:
                    # If there is no result, compare the Katakana matrix's combinations with correctJapaWordsList
                    returnedStatus, returnedWord = compareEveryCombinationWithTheCorrectList(
                        katakanaWordMatrix, correctJapaWordsList)
            # Found a word in correctJapaWordsList
            if returnedStatus:
                decipheredAndCorrect = True
                rebuiltAndCorrectWord = returnedWord
            # else: return False, None

    # Exception when a romaji does not exist
    except ValueError as err:
        print(
            f'There is something wrong with your input: "{romaji}" is NOT a Romaji')

    except LittleTsuError as err:
        print(
            f'There is something wrong with your input: "{err}" cannot follow っ')

    return decipheredAndCorrect, rebuiltAndCorrectWord


# Exercise: Japanese word to French word
def randomJapaneseToFrenchWord():
    print("")
    logging.info(
        "Japanese to French words exercises not yet implemented, please come back soon!")
    print("")

    # FIXME WIP, delete the above lines when implemented
    return False
