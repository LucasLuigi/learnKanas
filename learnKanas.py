# -*-coding:Latin-1 -*

import sys
import random
from PIL import Image

KANASNUMBER = 46
kanas = {
    "": ["a", "i", "u", "e", "o"],
    "K": ["ka", "ki", "ku", "ke", "ko"],
    "S": ["sa", "shi", "su", "se", "so"],
    "T": ["ta", "chi", "tsu", "te", "to"],
    "N": ["na", "ni", "nu", "ne", "no"],
    "H": ["ha", "hi", "fu", "he", "ho"],
    "M": ["ma", "mi", "mu", "me", "mo"],
    "Y": ["ya", "yu", "yo"],
    "R": ["ra", "ri", "ru", "re", "ro"],
    "W": ["wa", "wo"],
    "n": ["n"]
}


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
                    image.close()
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


def main():
    global kanasList

    random.seed()

    # for line in kanas:
    #     for kana in kanas[line]:
    #         image = Image.open("hiraganas/{}.png".format(kana))
    #         image.show()
    #         image.close

    kanasList = []
    for line in kanas:
        for kana in kanas[line]:
            kanasList.append(kana)

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


if __name__ == '__main__':
    print('- learnKanas - \n')
    main()
