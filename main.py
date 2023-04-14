from flask import Flask, request, Response
import requests

from game import FrameXBisector, bisect

import os
 
app = Flask(__name__)

TOKEN = "6149126155:AAF6FUeYlPkZo9Q6dOhRmErkN0xBQtD8UpA"
VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)


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
        'caption': title
    }
    # payload = {
    #             'chat_id': chat_id,
    #             'text': f"{title} - did the rocket launch yet?"
    #             }
   
    r = requests.post(url,json=payload)
    print(r.json())

    return  f"{title} - did the rocket launch yet?"
 
def tel_send_message(chat_id, text):
    print('acaaa')
    bisector = FrameXBisector(VIDEO_NAME)
    def mapper(n):
        """
        In that case there is no need to map (or rather, the mapping
        is done visually by the user)
        """

        return n

    def tester(n):
        """
        Displays the current candidate to the user and asks them to
        check if they see wildfire damages.
        """

        bisector.index = n
        # disp.fill(BLACK)
        bisector.blit()
        # pygame.display.update()

        # return confirm(bisector.index, chat_id, text)
    
    # culprit = bisect(bisector.count, mapper, tester)
    culprit = 20
    bisector.index = culprit
    img_base64 = bisector.blit()
    confirm(title='Image', chat_id=chat_id, text=img_base64)
    print('culprit', culprit)
    # url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    # payload = {
    #             'chat_id': chat_id,
    #             'text': text
    #             }
   
    # r = requests.post(url,json=payload)
    return 'img_base64'

def tel_send_image(chat_id):
    bisector = FrameXBisector(VIDEO_NAME)
    print(bisector)
    # url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    # payload = {
    #     'chat_id': chat_id,
    #     'photo': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-NkWPQU3-6dvelLDoZZ47CR_0iOnZvmI_WrCH1FrkBw&s",
    #     'caption': "This is a sample image"
    # }
 
    # r = requests.post(url, json=payload)
    return 'r'
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        res = 'ok'
        if txt == "hi":
            res = tel_send_message(chat_id,"Hello!!")
        elif txt == "image":
            tel_send_image(chat_id)
        else:
            tel_send_message(chat_id,'from webhook')
       
        return Response(res, status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')
