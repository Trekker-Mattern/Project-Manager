import heapq
from math import sqrt

keyboardLocations = {
        'q': (2, 0), 'w': (2, 1), 'e': (2, 2), 'r': (2, 3), 't': (2, 4),
        'y': (2, 5), 'u': (2, 6), 'i': (2, 7), 'o': (2, 8), 'p': (2, 9),
        'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4),
        'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8), ';': (1, 9),
        'z': (0, 0), 'x': (0, 1), 'c': (0, 2), 'v': (0, 3), 'b': (0, 4),
        'n': (0, 5), 'm': (0, 6), ',': (0, 7), '.': (0, 8), '/': (0, 9),
        }


def assessCloseness(vals: list[str], uInput: str) -> tuple[float,str]:

    """ 
    Input: list of Values, String To BeMatched
    Return: tuple[score | closest word in the list to the inputString] 
    """

    priorityQueue: list[tuple[float, str]] = []
    for val in vals:
        heapq.heappush(priorityQueue, (assessWordCloseness(val.lower(), uInput.lower()), val.lower()))

    return heapq.heappop(priorityQueue)


def assessWordCloseness(word1: str, word2: str) -> float:
    score: float = 0
    index: int = 0
    distanceScore: float = 0

    # score += abs(len(word1) - len(word2))*2
    # score += len(converseOfSetIntersection(createLetterSet(word1), createLetterSet(word2)))*3

    for letter in word1:
        letter = letter.lower()
        if index >= len(word2):
            score += min(len(converseOfSetIntersection(createLetterSet(word1), createLetterSet(word2)))*5, distanceScore)
            print(f"Escaping Early at index: {index} Word: {word1}, Score: {score}")
            return score

        try:
            keyboardLocations[letter]
            keyboardLocations[word2[index]]
        except KeyError:
            print(letter, word2[index])
            index+=1
            continue

        if index == 0 and letter == word2[0]:
            score -= 10

        distanceScore += distance(keyboardLocations[letter], keyboardLocations[word2[index]])
        index += 1

    score += min(len(converseOfSetIntersection(createLetterSet(word1), createLetterSet(word2)))*5, distanceScore)
    print(f"Word: {word1}, Score: {score}")
    return score


def distance(location1: tuple[int, int], location2: tuple[int, int]):
    return sqrt((location1[0]-location2[0])**2 + (location1[1]-location2[1])**2)


def createLetterSet(word: str):
    s = [letter for letter in word]
    return set(s)


def converseOfSetIntersection(setOne: set[str], setTwo: set[str]):
    return setOne.difference(setTwo)
