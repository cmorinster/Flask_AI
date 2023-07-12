import os
import base64
from datetime import datetime, timedelta
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(32), unique=True, index=True)
    token_expiration = db.Column(db.DateTime)
    characters = db.relationship('Characters', backref='creator', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|{self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created
        }

    def get_token(self, expires_in=1200):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for field in data:
            if field not in {'username', 'email', 'password', 'is_admin'}:
                continue
            if field == 'password':
                setattr(self, field, generate_password_hash(data[field]))
            else:
                setattr(self, field, data[field])
        db.session.commit()


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(150), nullable= False)
    #type = db.Column(db.String(150), nullable= True)
    strength = db.Column(db.Integer, nullable= False)
    agility = db.Column(db.Integer, nullable= False)
    intellegence = db.Column(db.Integer, nullable= False)
    speed = db.Column(db.Integer, nullable= False)
    endurance = db.Column(db.Integer, nullable= False)
    camoflague = db.Column(db.Integer, nullable= False)
    health = db.Column(db.Integer, nullable= False)
    link = db.Column(db.String(500), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    champion = db.Column(db.Boolean, nullable = False, default = False)
    wins = db.Column(db.Integer, nullable = False, default = 0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Character {self.id}|{self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            #'type': self.type,
            'strength': self.strength,
            'agility': self.agility,
            'intellegence': self.intellegence,
            'speed': self.speed,
            'endurance': self.endurance,
            'camoflague': self.camoflague,
            'health': self.health,
            'link': self.link,
            'description': self.description,
            'date_created': self.date_created,
            'wins': self.wins,
            'champion': self.champion,
            'creator': User.query.get(self.user_id).to_dict()
        }
    
    def to_dict_wins(self):   
        return{
            'id': self.id,
            'name': self.name,
            'wins': self.wins,
            'creator': User.query.get(self.user_id).to_dict()
        }

        

    def update(self, data):
        for field in data:
            if field not in {'name', 'type', 'strength', 'agility', 'intellegence', 'speed', 'endurance', 'camoflague', 'health', 'description', 'link', 'wins', 'champion' }:
                continue
            setattr(self, field, data[field])
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()