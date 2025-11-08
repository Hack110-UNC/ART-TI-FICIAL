import json
from openai import OpenAI
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