# -*-coding:utf-8 -*

import logging
from os import listdir
from os.path import isfile, join
from pathlib import Path

import kanas

wordsDict = {}


def importWords(wordFileName, wordFileContent):
    # FIXME Manage cases when n french words have the same translation ("bye/à plus/à bientot" or 3 lines in the file)
    global wordsDict

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
                frenchWord = frenchWord.strip(" ")

                if frenchWord in wordsDict:
                    # A list of japanese words already exists at the key of wordsList
                    # Append
                    for japaWord in japaWordsList:
                        wordsDict[frenchWord].append(japaWord)
                else:
                    # Append the list to a new key
                    wordsDict[frenchWord] = japaWordsList

    logging.debug("Words list:")
    for key in wordsDict:
        logging.debug(f"{key}: {wordsDict[key]}")


def initWords():
    WORDS_RELATIVE_PATH = "./wordsLists"

    logging.debug(
        "words.initWords: importing file in wordLists/ to fill the list used by the learnKanas words' exercise...")

    wordsFiles = [f for f in listdir(
        WORDS_RELATIVE_PATH) if isfile(join(WORDS_RELATIVE_PATH, f))]

    for wordFile in wordsFiles:
        logging.debug(
            f"words.initWords: {wordFile} will be imported")
        with open(f"{WORDS_RELATIVE_PATH}/{wordFile}", "r", encoding="utf-8") as wordFileContent:
            importWords(wordFile, wordFileContent)

    logging.debug(
        "words.initWords: ... import done.\n")
