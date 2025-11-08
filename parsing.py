import json
from openai import OpenAI
import csv
def getRawOutputText(response):
    text = response.output_text
    return text
def parseRawText(string): #must be of form "[OBJECT,SCORE]"
    #implement checker that makes sure the form is right
    string = string.removeprefix("[")
    string = string.removesuffix("]")
    values = string.partition(",")
    score = int(values[2])
    objectAI = values[0]
    return objectAI, score
def csvNounsToList(filePath):
    list=[]
    with open(filePath,"r", newline="") as csvFile:
        reader=csv.reader(csvFile)
        for row in reader:
            list.append(row)
    return list[0]
