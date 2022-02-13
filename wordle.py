from expectedValues import changeValidWords

POSSIBLE_WORDS = [f'{line.rstrip()}' for line in open("possibleWords.txt", "r")]
INITIAL_EXPECTED_VALUE = [tuple(line.rstrip().split(', ')) for line in open("initialExpectedValue.txt", "r")]

def runGame():
    wordsLeft = POSSIBLE_WORDS
    print('---Welcome to Wordle Bot---\n')
    print('Here are some words with the highest amount of information:')
    for i in range(15):
        print(INITIAL_EXPECTED_VALUE[i][0], INITIAL_EXPECTED_VALUE[i][1] + '0' * (18 - len(str(INITIAL_EXPECTED_VALUE[i][1]))))
    while True:
        word = input('\nPlease input the WORD you chose (e.g. crane): ')
        if (word not in POSSIBLE_WORDS):
            print('Please enter a valid 5 letter WORD\n')
            continue

        colorResult = input('Please input the COLOR RESULTS (e.g. bbygb): ')
        if (len(colorResult) != 5 or all([True if character not in ['b', 'y', 'g'] else False for character in colorResult])):
            print('Please enter a valid 5 COLOR RESULTS\n')
            continue

        wordsLeftExpected, wordsLeft, result = changeValidWords(word, colorResult, wordsLeft)
        print()
        if (len(result) == 1):
            print(f'The word is "{result[0]}"')
            break
        print('\nHere are some words with the highest amount of information after picking {word}:')
        for i in range(15):
            print(wordsLeftExpected[i][0], f'{wordsLeftExpected[i][1]}' + '0' * (18 - len(str(wordsLeftExpected[i][1]))))

if __name__ == '__main__':
    runGame()

