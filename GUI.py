# -*-coding:Latin-1 -*

from tkinter import Tk, Label


class GUI():
    def __init__(self):
        self.window = Tk(screenName="learnKanas")
        label = Label(self.window, text="Yoooooooooooooooooooooooo")
        label.pack()
        self.window.mainloop()
