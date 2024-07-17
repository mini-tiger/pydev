import requests
import json
import base64
def paddleocr(image_path):
    encoded_string = ""
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    apiURL = "http://172.22.220.61:8866/predict/ocr_system"
    headers = {'Content-Type':'application/json'}
    query = {}
    images = []
    images.append(encoded_string)
    query["images"] = images
    result = requests.post(apiURL,data=json.dumps(query),headers=headers)
    data = json.loads(result.text)
    print(data)
    text = ""
    if(len(data["results"][0]) > 0):
        text = data["results"][0][0]["text"]
    return text


text=paddleocr("/mnt/191/20240626-165451.jpg")
print(text)