from words import possibleWords
from colors import colors
from initialExpectValue import initialExpected
from expectedValues import changeValidWords

if __name__ == '__main__':
    wordsLeft = possibleWords
    print('---Welcome to Wordle Bot---\n')
    print('Here are some words with the highest amount of information:')
    for i in range(15):
        print(initialExpected[i][0], initialExpected[i][1])
    while True:
        word = input('\nPlease input the WORD you chose (e.g. crane): ')
        if (word not in possibleWords):
            print('Please enter a valid 5 letter WORD\n')
            continue

        colorResult = input('Please input the COLOR RESULTS (e.g. bbygb): ')
        if (len(colorResult) != 5 or all([True if character not in colors else False for character in colorResult])):
            print('Please enter a valid 5 COLOR RESULTS\n')
            continue

        wordsLeftExpected, wordsLeft, result = changeValidWords(word, colorResult, wordsLeft)
        print()
        if (len(result) == 1):
            print(f'The word is "{result[0]}"')
            break
        print('\nHere are some words with the highest amount of information after picking {word}:')
        for i in range(15):
            print(wordsLeftExpected[i][0], wordsLeftExpected[i][1])
        print("...")

