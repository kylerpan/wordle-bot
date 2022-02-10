from copy import copy

colors = ['b', 'y', 'g']
colorCombinations = []

def permutation(colors, result, index):
    temp = copy(result)
    temp.append(colors[index])
    
    if (len(temp) >= 5):
        colorCombinations.append(temp)
    else:
        permutation(colors, temp, 0)
        permutation(colors, temp, 1)
        permutation(colors, temp, 2)

for i in range(len(colors)):
    permutation(colors, [], i)

colorCombinationsLength = len(colorCombinations)