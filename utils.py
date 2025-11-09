import random
def getNewWord(wordList):
    index=random.randint(0,len(wordList)-1)
    newWord=wordList[index]
    return newWord
