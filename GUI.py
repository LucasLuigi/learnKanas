# -*-coding:Latin-1 -*

from tkinter import *
from tkinter.font import *
from tkinter import Tk, Listbox, Label, Button, Frame, StringVar, TOP, BOTTOM, LEFT, RIGHT, GROOVE, BROWSE
from tkinter.font import Font, BOLD, ROMAN

import logging
import sys
import time
import random
from PIL import Image


from kanas import KANASNUMBER, kanasList


class Gui():
    # Init
    def __init__(self):
        self.consoleBuffer = str("")
        random.seed()

        self.window = Tk(screenName="learnKanas")
        #self.window['bg'] = 'white'

        # title
        windowTitle = LabelFrame(
            self.window, text="", padx=20, pady=5)
        windowTitle.pack(fill="both", expand="yes", side=TOP)
        Label(windowTitle, text="learnKanas",
              font=("Helvetica", 20, BOLD)).pack()

        # select game
        self.listItem = Listbox(self.window, width=40,
                                height=5, selectmode=SINGLE)
        self.listItem.insert(1, "Random Romaji->Hiragana")
        self.listItem.insert(2, "Random Romaji->Katakana")
        self.listItem.insert(3, "Exit")
        self.listItem.pack(side=TOP, padx=10, pady=5)

        # button to valid game
        buttonItem = Button(self.window, text="Valid",
                            command=self.chooseGame)
        buttonItem.pack(pady=10)

        # console
        self.consoleText = StringVar(value="papa")

        windowTitle = LabelFrame(
            self.window, text="Game", padx=20, pady=5)
        windowTitle.pack(fill="both", expand="yes", side=BOTTOM, pady=10)
        Label(windowTitle, textvariable=self.consoleText,
              font=("Helvetica", 10, NORMAL)).pack(side=LEFT)

    # Print and log
    def logAndFillConsoleBuffer(self, text):
        print(type(text))
        logging.info(str(text))
        self.consoleBuffer += str(text)

    def printConsoleText(self):
        self.consoleText.set(self.consoleBuffer)
        self.consoleBuffer = ""

    # Games
    # FIXME Move them from the class. The issue is I do not how to access to self.consoleText
    def gameRandomRomajiToKana(self):
        global KANASNUMBER
        global kanasList

        score = 0

        self.logAndFillConsoleBuffer(
            "# How many kanas for the game? (1-{})\n".format(KANASNUMBER))
        try:
            # TMP
            # choice = int(input("> "))
            choice = 3
            if choice >= 1 and choice <= KANASNUMBER:

                randKanasList = random.sample(kanasList, choice)
                for game in range(0, choice):
                    kana = randKanasList[game]
                    # TMP
                    # input("#{}\n Draw {}".format(game+1, kana))
                    self.logAndFillConsoleBuffer("test\n")
                    self.logAndFillConsoleBuffer(
                        "#{}\n Draw {}".format(game+1, kana))
                    image = Image.open("hiraganas/{}.png".format(kana))
                    image.show()
                    image.close()
                    # TMP
                    #point = input("Press 1 if it is correct, 0 otherwise: ")
                    self.logAndFillConsoleBuffer(
                        "Press 1 if it is correct, 0 otherwise: ")
                    point = '1'
                    if point == '1':
                        score += 1

                    # Print
                    self.printConsoleText()
                    time.sleep(1)

                # Score
                self.logAndFillConsoleBuffer("\n Score: {}/{}, {}%".format(score, choice,
                                                                           100.0*score/choice))
                # Print
                self.printConsoleText()

            else:
                raise ValueError()
        except ValueError as err:
            logging.error(
                "Wrong choice (must be 1-{})\n".format(KANASNUMBER))

    def chooseGame(self):
        curSelectionGui = self.listItem.curselection()
        if len(curSelectionGui) > 0:
            selection = curSelectionGui[0]
            logging.debug("Game selection: {}".format(selection))
            # logging.info(
            #    "# Select mode\n 1- Random Romaji->Hiragana\n 2- Random Romaji->Katakana\n 0- Exit\n")
            if selection == 2:
                sys.exit(0)
            elif selection == 0 or selection == 1:
                self.gameRandomRomajiToKana()
            else:
                logging.error("Wrong choice")

    # Main loop
    def run(self):
        self.window.mainloop()
