from copy import copy

colorCombinations = []

def permutation(colors, result, index):
    temp = copy(result)
    temp += (colors[index],)
    
    if (len(temp) >= 5):
        colorCombinations.append(temp)
    else:
        permutation(colors, temp, 0)
        permutation(colors, temp, 1)
        permutation(colors, temp, 2)


colors = ('b', 'y', 'g')

for i in range(len(colors)):
    permutation(colors, [], i)

colorCombinations = tuple(colorCombinations)
colorCombinationsLength = len(colorCombinations)

if __name__ == '__main__':
    print(colorCombinations)
    print(colors)
    print(colorCombinationsLength)