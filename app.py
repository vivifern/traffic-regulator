'''File controller'''
import os
import psycopg2
from flask import Flask, redirect, url_for, render_template, request, session, g
import urllib.parse as urlparse
from flask_sqlalchemy import SQLAlchemy
import time
import smtplib
import email.mime.text
import requests

#heroku run:detached python app.py -a traffic-regulator
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
app.secret_key=os.urandom(24)
db=SQLAlchemy(app)

@app.route('/',methods = ['POST', 'GET'])
def index():
	
	verbose="Please Enter Username and Password"
	return render_template('admin-login.html',verbose=verbose)
		
@app.route('/logout',methods = ['POST', 'GET'])
def logout():
	
	session.pop('username', None)
	verbose="You have ben logged out"
	return render_template('admin-login.html',verbose=verbose)

@app.route('/remove-admin',methods = ['POST', 'GET'])
def remove_admin():
	
	user_name=request.form['user_name']
	mob_number=request.form['mob_number']
	
	if(session['username']=='root'):
		rmAdmin=Admins.query.filter_by(MOBILE_NUMBER=mob_number).first()
		if(rmAdmin.ADMIN_USER_NAME==user_name):
			
			db.session.delete(rmAdmin)
			db.session.commit()
			verbose="Removed admin "+user_name
			return render_template('verbose-page.html', verbose=verbose)
			
		else:
			verbose="Unable to remove Admin ",user_name
			return render_template('verbose-page.html', verbose=verbose)
	
	elif(session['user']=='root'):
		
		verbose="Only Root Admin can add new Admins"
		
@app.route('/remove-user',methods = ['POST', 'GET'])
def remove_user():
	
	mob_number=request.form['mob_number']
	email_address=request.form['email_address']
	
	rmUser=Users.query.filter_by(MOBILE_NUMBER=mob_number).first()
	if(rmUser.EMAIL_ID==email_address):
		
		user_name=rmUser.NAME_OF_USER
		db.session.delete(rmUser)
		db.session.commit()
		verbose="Removed User "+user_name
		return render_template('verbose-page.html', verbose=verbose)
		
	else:
	
		user_name=rmUser.NAME_OF_USER
		verbose="Unable to remove User "+user_name
		return render_template('verbose-page.html', verbose=verbose)
		
	
@app.route('/admin_login',methods=['POST','GET'])
def admin_login():
#
	username=request.form['user_name']
	password=request.form['pass_word']
	session.pop('username', None)
	verbose=""
	
	try:
	
		adminsTest=Admins.query.filter_by(ADMIN_USER_NAME=username).first()
			
		if(adminsTest.ADMIN_USER_NAME!=username or adminsTest.ADMIN_PASSWORD!=password):
			
			verbose="Incorrect Username or Password, Please re-enter your Details!!!"
			return render_template('admin-login.html',verbose=verbose)
	
		elif(adminsTest.ADMIN_USER_NAME==username and adminsTest.ADMIN_PASSWORD==password):
			
			session['username']=username
			return render_template('root-home.html')
			
	except AttributeError:
		
		verbose="Invalid Credentials, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	

@app.route('/add_admin_control',methods=['POST','GET'])
def add_admin_control():
#
	adm_name=request.form['adm_name']
	adm_mobNo=request.form['adm_mobNo']
	adm_userName=request.form['adm_userName']
	adm_password=request.form['adm_password']
	
	
	#verbose="Admin could not be Added"
	
	#app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
	#db=SQLAlchemy(app)
	#maxAdm = Admins.query.order_by(Admins.ADM_NO.desc()).first()
	#setAdmNo=maxAdm.ADM_NO + 1
	#insertNew=Admins(setAdmNo,adm_name,adm_mobNo,adm_userName,adm_password)
	#db.session.add(insertNew)
	#db.session.commit()
	verbose=adm_name+" Added as New Admin"
	verbose=addAdmins(0,adm_name,adm_mobNo,adm_userName,adm_password)
	
	return render_template('verbose-page.html', verbose=verbose)
		
	

@app.route('/add-user-control',methods=['POST','GET'])
def add_user_control():

	name_of_user=request.form['name_of_user']
	mobile_number=request.form['mobile_number']
	email_address=request.form['email_address']
	state_code=request.form['state_code']
	number_code=request.form['number_code']
	area_code=request.form['area_code']
	pin=request.form['pin']
    
	car_number=state_code+"-"+number_code+"-"+area_code+"-"+pin
	
	verbose="User could not be Added"

	#db=SQLAlchemy(app)
	#maxUsr = Users.query.order_by(Admins.ADM_NO.desc()).first()
	#setUsrNo=maxUsr.USR_NO + 1
	#insertNew=Users(setUsrNo,adm_name,adm_mobNo,adm_userName,adm_password)
	#db.session.add(insertNew)
	#db.session.commit()
	verbose=addUsers(0,name_of_user,mobile_number,email_address,car_number)
	
	#verbose="User "+name_of_user+" Added"

	return render_template('verbose-page.html', verbose=verbose)
	
@app.route('/update-admin',methods=['POST'])
def update_admin():

	dropDown1=request.form['dropDwn1']
	mob_number=request.form['mob_number']
	admin_name=request.form['admin_name']
	
	admDetails=Admins.query.filter_by(MOBILE_NUMBER=mob_number).first()
		
	try:
	
		if(str(format(session['username'])) == 'root'):
		
			if(dropDown1=="name"):
				
				admDetails.ADMIN_NAME=admin_name
				db.session.commit()
				updatedAdmDetails=Admins.query.filter_by(MOBILE_NUMBER=mob_number).first()
				verbose="Updated details for Admin, Corrected Name: "+updatedAdmDetails.ADMIN_NAME
				
			elif(dropDown1=="mob_number"):
				
				admDetails.MOBILE_NUMBER=admin_name
				db.session.commit()
				updatedAdmDetails=Admins.query.filter_by(MOBILE_NUMBER=admin_name).first()
				verbose="Updated details for Admin "+updatedAdmDetails.ADMIN_NAME+" Corrected/New Number: "+updatedAdmDetails.MOBILE_NUMBER
				
			elif(dropDown1=="user_name"):
				
				admDetails.ADMIN_USER_NAME=admin_name
				db.session.commit()
				updatedAdmDetails=Admins.query.filter_by(MOBILE_NUMBER=mob_number).first()
				verbose="Updated details for Admin "+updatedAdmDetails.ADMIN_NAME+" Corrected/New Username: "+updatedAdmDetails.ADMIN_USER_NAME
				
			return render_template('verbose-page.html', verbose=verbose)
		
		elif(str(format(session['username'])) != 'root'):
			
			verbose="Only Root Admin can add new Admins"
			return render_template('verbose-page.html', verbose=verbose)
			
#	except KeyError:
#		
#		verbose="You have not logged in, Please login to Continue"
#		return render_template('admin-login.html',verbose=verbose)
#		
#	except AttributeError:
#	
#		verbose="Admin's Existing Entry does not exist"
#		return render_template('admin-login.html',verbose=verbose)
	
	except Exception as e: 
		return e
		
@app.route('/update-user',methods=['POST','GET'])
def update_user():

	dropDown1=request.form['dropDwn1']
	mob_number=request.form['mob_number']
	usr_name=""
	state_code=""
	number_code=""
	area_code=""
	pin=""
	
	if(dropDown1!="car_number"):
		
		usr_name=request.form['usr_name']
		
	elif(dropDown1=="car_number"):
		state_code=request.form['state_code']
		number_code=request.form['number_code']
		area_code=request.form['area_code']
		pin=request.form['pin']
	
	userDetails=Users.query.filter_by(MOBILE_NUMBER=mob_number).first()
	
	if(dropDown1=="name"):
		
		userDetails.NAME_OF_USER=usr_name
		db.session.commit()
		updatedUserDetails=Users.query.filter_by(MOBILE_NUMBER=mob_number).first()
		verbose="Updated details for User Corrected Name: "+updatedUserDetails.NAME_OF_USER
	
	elif(dropDown1=="mob_number"):
		
		userDetails.MOBILE_NUMBER=usr_name
		db.session.commit()
		updatedUserDetails=Users.query.filter_by(MOBILE_NUMBER=usr_name).first()
		verbose="Updated details for User "+updatedUserDetails.NAME_OF_USER+" Corrected/New Mobile Number: "+updatedUserDetails.MOBILE_NUMBER
		
	elif(dropDown1=="email_address"):
		
		userDetails.EMAIL_ID=usr_name
		db.session.commit()
		updatedUserDetails=Users.query.filter_by(MOBILE_NUMBER=mob_number).first()
		verbose="Updated details for User "+updatedUserDetails.NAME_OF_USER+" Corrected/New Mobile Number: "+updatedUserDetails.EMAIL_ID
		
		
	elif(dropDown1=="car_number"):
		
		car_no=state_code+"-"+number_code+"-"+area_code+"-"+pin
		userDetails.CAR_NO=car_no
		db.session.commit()
		updatedUserDetails=Users.query.filter_by(MOBILE_NUMBER=mob_number).first()
		verbose="Updated details for User "+updatedUserDetails.NAME_OF_USER+" Corrected/New Car Number: "+updatedUserDetails.CAR_NO
		
	return render_template('verbose-page.html', verbose=verbose)
	
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
		
@app.route('/route-addAdmin',methods=['POST','GET'])
def route_addAdmin():
	
	try:
		
		if(str(format(session['username'])) == 'root'):
		
			return render_template('addAdmin.html')
		
		elif(format(session['username'])!='root'):
			
			verbose="Only Root Admin can add new Admins"
			return render_template('verbose-page.html', verbose=verbose)
	
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)		
	
@app.route('/route-updateAdminPassword',methods=['POST','GET'])
def route_updateAdminPassword():
	
	try:
	
		if(str(format(session['username'])) == 'root'):
			
			return render_template('updateAdmin.html')
			
		elif(str(format(session['username'])) != 'root'):
			
			verbose="Only Root Admin can add new Admins"
			return render_template('verbose-page.html', verbose=verbose)

	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-removeAdmin',methods=['POST','GET'])
def route_removeAdmin():
	
	try:
	
		if(str(format(session['username'])) == 'root'):
			
			return render_template('removeAdmins.html')
		
		elif(format(session['username'])!='root'):
			
			verbose="Only Root Admin can add new Admins"
			return render_template('verbose-page.html', verbose=verbose)

	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-addUser',methods=['POST','GET'])
def route_addUser():
	
	try:
	
		if(str(format(session['username'])) != '' or str(format(session['username'])) != None):
	
			return render_template('addUser.html')
	
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-updateUser',methods=['POST','GET'])
def route_updateUser():
	
	try:
	
		if(str(format(session['username'])) != '' or str(format(session['username'])) != None):
		
			return render_template('updateUser.html')
	
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-removeUser',methods=['POST','GET'])
def route_removeUser():
	
	try:
	
		if(str(format(session['username'])) != '' or str(format(session['username'])) != None):
	
			return render_template('removeUser.html')
	
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-fetchUserDetails',methods=['POST','GET'])
def route_fetchUserDetails():
	
	try:
	
		if(str(format(session['username'])) != '' or str(format(session['username'])) != None):
	
			return render_template('payment.html')
	
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)

@app.route('/route-payment',methods=['POST','GET'])
def route_payment():
	
	try:
	
		if(str(format(session['username'])) != '' or str(format(session['username'])) != None):	
		
			return render_template('payment-details.html')
			
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-generate-pdf',methods=['POST','GET'])
def route_generate_pdf():
	
	try:
	
		if(str(format(session['username'])) != '' or str(format(session['username'])) != None):	
	
			return render_template('generate-pdf.html')

	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
@app.route('/route-returnHome',methods=['POST','GET'])
def route_returnHome():
	
	user_name=format(session['username'])
	
	try:
	
		if(str(user_name) != '' or str(user_name) != None):	
	
			return render_template('root-home.html')
			
	except KeyError:
		
		verbose="You have not logged in, Please login to Continue"
		return render_template('admin-login.html',verbose=verbose)
	
class Admins(db.Model):

	ADM_NO=db.Column(db.Integer,primary_key=True)
	ADMIN_NAME=db.Column(db.String(20),unique=False)
	MOBILE_NUMBER=db.Column(db.BigInteger,unique=True)
	ADMIN_USER_NAME=db.Column(db.String(10),unique=True)
	ADMIN_PASSWORD=db.Column(db.String(16),unique=False)
	
	def __init__(self,ADM_NO,ADMIN_NAME,MOBILE_NUMBER,ADMIN_USER_NAME,ADMIN_PASSWORD):
		
		self.ADM_NO=ADM_NO
		self.ADMIN_NAME=ADMIN_NAME
		self.MOBILE_NUMBER=MOBILE_NUMBER
		self.ADMIN_USER_NAME=ADMIN_USER_NAME
		self.ADMIN_PASSWORD=ADMIN_PASSWORD
		
		
class Users(db.Model):

	USR_NO=db.Column(db.Integer,primary_key=True)
	NAME_OF_USER=db.Column(db.String(20),unique=False)
	MOBILE_NUMBER=db.Column(db.BigInteger,unique=True)
	EMAIL_ID=db.Column(db.String(30),unique=True)
	CAR_NO=db.Column(db.String(13),unique=False)
	
	def __init__(self,USR_NO,NAME_OF_USER,MOBILE_NUMBER,EMAIL_ID,CAR_NO):
		
		self.USR_NO=USR_NO
		self.NAME_OF_USER=NAME_OF_USER
		self.MOBILE_NUMBER=MOBILE_NUMBER
		self.EMAIL_ID=EMAIL_ID
		self.CAR_NO=CAR_NO
		
		
class Violations(db.Model):

	REC_NO=db.Column(db.Integer,primary_key=True)
	TIME_STAM=db.Column(db.String(30),unique=False)
	CAR_NO=db.Column(db.String(13),unique=False)
	LOC_NAME=db.Column(db.String(30),unique=False)
	FINE_AMOUNT=db.Column(db.Integer,unique=False)
	
	def __init__(self,REC_NO,TIME_STAM,CAR_NO,LOC_NAME,FINE_AMOUNT):
		
		self.REC_NO=REC_NO
		self.TIME_STAM=TIME_STAM
		self.CAR_NO=CAR_NO
		self.LOC_NAME=LOC_NAME
		self.FINE_AMOUNT=FINE_AMOUNT

def adminLogin(username,password):
	
	adminsTest=Admins.query.filter_by(ADMIN_USER_NAME=username).first()
	return adminsTest
		
def addAdmins(setAdmNo,adm_name,adm_mobNo,adm_userName,adm_password):
	
	if(setAdmNo!=1):
	
		maxAdm = Admins.query.order_by(Admins.ADM_NO.desc()).first()
		setAdmNo=maxAdm.ADM_NO + 1
	
	insert=Admins(setAdmNo,adm_name,adm_mobNo,adm_userName,adm_password)
	db.session.add(insert)
	db.session.commit()
	newMaxAdmId=Admins.query.order_by(Admins.ADM_NO.desc()).first()
	fetchAdmNo=newMaxAdmId.ADM_NO
	verbose="New Admin "+adm_name+" Added with ID " +str(fetchAdmNo)
	return verbose
	
def addUsers(setUsrNo,name_of_user,mobile_number,email_address,car_number):
	
	if(setUsrNo!=1):
	
		maxUsr = Users.query.order_by(Users.USR_NO.desc()).first()
		setUsrNo=maxUsr.USR_NO + 1
	insert=Users(setUsrNo,name_of_user,mobile_number,email_address,car_number)
	db.session.add(insert)
	db.session.commit()
	newMaxUsrId=Users.query.order_by(Users.USR_NO.desc()).first()
	fetchUsrNo=newMaxUsrId.USR_NO
	verbose="New User "+name_of_user+" Added " +str(fetchUsrNo)
	return verbose
	
def addVoilations(setRecNo,car_no,loc_name):
	
	amount=500
	time_stam=time.time()
	userDetails=Users.query.filter_by(CAR_NO=car_no).first()
	email_id=userDetails.EMAIL_ID
	name_of_user=userDetails.NAME_OF_USER
	#send_mail=SendMail()
	
	#verbose=sen_mail(time_stam,car_no,loc_name,amount,email_id,name_of_user)
	insertVoilation=Violations(setRecNo,str(time_stam),car_no,loc_name,amount)
	db.session.add(insertVoilation)
	db.session.commit()
	#verbose="Sent Mail to User "+name_of_user
	print(verbose)
	#return render_template('verbose-page.html', verbose=verbose)
	#template = env.get_template(template_name)
    #return template.render(**template_vars)
	
def sen_mail(time_stam,car_no,loc_name,fine_amount,email_id,name_of_user):
	
	#API_KEY = os.environ.get('MAILGUN_API_KEY')
	API_MAIL_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
	#API_URL = "https://api:#{API_KEY}@api.mailgun.net/v2/{API_MAIL_DOMAIN}"
	API_USERNAME = os.environ.get('MAILGUN_SMTP_LOGIN')
	API_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
	MAILGUN_SMTP_SERVER = os.environ.get('MAILGUN_SMTP_SERVER')

	msg = email.mime.text.MIMEText('Testing some Mailgun awesomness')
	msg['Subject'] = "Hello"
	msg['From']    = "root@"+API_MAIL_DOMAIN
	msg['To']      = email_id
	
	s = smtplib.SMTP(MAILGUN_SMTP_SERVER, 587)
	
	s.login(API_USERNAME, API_PASSWORD)
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()
	'''API_KEY = os.environ.get('MAILGUN_API_KEY')
	API_MAIL_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
	#return 
	requests.post(
		"https://api.mailgun.net/v3/{API_MAIL_DOMAIN}/messages",
		auth=("api", API_KEY),
		data={"from": "Excited User <root@{API_MAIL_DOMAIN}>",
			"to": "email_id",
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})'''
	verbose="Sent Mail to User "+name_of_user
	return verbose
	
@app.route('/payment-details-control',methods = ['POST', 'GET'])
def payment_details_control():

	dropDown1=request.form['dropDwn1']
	mob_number=request.form['mob_number']
	
	#return "Values from form: " + dropDown1 + " " + mob_number
	
	
	userDetails=Users.query.filter_by(MOBILE_NUMBER=mob_number).first()
	car_number=userDetails.CAR_NO
	
	#return "User table recodr for the "+ str(userDetails.MOBILE_NUMBER) + " " + userDetails.CAR_NO
	voilationRecord=Violations.query.filter_by(CAR_NO=car_number).first()
	
	#return "Voilation table recodr for the user"+str(voilationRecord.TIME_STAM) + " " + voilationRecord.CAR_NO
	
	if(dropDown1=="payment"):
	
		return render_template('payment.html',voilationRecord=voilationRecord)
		
	elif(dropDown1=="generate-pdf"):
	
		return render_template('generate-email.html',voilationRecord=voilationRecord)
		
@app.route('/make-payment-control',methods = ['POST', 'GET'])
def make_payment_control():

	time_stamp=request.form['time_stamp']
	
	rmViolation=Violations.query.filter_by(TIME_STAM=time_stamp).first()
	usrCarNo=rmViolation.CAR_NO
	fetchUsr=Users.query.filter_by(CAR_NO=usrCarNo).first()
	usrName=fetchUsr.NAME_OF_USER
	db.session.delete(rmViolation)
	db.session.commit()
	verbose="Payment Received from User "+usrName
	return render_template('verbose-page.html', verbose=verbose)
		
@app.route('/generate-email-control',methods = ['POST', 'GET'])
def generate_email():

	time_stam=request.form['time_stam']
	
	voilationRecord=Violations.query.filter_by(TIME_STAM=time_stam).first()
	car_no=voilationRecord.CAR_NO
	userDetails=Users.query.filter_by(CAR_NO=car_no).first()
	loc_name=voilationRecord.LOC_NAME
	amount=voilationRecord.FINE_AMOUNT
	email_id=userDetails.EMAIL_ID
	name_of_user=userDetails.NAME_OF_USER
	#send_mail=SendMail()
	verbose=verbose=sen_mail(time_stam,car_no,loc_name,amount,email_id,name_of_user)
	return render_template('verbose-page.html', verbose=verbose)

if __name__ == '__main__':
	#app.run(debug = True)
	db.create_all()
	'''insertAdm=Admins(1,'MAIN_ADMIN',12345789,'root','ROOT1234')
	db.session.add(insertAdm)
	db.session.commit()
	insertUsr=Users(1,"User1",987654321,"testuser123@gmail.com","MH-01-CH-0007")
	db.session.add(insertUsr)
	db.session.commit()'''
	#addUsers(1,"User1",9876543212,"vivianfernandes6795@gmail.com","KL-01-CC-5919")
	'''addUsers(2,"User1",8422065548,"vivianfernandes67@gmail.com","AP-28-DD-2438")
	addUsers(3,"User1",9167316411,"vivianfernandes6@gmail.com","AP-29-AS-8467")
	addUsers(4,"User1",9769483249,"vivianfernandes@gmail.com","RJ-20-CC-5851")
	addUsers(5,"User1",9619992079,"vivianfernande@gmail.com","TS-07-EK-7622")
	addUsers(6,"User1",8286546670,"vivianfernand@gmail.com","AP-10-BC-1485")
	addUsers(7,"User1",7777721725,"vivianfernan@gmail.com","MH-08-AG-1886")
	addUsers(8,"User1",8625552718,"vivianferna@gmail.com","AP-36-A-5868")'''
	#addVoilations(1,'KL-01-CC-5919','ChurchGate')
	'''addVoilations(2,'AP-28-DD-2438','ChurchGate')
	addVoilations(3,'AP-29-AS-8467','ChurchGate')
	addVoilations(4,'RJ-20-CC-5851','ChurchGate')
	addVoilations(5,'TS-07-EK-7622','ChurchGate')
	addVoilations(6,'AP-10-BC-1485','ChurchGate')
	addVoilations(7,'MH-08-AG-1886','ChurchGate')
	addVoilations(8,'AP-36-A-5868','ChurchGate')'''
	addAdmins(1,'MAIN_ADMIN',12345789,'root','ROOT1234')
	
