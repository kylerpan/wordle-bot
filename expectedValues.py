from words import possibleWords, possibleWordsLength
from colors import colorCombinations
from copy import copy
from math import log2

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

def initialExpectedValues(wordInput):
    allExpected = []

    for combination in colorCombinations:
        result = copy(possibleWords)

        for i in range(5):
            if combination[i] == 'b':
                result = [word for word in result if wordInput[i] not in word]
            elif combination[i] == 'y':
                result = [word for word in result if wordInput[i] in word and word[i] != wordInput[i]]
            else:
                result = [word for word in result if word[i] == wordInput[i]]

        resultLength = len(result)
        probability = resultLength / possibleWordsLength
        infoBit = log2(1/probability) if probability != 0 else 0
        allExpected.append(probability * infoBit)
    
    print(wordInput, sum(allExpected))
    return sum(allExpected)

def allExpectedValues(wordInput, wordsLeft):
    allExpected = []

    for combination in colorCombinations:
        result = copy(wordsLeft)

        for i in range(5):
            if combination[i] == 'b':
                result = [word for word in result if wordInput[i] not in word]
            elif combination[i] == 'y':
                result = [word for word in result if wordInput[i] in word and word[i] != wordInput[i]]
            else:
                result = [word for word in result if word[i] == wordInput[i]]

        resultLength = len(result)
        probability = resultLength / len(wordsLeft)
        if probability == 0: continue
        infoBit = log2(1/probability) if probability != 0 else 0
        allExpected.append(probability * infoBit)
    
    # print(wordInput, sum(allExpected))
    return sum(allExpected)

def changeValidWords(wordInput, colorResult, wordsLeft):
    result = copy(wordsLeft)
    for i in range(5):
        if colorResult[i] == 'b':
            result = [word for word in result if wordInput[i] not in word]
        elif colorResult[i] == 'y':
            result = [word for word in result if wordInput[i] in word and word[i] != wordInput[i]]
        else:
            result = [word for word in result if word[i] == wordInput[i]]

    # wordsLeftExpected = sorted([(word, allExpectedValues(word, result)) for word in possibleWords], key=lambda x: x[1], reverse=True)
    wordsLeftExpected = []
    for word in progressBar(possibleWords, prefix='Progress', suffix='Complete', length=50):
        wordsLeftExpected.append((word, allExpectedValues(word, result)))
    wordsLeftExpected = sorted(wordsLeftExpected, key=lambda x: x[1], reverse=True)
    
    print(f'\n{len(result)} Words Left: ')
    for i in range(len(result)):
        print(result[i], end=" ")
        if i % 15 == 0 and i != 0: print()
    return wordsLeftExpected, result, result


if __name__ == '__main__':
    allWordsExpected = sorted([(word, initialExpectedValues(word)) for word in possibleWords], key=lambda x: x[1], reverse=True)
    f = open("allWordsExpected.txt", "w")
    f.write('(')
    for word in allWordsExpected:
        f.write(f'{word}, ')
    f.write(')')
    f.close()