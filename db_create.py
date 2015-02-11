from app import db
from models import User, App, AppServer

db.create_all()

db.session.add(User('Piotr', 'pdlekowski@grupainteger.pl', 'qwerty'))
db.session.add(User('Piotr 2', 'p2dlekowski@grupainteger.pl', 'zaq1xsw2cde3'))

db.session.add(App('Console Administration', 'administration_console', 'Console administration application', 'git@gitlab.easypack24.net:pdelkowski/administration_console.git'))
db.session.add(App('API v4', 'apiv4', 'Ruby API version 4', 'git@gitlab.easypack24.net:pdelkowski/administration_console.git'))


db.session.add(AppServer('TEST PL', 1, 'bundle exec cap test_pl', './symfony cc', 'server-url: test.pl.console.easypack24.net', 'url1|root|qwerty'))
db.session.add(AppServer('STAG PL', 1, 'bundle exec cap stag_pl', './symfony cc', 'server-url: stag.pl.console.easypack24.net', 'url|user|password'))

db.session.commit()

