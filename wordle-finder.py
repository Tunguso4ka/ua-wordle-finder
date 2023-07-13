#!/bin/python3

#IMPORTS
from os.path import exists
from os import getenv

#VARIABLES
settings = {
        'program_home_path':f'{getenv("HOME")}/.config/wordle-finder/',
        'dictionary_file_name':'words-UA',
        'suggestion_count':5,
        'help':'wordle-finder:\nexit, вийти - вихід з програми;\nturn, t, хід, х - ввести слово'
        }
words    = []
turns    = []

#CODE
def load_words(path=''):
    global words
    words = []
    if exists(path):
        print('Використовуємо файл з заданого шляху.')
    elif exists(settings['dictionary_file_name']):
        print('Використовуємо файл з текущей теки.')
        path = settings['dictionary_file_name']
    elif exists(settings['program_home_path'] + settings['dictionary_file_name']):
        print('Використовуємо файл з налаштунок')
        path = settings['program_home_path'] + settings['dictionary_file_name']
    else:
        print('Жодних файлів зі словами не існує.')
        quit()

    file = open(path)
    text = file.readlines()
    file.close()

    for i in text: words.append(i.strip().upper())
    print(f'Завантажено {len(words)} слів.')

def turn(word, model):
    global turns
    #тимчасовий костиль
    r = []
    num = 0
    while num < len(word):
        if word.count(word[num]) > 1: r.append([word[num], model[num], num])
        num += 1
    for i in r:
        for t in r:
            if t[0] == i[0] and i[1] not in 'сb' and t[1] in 'сb': model = model[:t[2]] + 'ж' + model[(t[2]+1):]
    turns.append([word, model])

def search():
    suggests = []

    for i in words:
        add = True
        try:
            for t in turns:
                num = 0
                while num < len(i):
                    if t[1][num] in 'сb' and t[0][num] in i: add = False
                    if t[1][num] in 'жy' and t[0][num] not in i: add = False
                    if t[1][num] in 'жу' and t[0][num] == i[num]: add = False
                    if t[1][num] in 'зg' and t[0][num] != i[num]: add = False
                    num += 1
        except: add = False
        if add: suggests.append(i)
    
    print(f'Знайдено {len(suggests)} слів.')
    line = ''
    num = 0
    while num < len(suggests):
        if str((num+1) / settings['suggestion_count'])[-1] == '0': line += suggests[num] + '\n'
        else: line += suggests[num] + ' '
        num += 1
    if line != '': print(line)

def main():
    global turns
    load_words()
    while True:
        res = input('> ')
        if res == '': continue
        res = res.split(' ')
        if   res[0] in ['exit', 'вийти']: quit()
        elif res[0] in ['help', 'допомога']: print(settings['help'])
        elif res[0] in ['хід', 'turn', 'х', 't']: turn(res[1].upper(), res[2])
        elif res[0] in ['знайти', 'search', 'з', 's']: search()
        elif res[0] in ['перезавантажити', 'reload', 'п', 'r']: load_words()
        elif res[0] in ['обнулити', 'null', 'о', 'n']: turns = []
        else: print(res)

if __name__ == "__main__": main()
