from flask import Flask, request, Response
 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print('hola')
    print(request.method)
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')
