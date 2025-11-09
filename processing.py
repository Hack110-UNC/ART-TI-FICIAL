import numpy as np
from PIL import Image
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("OPENAI_KEY")

def imgData2Png(imageArray): #numpy image array
    matrix = np.array(imageArray).astype('uint8') * 255 #scale to RGB
    img = Image.fromarray(matrix, mode='L')
    directory=os.getcwd()
    filename=f"temp.jpg"
    path=os.path.join(directory,filename)
    img.save(path)
    return path

def filePath2AIPayload(filePath):
    with open(filePath, "rb") as image:
        base64BytesRaw=base64.b64encode(
            image.read())
        base64ImgString = base64BytesRaw.decode("utf-8")
    os.remove(filePath)
    return base64ImgString #send to AI

def getResponseFromAI(imagePayload,targetWord):
    try:
        client = OpenAI(api_key=API_KEY)
    except Exception as e:
        quit()
        print('API error, please check key configuration')
    response = client.responses.create(
    model="gpt-4o-mini",
    input=[
    {"role": "user",
     "content":[
        { "type": "input_text", 
         "text": f"What objects or shapes do you see in this image? Give a word or phrase to describe it, being as specific as possible without making up details. Please keep in mind you are not supposed to know what the drawing is at this point. Next, score how close that phrase is to the {targetWord} on a 0–5000 scale, thinking in terms of semantic association. Answer with a positive integer but don't round it. Answer only like this: [phrase, score]"
         },
         { "type": "input_image",
          "image_url": f"data:image/jpeg;base64,{imagePayload}"   
         }]

    }
    ]
    )
    return response


        

