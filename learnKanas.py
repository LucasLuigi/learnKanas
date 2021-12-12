import sys
from PIL import Image

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


def randomFrToKana():
    print("\n")
    while not select1:
        print("# How many kanas for the game? (1-\n")
        choice = input(">")
        if choice == '1' or choice == '2':
            select1 = True
            randomFrToKana()
        else:
            print("Wrong choice\n")


def main():
    global kanasList

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
        print("# Select mode\n 1- Random FR->JP hiragana\n 2- Random FR->JP katakana\n")
        choice = input(">")
        if choice == '1' or choice == '2':
            select1 = True
            randomFrToKana()
        else:
            print("Wrong choice\n")


if __name__ == '__main__':
    print('- learnKanas - \n')
    main()
