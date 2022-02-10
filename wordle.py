from words import possibleWords, possibleWordsLength
from colors import colors, colorCombinations, colorCombinationsLength
from copy import copy
from math import log2

def wordProbability(var):
    allExpected = []
    timeSpent = 0

    for combination in colorCombinations:
        result = copy(possibleWords)

        for i in range(5):
            if combination[i] == 'b':
                result = [word for word in result if var[i] not in word]
            elif combination[i] == 'y':
                result = [word for word in result if var[i] in word]
            elif combination[i] == 'g':
                result = [word for word in result if word[i] == var[i]]

        resultLength = len(result)
        probability = resultLength / possibleWordsLength
        infoBit = log2(1/probability) if probability != 0 else 0
        allExpected.append(probability * infoBit)
    
    return sum(allExpected)


if __name__ == '__main__':
    
    # print(possibleWords)
    # print()
    # print(possibleWordsLength)
    # print()
    # print(colors)
    # print()
    # print(colorCombinations)
    # print()
    # print(colorCombinationsLength)
    # print()
    for word in possibleWords:
        print(word, wordProbability(word))
