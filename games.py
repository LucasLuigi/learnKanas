# -*-coding:Latin-1 -*

import random
from PIL import Image
from kanas import KANASNUMBER, kanasList


def randomRomajiToKana():
    global KANASNUMBER
    global kanasList

    select1 = False
    score = 0
    while not select1:
        print("# How many kanas for the game? (1-{})\n".format(KANASNUMBER))
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
                    point = input("Press 1 if it is correct, 0 otherwise: ")
                    if point == '1':
                        score += 1

                # Score
                print("\n Score: {}/{}, {}%".format(score, choice,
                                                    100.0*score/choice))

            else:
                raise ValueError()
        except ValueError as err:
            print("Wrong choice (must be 1-{})\n".format(KANASNUMBER))


def menu():
    random.seed()

    select1 = False
    while not select1:
        print(
            "# Select mode\n 1- Random Romaji->Hiragana\n 2- Random Romaji->Katakana\n")
        choice = input("> ")
        if choice == '1' or choice == '2':
            select1 = True
            randomRomajiToKana()
        else:
            print("Wrong choice\n")
