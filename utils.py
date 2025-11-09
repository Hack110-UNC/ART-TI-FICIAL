import random
def getNewWord(wordListOfLists,round):
    level=round-1
    match level:
        case 0:
            difficulty="easy"
        case 1:
            difficulty="medium"
        case 2:
            difficulty="hard"    
    wordList=wordListOfLists[level]
    index=random.randint(0,len(wordList)-1)
    newWord=wordList[index]
    return newWord, difficulty
