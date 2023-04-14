from flask import Flask, request, Response
import requests

from game import FrameXBisector, bisect

import random
import os
 
app = Flask(__name__)

TOKEN = "6149126155:AAF6FUeYlPkZo9Q6dOhRmErkN0xBQtD8UpA"
VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)
global n
n = 20

def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt

def confirm(title, chat_id, text):
    """
    Asks a yes/no question to the user
    """
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': text,
        'caption': ''
    }
    r = requests.post(url,json=payload)

    # url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    # payload = {
    #     'chat_id': chat_id,
    #     'text': "¿se ha lanzado el cohete?"
    # }
    # r = requests.post(url,json=payload)

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "¿se ha lanzado el cohete?",
                'reply_markup': {'keyboard': [[{'text': 'si'}, {'text': 'no'}]]}
    }
    r = requests.post(url,json=payload)
    print(r.json())

    return  f"{title} - did the rocket launch yet?"

def confirm2(title, chat_id, text):

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url,json=payload)

    return  f"{title} - did the rocket launch yet?"
 

def tel_send_message(chat_id, text):
    bisector = FrameXBisector(VIDEO_NAME)
    # culprit = bisect(bisector.count, mapper, tester)
    n = os.getenv('N', '20')
    culprit = int(n)
    bisector.index = culprit
    img_base64 = bisector.blit()
    print(img_base64)
    if text != 'si':
        confirm(title='Image', chat_id=chat_id, text=img_base64)
        n = int(n) + random.randint(1000, 10000)
        if n > 61695:
            confirm2(title='', chat_id=chat_id, text='No se ha encontrado el lanzamiento del cohete')
            n = 20
        os.environ['N'] = str(n)    
    else:
        n = os.getenv('N')
        confirm2(title='muajja', chat_id=chat_id, text='Se ha lanzadao el cohete en el frame ' + str(n))
        n = 20
        os.environ['N'] = str(n)

    return 'img_base64'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        res = tel_send_message(chat_id, txt)
       
        return Response(res, status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')
