import numpy as np
from PIL import Image
import base64
from openai import OpenAI
def imgData2Png(imageArray): #image array of type [[0,0,1],[1,0,0],[1,0,1]] etc.
    matrix = np.array(imageArray) * 255 #convert to np
    #and scale to RGB coloring
    img = Image.fromarray(matrix, mode='L')
    return img

def filePath2AIPayload(filePath):
    with open(filePath, "rb") as image:
        base64BytesRaw=base64.b64encode(
            image.read())
        base64ImgString = base64BytesRaw.decode("utf-8")
        return base64ImgString #send to AI

def getResposeFromAI(imagePayload,targetWord):
    #PLESAE DO NOT LEAVE THE API KEY HERE
    try:
        client = OpenAI(api_key=['PLACEHOLDER'])
    except Exception as e:
        quit()
        print('API error, please check key configuration')
    response = client.responses.create(
    model="gpt-4o-mini",
    input=[
    {"role": "user",
     "content":[
        { "type": "input_text", 
         "text": f"In four words max, what objects or shapes do you see in this image? Then score how related it is to the word {targetWord} on a 0–5000 scale. Answer only like this: [phrase, score]"
         },
         { "type": "input_image",
          "image_url": f"data:image/jpeg;base64,{imagePayload}"   
         }]

    }
    ]
    )
    return response


        

