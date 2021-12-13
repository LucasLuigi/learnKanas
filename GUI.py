# -*-coding:Latin-1 -*

from tkinter import *
from tkinter.font import *
from tkinter import Tk, Listbox, Label, Button, Frame, TOP, BOTTOM, LEFT, RIGHT, GROOVE, BROWSE
from tkinter.font import Font, BOLD

from games import Games
import logging


class Gui():
    def __init__(self):
        self.gamesInst = Games()

        self.window = Tk(screenName="learnKanas")
        #self.window['bg'] = 'white'

        windowTitle = LabelFrame(
            self.window, text="", padx=20, pady=5)
        windowTitle.pack(fill="both", expand="yes")
        Label(windowTitle, text="learnKanas",
              font=("Helvetica", 20, BOLD)).pack()

        # list
        self.listItem = Listbox(self.window, width=40,
                                height=5, selectmode=SINGLE)
        self.listItem.insert(1, "Random Romaji->Hiragana")
        self.listItem.insert(2, "Random Romaji->Katakana")
        self.listItem.insert(3, "Exit")
        self.listItem.pack(side=TOP, padx=20, pady=20)

        buttonItem = Button(self.window, text="Valid",
                            command=self.chooseGame)
        buttonItem.pack()

    def chooseGame(self):
        curSelection = self.listItem.curselection()
        self.gamesInst.selectGame(curSelection[0])

    def run(self):
        self.window.mainloop()
