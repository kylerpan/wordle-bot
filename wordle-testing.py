from words import possibleWords, possibleAnswers
from colors import colorCombinations
from initialExpectValue import initialExpected
from copy import copy
from math import log2
import time

allTries = []

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

    wordsLeftExpected = []
    for word in possibleWords:
        wordsLeftExpected.append((word, allExpectedValues(word, result)))
    wordsLeftExpected = sorted(wordsLeftExpected, key=lambda x: x[1], reverse=True)

    return wordsLeftExpected, result, result

def runGame(word):
    wordsLeft = possibleWords
    wordInput = initialExpected[0][0]
    print(f'answer: {word} \nguesses: ', end='')
    count = 0

    while True:
        count += 1
        print(f'{wordInput} ', end='')
        
        colorResult = ''
        for i in range(5):
            if wordInput[i] == word[i]:
                colorResult += 'g'
            elif wordInput[i] != word[i] and wordInput[i] in word:
                colorResult += 'y'
            else:
                colorResult += 'b'

        wordsLeftExpected, wordsLeft, result = changeValidWords(wordInput, colorResult, wordsLeft)
        if (len(result) == 1):
            count += 1
            print(f'{result[0]}\ncount: {count}')
            allTries.append(count)
            break

        wordInput = wordsLeftExpected[0][0]

if __name__ == '__main__':
    start = time.time()
    runGame('shard')
    end = time.time()
    print(f'time: {int(end - start)}')