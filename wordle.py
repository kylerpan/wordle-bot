from words import possibleWords
from initialExpectValue import initialExpected
from expectedValues import changeValidWords

if __name__ == '__main__':
    wordsLeft = possibleWords
    print('---Welcome to Wordle Bot---\n')
    print('Here are some words with the highest amount of information:')
    for i in range(15):
        print(initialExpected[i][0], initialExpected[i][1])
    while True:
        print(wordsLeft)
        word = input('Please input the first word you chose (e.g. crane): ')
        result = input('Please input the color results (e.g. bbygb): ')
        if (word == 'quit' or result == 'quit'): break
        print()
        wordsLeftExpected, wordsLeft = changeValidWords(word, result, wordsLeft)
        print()
        print('Here are some words with the highest amount of information after picking {word}:')
        for i in range(15):
            print(wordsLeftExpected[i][0], wordsLeftExpected[i][1])

