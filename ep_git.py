import git
import os

class EPGit:
  """ Git wrapper class """
  app = None
  repo = None
  origin = None

  def __init__(self, app):
    self.app = app

  def get_repo(self):
    self.repo = git.Repo.init(os.path.join('.', self.app.slug))
    try:
      self.origin = self.repo.create_remote('origin', self.app.repo_url)
    except git.exc.GitCommandError:
      self.origin = self.repo.remote()
    self.origin.fetch()
    return self.repo

  def get_tags(self):
    return self.get_repo().tags

  def get_tag_commit(self, tag):
    return tag.commit

  def find_tag(self, version):
    tags = self.get_tags()
    for tag in tags:
      if tag.name == version:
        return tag
    return None

  def __unicode__():
    return self.name
