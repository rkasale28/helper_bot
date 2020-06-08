from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__)
context_set = ""

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'GET':
        val = str(request.args.get('text'))
        data = json.dumps({"sender": "Rasa","message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
        res = res.json()
        print(res)
        val = res[0]['text']
        return render_template('index.html', val=val)

if __name__ == '__main__':
  app.run(debug=True)