from flask import Flask, redirect, url_for, request, render_template, flash
from flask_migrate import MigrateCommand
from flask_script import Manager
from models import db,migrate,user_datastore,Helper,User,Role
from flask_security.utils import hash_password,verify_password,login_user,logout_user
from flask_security import Security,current_user,login_required
import requests
import json

def create_app():
  app = Flask(__name__)
  context_set = ""
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/helper'
  app.config['SECRET_KEY']='ROHIT'
  app.config['SECURITY_PASSWORD_SALT']='ROHIT'
  app.config['SECURITY_LOGIN_USER_TEMPLATE']='login.html'
  db.init_app(app)
  migrate.init_app(app,db)
  return app

app=create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

security = Security(app, user_datastore)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
  if (request.method=='POST'):
    fname=request.form['fname']
    lname=request.form['lname']
    mail=request.form['mail']
    uname=request.form['uname']
    pwd=hash_password(request.form['pwd'])
    role=Role.query.get_or_404(1)

    user_datastore.create_user(username=uname,password=pwd,roles=[role])
    db.session.commit()
        
    user = User.query.filter_by(username=uname).first()
    newhelper=Helper(firstname=fname, lastname=lname, email=mail, user=user)
    db.session.add(newhelper)
    db.session.commit()

    login_user(user)
    return redirect('/homepage')
  else:
    return render_template('signup.html')

@app.route('/signin', methods = ['POST', 'GET'])
def login():
  if (request.method=='POST'):
    uname=request.form['uname']
    pwd=request.form['pwd']
    
    user = User.query.filter_by(username = uname).first()
    
    if not user or not verify_password(pwd, user.password):
      flash('Please check your login details and try again.')
      return redirect('/signin')
    else:
      login_user(user)
      return redirect('/homepage')
  else:
    return render_template('login.html')

@app.route('/signout')
def logout():
    logout_user()
    return redirect('/signin')

@app.route('/homepage', methods = ['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
      val = request.form['text']
      data = json.dumps({"sender": current_user.username,"message": val})
      headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
      res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
      res = res.json()
      return redirect('/homepage')
    else:
      res = requests.get('http://localhost:5005/conversations/{}/tracker'.format(current_user.username))
      res=res.json()
      list=[]
      for i in res['events']:
        if (i['event']=='user' or i['event']=='bot'):
          t=i['text']
          t="<br />".join(t.split("\n"))
          list.append({'event':i['event'],'text':t})
      
      return render_template('index.html', list=list)


if __name__ == '__main__':
  manager.run()
  app.run(debug=True)