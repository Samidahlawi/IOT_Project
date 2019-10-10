from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin


db = SQLAlchemy()




class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100),unique=True)
	email = db.Column(db.String(80),unique=True)
	pwdhash = db.Column(db.String(54))


	def __init__(self,username,password,email):
		self.username = username
		self.email = email
		self.set_password(password)

	def set_password(self,password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.pwdhash,password)

class Experiment(db.Model):
	__tablename__ = 'experiments'
	eid = db.Column(db.Integer,primary_key=True)
	uid = db.Column(db.Integer)
	title = db.Column(db.String(100))
	description = db.Column(db.Text)
	created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	duration = db.Column(db.Integer)
	protocol = db.Column(db.String(25))
	status = db.Column(db.String(15))

	def __init__(self,uid,title,duration,protocol,description = ''):
		self.uid = uid
		self.title = title
		self.description = description
		self.duration = duration
		self.protocol = protocol
		self.status = "Waiting"

class Node(db.Model):
	__tablename__ = 'nodes'
	nid = db.Column(db.Integer,primary_key=True)
	eid = db.Column(db.Integer)
	name = db.Column(db.String(50))
	humdity = db.Column(db.Integer)
	temperature = db.Column(db.Integer)
	protocol = db.Column(db.String(50))

	def __init__(self,eid,name,humdity,temperature,protocol):
		self.eid = eid
		self.name = name
		self.humdity = humdity
		self.temperature = temperature
		self.protocol = protocol

class Scenario(db.Model):
	__tablename__ = 'scenario'
	pid = db.Column(db.Integer,primary_key=True)
	eid = db.Column(db.Integer)
	en1 = db.Column(db.Integer)
	en2 = db.Column(db.Integer)

	def __init__(self,eid,en1,en2):
		self.eid = eid
		self.en1 = en1
		self.en2 = en2

class Result(db.Model):
	__tablename__ = 'results'
	res_id = db.Column(db.Integer,primary_key=True)
	pid = db.Column(db.Integer)
	eid = db.Column(db.Integer)
	output = db.Column(db.String(255))

	def __init__(self,pid,eid,output):
		self.pid = pid
		self.eid = eid
		self.output = output