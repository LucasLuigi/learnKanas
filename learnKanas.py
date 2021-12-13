# -*-coding:Latin-1 -*

from GUI import GUI
from games import menu
from kanas import kanas, KANASNUMBER, kanasList


def main():
    global kanasList

    for line in kanas:
        for kana in kanas[line]:
            kanasList.append(kana)

    gui = GUI()

    menu()


if __name__ == '__main__':
    print('- learnKanas - \n')
    main()
