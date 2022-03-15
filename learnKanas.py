# -*-coding:utf-8 -*

import logging
import sys
import random

import config

import kanas
import words

import kanasExercises
import wordsExercises


def main():
    logger = logging.getLogger()
    logger.setLevel(config.DEBUG_LEVEL)

    random.seed()

    kanas.initFlattenedKanas()
    words.initWords()

    selected1 = False
    while not selected1:
        print(
            "# Select category\n 1- Kanas exercises (characters)\n 2- Words exercises\n 0- Exit\n")
        choice1 = input("> ")
        selected1 = True

        if choice1 == '1':
            selected1 = kanasExercises.selectKanasExercise()
        elif choice1 == '2':
            selected1 = wordsExercises.selectWordsExercise()
        elif choice1 == '0':
            sys.exit(0)
        else:
            selected1 = False
            print("Wrong choice\n")


if __name__ == '__main__':
    print('- learnKanas - \n\nようこそ！\n\nIf the sentence above is only blank squares instead of Japanese Hiragana, something is wrong with your terminal.\nOn Windows run chcp 936 (or chcp 932) before launching learnKanas again\n')
    main()
    print('Thank you for playing!\nGame made by LucasLuigi - https://github.com/LucasLuigi/learnKanas')
