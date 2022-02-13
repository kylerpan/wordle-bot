from collections import defaultdict
from copy import copy
from math import log2

POSSIBLE_WORDS = [f'{line.rstrip()}' for line in open("possibleWords.txt", "r")]
COLOR_COMBINATIONS = [list(line.rstrip()) for line in open("colorCombinations.txt", "r")]

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

def newResult(wordInput, colorResult, wordsLeft, allCombination):
    result = copy(wordsLeft)
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
        result = [word for word in result if word[index] == letter]
    
    for letter, index in colorsDict['y']:
        result = [word for word in result if word[index] != letter]
        result = [word for word in result if word.count(letter) >= letterCounter[letter]]

    for letter, index in colorsDict['b']:
        result = [word for word in result if word.count(letter) == letterCounter[letter]]

    return result

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
    for word in progressBar(POSSIBLE_WORDS, prefix='Progress', suffix='Complete', length=50):
        wordsLeftExpected.append((word, allExpectedValues(word, result)))
    wordsLeftExpected = sorted(wordsLeftExpected, key=lambda x: x[1], reverse=True)
    
    print(f'\n{len(result)} Words Left: ')
    for i in range(len(result)):
        print(result[i], end=" ")
        if (i + 1) % 15 == 0: print()
    return wordsLeftExpected, result, result


if __name__ == '__main__':
    allWordsExpected = sorted([(word, allExpectedValues(word, POSSIBLE_WORDS)) for word in POSSIBLE_WORDS], key=lambda x: x[1], reverse=True)
    f = open("allWordsExpected.txt", "w")
    f.write('(')
    for word in allWordsExpected:
        f.write(f'{word}, ')
    f.write(')')
    f.close()