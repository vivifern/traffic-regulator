import os
import urllib.parse as urlparse
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, render_template, request
from sqlalchemy.orm import scoped_session,sessionmaker
#from zope.sqlalchemy import ZopeTransactionExtension
#import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
db=SQLAlchemy(app)

#DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

class Admins(db.Model):

	ADM_NO=db.Column(db.Integer,primary_key=True)
	ADMIN_NAME=db.Column(db.String(20),unique=False)
	MOBILE_NUMBER=db.Column(db.Integer,unique=True)
	ADMIN_USER_NAME=db.Column(db.String(10),unique=True)
	ADMIN_PASSWORD=db.Column(db.String(16),unique=False)
	
	def __init__(self,ADM_NO,ADMIN_NAME,MOBILE_NUMBER,ADMIN_USER_NAME,ADMIN_PASSWORD):
		
		self.ADMIN_NAME=ADMIN_NAME
		self.MOBILE_NUMBER=MOBILE_NUMBER
		self.ADMIN_USER_NAME=ADMIN_USER_NAME
		self.ADMIN_PASSWORD=ADMIN_PASSWORD
		
		
class Users(db.Model):

	USR_NO=db.Column(db.Integer,primary_key=True)
	NAME_OF_USER=db.Column(db.String(20),unique=False)
	MOBILE_NUMBER=db.Column(db.Integer,unique=True)
	EMAIL_ID=db.Column(db.String(30),unique=True)
	CAR_NO=db.Column(db.String(10),unique=False)
	
	def __init__(self,USR_NO,NAME_OF_USER,MOBILE_NUMBER,EMAIL_ID,CAR_NO):
		
		self.NAME_OF_USER=NAME_OF_USER
		self.MOBILE_NUMBER=MOBILE_NUMBER
		self.EMAIL_ID=EMAIL_ID
		self.CAR_NO=CAR_NO
		
class Locations(db.Model):

	LOC_NO=db.Column(db.Integer,primary_key=True)
	LOC_NAME=db.Column(db.String(20),unique=True)
	
	def __init__(self,LOC_NO,LOC_NAME,MOBILE_NUMBER,EMAIL_ID,CAR_NO):
		
		self.LOC_NAME=LOC_NAME
		
class Violations(db.Model):

	REC_NO=db.Column(db.Integer,primary_key=True)
	TIME_STAMP=db.Column(db.Integer,unique=False)
	CAR_NO=db.Column(db.String(30),unique=True)
	LOC_NAME=db.Column(db.String(30),unique=True)
	FINE_AMOUNT=db.Column(db.Integer,unique=False)
	
	def __init__(self,REC_NO,TIME_STAMP,CAR_NO,LOC_NAME,VIOLATION_IMAGE,FINE_AMOUNT):
		
		self.TIME_STAMP=TIME_STAMP
		self.CAR_NO=CAR_NO
		self.LOC_NAME=LOC_NAME
		self.VIOLATION_IMAGE=VIOLATION_IMAGE
		self.FINE_AMOUNT=FINE_AMOUNT
		
class fetch_recod:
	def adminLogin(self,username,password):
	
		stringE=""
	
			#login_string=Admin_table.query.filter_by(ADMIN_USER_NAME = username).all()
			#login_string=db
			#from sqlalchemy import and_
			#login_string=DBSession.query(Admin_table).filter(and_(Admin_table.ADMIN_USER_NAME=username,Admin_table.ADMIN_PASSWORD=password))
			#return login_string.ADMIN_USER_NAME
		adminsTest=Admins.query.filter_by(ADMIN_USER_NAME=username).first()
		return adminsTest.ADMIN_USER_NAME

		
if __name__ == '__main__':
	#app.run(debug = True)
	db.create_all()
	insert=Admins(1,'MAIN_ADMIN',123456789,'root','ROOT1234')
	db.session.add(insert)
	db.session.commit()
