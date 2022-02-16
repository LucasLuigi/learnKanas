# -*-coding:utf-8 -*

import logging
from os import listdir
from os.path import isfile, join
from pathlib import Path

import kanas

frenchToJapaWordsDict = {}
japaToFrenchWordsDict = {}


def buildFrenchToJapaWordsDict(wordFileContent, wordFileName):
    global frenchToJapaWordsDict

    for line in wordFileContent:
        splittedLine = line.strip(" ").split(" ")
        if len(splittedLine) < 2:
            logging.warning(
                f"The words '{line}' from {wordFileName} will not be imported\nReason: it is not correctly formatted: 'frenchWord japaneseWord'\n")
        else:
            continueToParseLine = True
            japaWordsSeq = splittedLine[-1].strip("\n")
            for kana in kanas.rootKanasHira[kanas.KANAS_SUBSETS.index("Kanas")]:
                if kana in splittedLine[-2]:
                    continueToParseLine = False
                    logging.warning(
                        f"The words '{line}' from {wordFileName} will not be imported\nReason: it is not correctly formatted: the japanese word is splitted by a space\n")

            if continueToParseLine:
                japaWordsList = japaWordsSeq.split("/")
                # Regroup French words (everyone but the last)
                frenchWord = ""
                for splittedWord in splittedLine[:-1]:
                    frenchWord = frenchWord + splittedWord + " "
                frenchWord = frenchWord.strip(" ").lower()

                if frenchWord in frenchToJapaWordsDict:
                    # A list of japanese words already exists at the key of frenchToJapaWordsDict
                    # Append
                    for japaWord in japaWordsList:
                        frenchToJapaWordsDict[frenchWord].append(japaWord)
                else:
                    # Append the list to a new key
                    frenchToJapaWordsDict[frenchWord] = japaWordsList

    logging.debug("French to Japanese: words dict:")
    for key in frenchToJapaWordsDict:
        logging.debug(f"{key}: {frenchToJapaWordsDict[key]}")
    logging.debug("############################################")


# Reverse the French to Japanese words dictionnary to make a Japanese to French dictionnary
def buildJapaToFrenchWordsDict():
    global frenchToJapaWordsDict
    global japaToFrenchWordsDict

    for frenchWord in frenchToJapaWordsDict:
        for japaWord in frenchToJapaWordsDict[frenchWord]:
            # japaWord will be the key of the new dict
            # Example of "bye/à plus/à bientot": they all have the same translation in Japanese. In the French to Japa dict, they appear three time.
            # In this Japa to French dict, there will be one key, じゃあね, and 3 french words in the value (the list)
            if japaWord not in japaToFrenchWordsDict:
                # Append a new list to a new key
                japaToFrenchWordsDict[japaWord] = []
            # If a list of French words already exists at the key of japaToFrenchWordsDict, append only in the existing list at japaToFrenchWordsDict[japaWord]
            japaToFrenchWordsDict[japaWord].append(frenchWord)


# Check if each word in one dict is in the other one
def checkDicts():
    global frenchToJapaWordsDict
    global japaToFrenchWordsDict

    # Check if each word in one dict is in the other one
    for frenchKey in frenchToJapaWordsDict:
        if len(frenchToJapaWordsDict[frenchKey]) == 0:
            logging.warning(
                f"Someting went wrong: {frenchKey} seems to not have any translation in the line where it is written.")
        for japaWord in frenchToJapaWordsDict[frenchKey]:
            if japaWord not in japaToFrenchWordsDict:
                logging.warning(
                    f"Someting went wrong: {japaWord} not in the dynamically built Japanese to French dictionary.")

    for japaKey in japaToFrenchWordsDict:
        if len(japaToFrenchWordsDict[japaKey]) == 0:
            logging.warning(
                f"Someting went wrong: {japaKey} seems to not have any translation in the line where it is written.")
        for frenchWord in japaToFrenchWordsDict[japaKey]:
            if frenchWord not in frenchToJapaWordsDict:
                logging.warning(
                    f"Someting went wrong: {frenchWord} not in the dynamically built Japanese to French dictionary.")


def initWords():
    WORDS_RELATIVE_PATH = "./wordsLists"

    logging.debug(
        "words.initWords: importing file in wordLists/ to fill the list used by the learnKanas words' exercise...")

    wordsFiles = [f for f in listdir(
        WORDS_RELATIVE_PATH) if isfile(join(WORDS_RELATIVE_PATH, f))]

    for wordsFile in wordsFiles:
        logging.debug(
            f"words.initWords: {wordsFile} will be imported")
        with open(f"{WORDS_RELATIVE_PATH}/{wordsFile}", "r", encoding="utf-8") as wordsFileContent:
            buildFrenchToJapaWordsDict(wordsFileContent, wordsFile)

    buildJapaToFrenchWordsDict()

    logging.debug("Japanese to French: words dict:")
    for key in japaToFrenchWordsDict:
        logging.debug(f"{key}: {japaToFrenchWordsDict[key]}")
    logging.debug("############################################")

    checkDicts()

    logging.debug(
        "words.initWords: ... import done.\n")
