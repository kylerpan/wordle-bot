from collections import defaultdict
from math import log2
import time

POSSIBLE_WORDS = [f'{line.rstrip()}' for line in open("textFiles/possibleWords.txt", "r")]
COLOR_COMBINATIONS = [list(line.rstrip()) for line in open("textFiles/colorCombinations.txt", "r")]
INITIAL_EXPECTED_VALUE = [tuple(line.rstrip().split(', ')) for line in open("textFiles/initialExpectedValue.txt", "r")]
allTries = []

def newResult(wordInput, colorResult, wordsLeft, allCombination):
    letterCounter = defaultdict(int)
    colorsDict = defaultdict(list)
    colorsCheck = defaultdict(int)

    for i in range(5):
        if colorResult[i] == 'b':
            colorsDict['b'].append((wordInput[i], i))
            colorsCheck[f'b-{wordInput[i]}'] += 1
        elif colorResult[i] == 'y':
            colorsDict['y'].append((wordInput[i], i))
            colorsCheck[f'y-{wordInput[i]}'] += 1
        else:
            colorsDict['g'].append((wordInput[i], i))
            colorsCheck[f'g-{wordInput[i]}'] += 1
    
    if (colorsCheck in allCombination): return []
    else: allCombination.append(colorsCheck)

    for colorList in [colorsDict['g'], colorsDict['y']]:
        for letter, index in colorList:
            letterCounter[letter] += 1

    for letter, index in colorsDict['g']:
        wordsLeft = [word for word in wordsLeft if word[index] == letter]
    
    for letter, index in colorsDict['y']:
        wordsLeft = [word for word in wordsLeft if word[index] != letter]
        wordsLeft = [word for word in wordsLeft if word.count(letter) >= letterCounter[letter]]

    for letter, index in colorsDict['b']:
        wordsLeft = [word for word in wordsLeft if word.count(letter) == letterCounter[letter]]

    return wordsLeft

def allExpectedValues(wordInput, wordsLeft):
    allExpected = []
    wordsLeftLength = len(wordsLeft)
    allCombination = []

    for combination in COLOR_COMBINATIONS:
        result = newResult(wordInput, combination, wordsLeft, allCombination)
        resultLength = len(result)
        probability = resultLength / wordsLeftLength

        if probability == 0: continue
        infoBit = log2(1/probability)
        allExpected.append(probability * infoBit)
        
    return sum(allExpected)

def changeValidWords(wordInput, colorResult, wordsLeft):
    result = newResult(wordInput, colorResult, wordsLeft, [])

    wordsLeftExpected = []
    for word in POSSIBLE_WORDS:
        wordsLeftExpected.append((word, allExpectedValues(word, result)))
    wordsLeftExpected = sorted(wordsLeftExpected, key=lambda x: x[1], reverse=True)

    return wordsLeftExpected, result

def runGame(word):
    wordsLeft = POSSIBLE_WORDS
    wordInput = INITIAL_EXPECTED_VALUE[0][0]
    letterCounter = defaultdict(int)
    count = 0
    
    for i in range(5):
        letterCounter[word[i]] += 1
    
    print(f'answer: {word} \nguesses: ', end='')

    while True:
        count += 1
        print(f'{wordInput} ', end='')
        
        colorResult = ''
        for i in range(5):
            if wordInput[i] == word[i]:
                letterCounter[wordInput[i]] -= 1
                colorResult += 'g'
            elif wordInput[i] != word[i] and letterCounter[wordInput[i]] > 0:
                letterCounter[wordInput[i]] -= 1
                colorResult += 'y'
            elif letterCounter[wordInput[i]] == 0:
                colorResult += 'b'

        wordsLeftExpected, wordsLeft = changeValidWords(wordInput, colorResult, wordsLeft)
        if (len(wordsLeft) == 1):
            count += 1
            print(f'{wordsLeft[0]}\ncount: {count}')
            allTries.append(count)
            break

        wordInput = wordsLeftExpected[0][0]

if __name__ == '__main__':
    start = time.time()
    runGame('shard')
    end = time.time()
    print(f'time: {int(end - start)}s')