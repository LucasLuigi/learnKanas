# -*-coding:utf-8 -*

import logging
from os import listdir
from os.path import isfile, join
from pathlib import Path

import kanas

wordsList = []


def importWords(wordFileName, wordFileContent):
    global wordsList

    for line in wordFileContent:
        splittedLine = line.strip(" ").split(" ")
        if len(splittedLine) < 2:
            logging.warning(
                f"WARNING: the words '{line}' from {wordFileName} will not be imported\nReason: it is not correctly formatted: 'frenchWord japaneseWord'")
        else:
            continueToParseLine = True
            japaWord = splittedLine[-1].strip("\n")
            for kana in kanas.rootKanasHira[kanas.KANAS_SUBSETS.index("Kanas")]:
                if kana in splittedLine[-2]:
                    continueToParseLine = False
                    logging.warning(
                        f"WARNING: the words '{line}' from {wordFileName} will not be imported\nReason: it is not correctly formatted: the japanese word is splitted by a space")

            if continueToParseLine:
                # Regroup French words (everyone but the last)
                frenchWord = ""
                for splittedWord in splittedLine[:-1]:
                    frenchWord = frenchWord + splittedWord + " "
                frenchWord = frenchWord.strip(" ")

                pairToAppend = [frenchWord, japaWord]
                wordsList.append(pairToAppend)

    logging.debug("Words list:")
    for pair in wordsList:
        logging.debug(f"{pair}")


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
