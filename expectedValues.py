from words import possibleWords, possibleWordsLength
from colors import colorCombinations
from copy import copy
from math import log2

def allExpectedValues(wordInput):
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
    
    print(wordInput, sum(allExpected))
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

    wordsLeftExpected = sorted([(word, allExpectedValues(word, result)) for word in possibleWords], key=lambda x: x[1], reverse=True)
    print(result)
    print(len(result))
    return wordsLeftExpected, result


if __name__ == '__main__':
    allWordsExpected = sorted([(word, allExpectedValues(word)) for word in possibleWords], key=lambda x: x[1], reverse=True)
    f = open("allWordsExpected.txt", "w")
    f.write('(')
    for word in allWordsExpected:
        f.write(f'{word}, ')
    f.write(')')
    f.close()