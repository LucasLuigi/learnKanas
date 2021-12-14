# -*-coding:Latin-1 -*

import sys
import threading
import logging

from GUI import Gui
from games import Games
from kanas import kanas, KANASNUMBER, kanasList


def main():
    global kanasList

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] %(message)s')

    logging.info('- learnKanas - \n')

    for line in kanas:
        for kana in kanas[line]:
            kanasList.append(kana)

    guiInst = Gui()

    # Tkinter only works in the main Thread
    guiInst.run()


if __name__ == '__main__':
    main()
