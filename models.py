from app import db
import datetime

class User(db.Model):

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String)
  # posts = relationship("BlogPost", backref="author")

  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<name - {}>'.format(self.name)

class App(db.Model):

  __tablename__ = "apps"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  slug = db.Column(db.String, nullable=False)
  description = db.Column(db.String, nullable=True)
  repo_url = db.Column(db.String, nullable=False)
  # posts = relationship("BlogPost", backref="author")

  def __init__(self, name, slug, description, repo_url):
    self.name = name
    self.slug = slug
    self.description = description
    self.repo_url = repo_url

  def is_active(self):
    return True

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<name - {}>'.format(self.name)

class AppServer(db.Model):

  __tablename__ = "app_servers"

  id = db.Column(db.Integer, primary_key=True)
  app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
  name = db.Column(db.String, nullable=False)
  deploy_command = db.Column(db.String, nullable=True)
  post_deploy_command = db.Column(db.String, nullable=False)
  deploy_configuration = db.Column(db.String, nullable=False)
  server_credentials = db.Column(db.String, nullable=False)

  def __init__(self, name, app_id, deploy_command, post_deploy_command, deploy_configuration, server_credentials):
    self.name = name
    self.app_id = app_id
    self.deploy_command = deploy_command
    self.post_deploy_command = post_deploy_command
    self.deploy_configuration = deploy_configuration
    self.server_credentials = server_credentials

  def get_app(self):
    app = App.query.filter(App.id == self.app_id).first()
    return app

  def is_active(self):
    return True

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<name - {}>'.format(self.name)


class Deployment(db.Model):

  __tablename__ = 'deployments'

  def _get_date(self):
    return datetime.datetime.now()

  id = db.Column(db.Integer, primary_key=True)
  app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  version = db.Column(db.String, nullable=False)
  commit = db.Column(db.String, nullable=False)
  server = db.Column(db.String, nullable=False)
  created_at = db.Column(db.Date, default=_get_date)

  def __init__(self, app_id, user_id, version, commit, server):
    self.app_id = app_id
    self.user_id = user_id
    self.version = version
    self.commit = commit
    self.server = server

  def get_user(self):
    user = User.query.filter(User.id == self.user_id).first()
    return user

  def get_app(self):
    app = AppServer.query.filter(AppServer.id == self.app_id).first()
    return app

  def is_active(self):
    return True

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<name - {}>'.format(self.app)

