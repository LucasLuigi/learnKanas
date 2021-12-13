# -*-coding:Latin-1 -*

import logging
import sys
import random
from PIL import Image
from kanas import KANASNUMBER, kanasList


class Games():
    def __init__(self):
        random.seed()

    def randomRomajiToKana(self):
        global KANASNUMBER
        global kanasList

        select1 = False
        score = 0
        while not select1:
            logging.info(
                "# How many kanas for the game? (1-{})\n".format(KANASNUMBER))
            try:
                choice = int(input("> "))
                if choice >= 1 and choice <= KANASNUMBER:
                    select1 = True

                    randKanasList = random.sample(kanasList, choice)
                    for game in range(0, choice):
                        kana = randKanasList[game]
                        input("#{}\n Draw {}".format(game+1, kana))
                        image = Image.open("hiraganas/{}.png".format(kana))
                        image.show()
                        image.close
                        point = input(
                            "Press 1 if it is correct, 0 otherwise: ")
                        if point == '1':
                            score += 1

                    # Score
                    logging.info("\n Score: {}/{}, {}%".format(score, choice,
                                                               100.0*score/choice))

                else:
                    raise ValueError()
            except ValueError as err:
                logging.error(
                    "Wrong choice (must be 1-{})\n".format(KANASNUMBER))

    # TODO Menu to implement in GUI
    def selectGame(self, selection):
        logging.debug("Game selection: {}".format(selection))
        # logging.info(
        #    "# Select mode\n 1- Random Romaji->Hiragana\n 2- Random Romaji->Katakana\n 0- Exit\n")
        if selection == '3':
            sys.exit(0)
        elif selection == '1' or selection == '2':
            self.randomRomajiToKana()
        else:
            logging.error("Wrong choice\n")
