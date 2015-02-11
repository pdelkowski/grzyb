from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from ep_git import EPGit
import git
import os
import string
import spur

app = Flask(__name__)

app.secret_key = 'adsjlkj2(*(3kjsdfj))'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/python_apps/grzyb/src/grzyb.db'

db = SQLAlchemy(app)

from models import *

# decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect(url_for('login'))
  return wrap

# routing
@app.route("/login", methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if User.query.filter(User.name == request.form['username']).first() is not None:
      user = User.query.filter(User.name == request.form['username']).first()
      if user.password == request.form['password']:
        session['logged_in'] = True
        session['user_id'] = user.id
        return redirect(url_for('home'))
      else:
        error = 'Invalid credentials.'
    else:
        error = 'Invalid credentials.'

  return render_template('login.html', error=error)

@app.route("/logout")
def logout():
  session.pop('logged_in', None)
  session.pop('user', None)
  return redirect(url_for('home'))

@app.route("/")
@login_required
def home():
  deploys = Deployment.query.all()
  return render_template('home.html', deploys=deploys) 

@app.route("/deploy")
@login_required
def deploy_select_app():
  apps = AppServer.query.all()
  return render_template('deploy_select_app.html', apps=apps)

@app.route("/deploy_app/<app_server_id>", methods=['GET'])
@login_required
def deploy_select_version(app_server_id):
  app = AppServer.query.filter(AppServer.id == app_server_id).first()
  repo = EPGit(app.get_app())
  tags = repo.get_tags()
  return render_template('deploy_select_version.html', app_server=app, tags=tags)

@app.route("/deploy_details/<app_server_id>/<version>", methods=['GET'])
@login_required
def deploy_details(app_server_id, version):
  app = AppServer.query.filter(AppServer.id == app_server_id).first()
  repo = EPGit(app.get_app())
  tagref = repo.find_tag(version)
  return render_template('deploy_select_detail.html', app=app, version=tagref)

@app.route("/deploy_final/<app_server_id>/<version>", methods=['GET'])
@login_required
def deploy_final(app_server_id, version):
  app = AppServer.query.filter(AppServer.id == app_server_id).first()
  repo = EPGit(app.get_app())
  tagref = repo.find_tag(version)
  server = app.server_credentials
  server = server.split('|')

  # ssh credentails
  ssh_host = server[0]
  ssh_user = server[1]
  ssh_pass = server[2]

  # commands
  command = app.deploy_command.split('|')
  command_1 = command[0]
  command_2 = command[1]

  # run ssh common
  shell = spur.SshShell(hostname=ssh_host, username=ssh_user, password=ssh_pass, missing_host_key=spur.ssh.MissingHostKey.accept)
  result = shell.run([command_1, command_2])
  print result.output # prints hello

  # save deployment information
  deployment = Deployment(app.id, session['user_id'], tagref.name, str(tagref.commit), server[0])
  db.session.add(deployment)
  db.session.commit()

  flash('Application has been deployed successfully')

  return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
  user_id = session.get('user_id')
  user = User.query.filter(User.id == user_id).first()
  return render_template('profile.html', user=user)

@app.route("/version")
@login_required
def version():
  myapp = App.query.filter(App.id == 1).first()
  repo = EPGit(myapp)
  tags = repo.get_tags()

  return render_template('version.html', tags=tags)

if __name__ == "__main__":
      app.run(debug=True)
