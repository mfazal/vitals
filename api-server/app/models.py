from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    devices = db.relationship('Device', backref='user', lazy='dynamic')
    vitals = db.relationship('Vital', backref='user', lazy='dynamic')
    sos = db.relationship('SOS', backref='user', lazy='dynamic')   
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
 
    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Device(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(25), index=True, unique=True)
  type = db.Column(db.String(25))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  def __repr__(self):
        return '<Device %r>'% (self.name)

class Vital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tempinternal = db.Column(db.Float(precision=4), default=0)
    tempexternal = db.Column(db.Float(precision=4), default=0)
    heartrate = db.Column(db.Float(precision=4), default=0)
    bloodoxy = db.Column(db.Float(precision=4), default=0)
    baro = db.Column(db.Float(precision=4), default=0)
    
    def __repr__(self):
        return '<Vital %r>' % (self.user_id)


class SOS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sostxt = db.Column(db.String(200))
    
    def __repr__(self):
        return '<SOS %r>' % (self.user_id)

   
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    msg = db.Column(db.Text)
    mode = db.Column(db.String(10))
    
    def __repr__(self):
        return '<Notification %r>' % (self.user_id)
     
  
class NotificationContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    email = db.Column(db.String(25))
    phonenum = db.Column(db.String(25))
    
    def __repr__(self):
        return '<NotificationContact %r>' % (self.email)
     
