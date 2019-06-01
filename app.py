'''File controller'''
import os
import psycopg2
from flask import Flask, redirect, url_for, render_template, request
import urllib.parse as urlparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Person:#(db.Model):

	app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
	db=SQLAlchemy(app)

	ADM_NO=db.Column(db.Integer,primary_key=True)
	ADMIN_NAME=db.Column(db.String(20),unique=False)
	MOBILE_NUMBER=db.Column(db.Integer,unique=True)
	ADMIN_USER_NAME=db.Column(db.String(10),unique=True)
	ADMIN_PASSWORD=db.Column(db.String(16),unique=False)
	
	def __init__(self,ADM_NO,ADMIN_NAME,MOBILE_NUMBER,ADMIN_USER_NAME,ADMIN_PASSWORD):
		self.ADM_NO=ADM_NO
		self.ADMIN_NAME=ADMIN_NAME
		self.MOBILE_NUMBER=MOBILE_NUMBER
		self.ADMIN_USER_NAME=ADMIN_USER_NAME
		self.ADMIN_PASSWORD=ADMIN_PASSWORD

@app.route('/')
def index():

	#app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
	#db=SQLAlchemy(app)
	
	# Open database connection
	#conn=psycopg2.connect(dbname=dbname,user=user,password=password,host=host,port=port)

	# Prepare a cursor object
	#cursor = conn.cursor()
	
	#query="select count(ADMIN_USER_NAME) from admin_table"
	#query="CREATE TABLE admin_table(ADM_NO SERIAL PRIMARY KEY NOT NULL, ADMIN_NAME VARCHAR(30) NOT NULL, MOBILE_NUMBER NUMBER NOT NULL,ADMIN_USER_NAME VARCHAR(20) NOT NULL, ADMIN_PASSWORD VARCHAR(16) NOT NULL)"
		
	result=0
	app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
	db=SQLAlchemy(app)
		
	try:
		
		#return "Fine till here"
		
		# Execute SQL query using execute() method.
		#cursor.execute(query)

		# Fetch result
		#result=cursor.fetchall()
			
		#cursor.close()
		
		
		db.create_all()
		return "No error"
		
		
		url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
		db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
		schema = "schema.sql"
		conn = psycopg2.connect(db)

		cur = conn.cursor()
		
		cur.execute(query)
		
		'''cur.commit()'''	
		

	#except:
            
		#return "Error while fetching record"
		
	except Exception as e:
		
		return e
	
	if(result>0):
		
		return render_template('admin-login.html')
			
	else:		

		query1="CREATE TABLE user_table(USR_NO SERIAL PRIMARY KEY NOT NULL, NAME_OF_USER VARCHAR(30) NOT NULL, MOBILE_NUMBER NUMBER NOT NULL, EMAIL_ID VARCHAR(30) NOT NULL, CAR_NO VARCHAR(10) NOT NULL)"

		query2="CREATE TABLE admin_table(ADM_NO SERIAL PRIMARY KEY NOT NULL, ADMIN_NAME VARCHAR(30) NOT NULL, MOBILE_NUMBER NUMBER NOT NULL,ADMIN_USER_NAME VARCHAR(20) NOT NULL, ADMIN_PASSWORD VARCHAR(16) NOT NULL)"

		query3="INSERT INTO  admin_table VALUES(1,'MAIN_ADMIN',123456789,'root','ROOT1234')"

		query4="CREATE TABLE locations (LOC_NO SERIAL PRIMARY KEY NOT NULL,LOC_NAME VARCHAR(10) NOT NULL)"

		query5="CREATE TABLE violation_record(REC_NO SERIAL PRIMARY KEY NOT NULL, TIME_STAMP TIMESTAMP NOT NULL,CAR_NO VARCHAR(10) NOT NULL,LOC_NAME VARCHAR(10) NOT NULL,VIOLATION_IMAGE BLOB NOT NULL,FINE_AMOUNT VARCHAR(30) NOT NULL)"

		try:

			# Execute SQL query using execute() method.
			cursor.execute(query1)

			cursor.execute(query2)

			cursor.execute(query4)
			
			cursor.execute(query5)


			# Commit your changes in the database
			cursor.commit()
			
			cursor.execute(query3)
			
			cursor.commit()
			
			cursor.close()
			
			return render_template('admin-login.html')

		except:

			# Rollback in case there is any error
			cursor.rollback()
			
			cursor.close()

@app.route('/admin_login',methods=['POST','GET'])
def admin_login():

	user_name=request.form['user_name']
	pass_word=request.form['pass_word']

	obj_myDB=myDB()

	login_string=obj_myDB.admin_login(user_name,pass_word)

	if(login_string!="SUCCESSFUL"):

		return render_template('admin-login.html')

	else:

		return render_template('home.html')

    


@app.route('/add_admin_control',methods=['POST','GET'])
def add_admin_control():

	adm_name=request.form['adm_name']
	adm_mobNo=request.form['adm_mobNo']
	adm_userName=request.form['adm_userName']
	adm_password=request.form['adm_password']
    
	verbose="Admin could not be Added"

	obj_myDB=myDB()

	verbose=obj_myDB.add_admin(adm_name,adm_mobNo,adm_userName,adm_password)

	return render_template('verbose-page.html', verbose)
	
@app.route('/add_user_control',methods=['POST'])
def add_user_control():

	name_of_user=request.form['name_of_user']
	mobile_number=request.form['mobile_number']
	email_address=request.form['email_address']
	car_number=request.form['car_number']
    
	verbose="User could not be Added"

	obj_myDB=myDB()

	verbose=obj_myDB.user_details(name_of_user,mobile_number,email_address,car_number)

	return render_template('verbose-page.html', verbose)
	
@app.route('/temp_password_control',methods=['POST'])
def temp_password_control():

	user_name=request.form['user_name']
	temp_password=request.form['temp_password']
	re_enter_password=request.form['re_enter_password']

	if(temp_password==re_enter_password):

		obj_myDB=myDB()

		verbose_string=""

		verbose_string=obj_myDB.update_temp_admin_password(user_name,temp_password)

		return render_template('verbose-page.html', verbose_string)

if __name__ == '__main__':
	app.run(debug = True)