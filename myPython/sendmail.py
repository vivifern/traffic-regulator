import sendgrid
import os
from sendgrid.helpers.mail import *

class SendMail:

	def send_mail(self,time_stam,car_no,loc_name,fine_amount,email_id,name_of_user):
		sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		from_email = Email(email_id)
		subject = "Test Mail to Display Voilation!"
		to_email = Email(email_id)
		str_content="User,\n \n Seems like you have voilated traffic rules! Below are the details:\v Time Stamp \t : \t"+str(time_stam)+"\nCar Number \t : \t"+car_no+"\nLocation \t : \t"+loc_name+"\nFine Amount \t : \t"+str(fine_amount)
		content = Content("text/plain", str_content)
		mail = Mail(from_email, to_email, subject, content)
		personalization = Personalization()
		personalization.add_bcc(Email("vivianfernandes6795@gmail.com"))
		mail.add_personalization(personalization)
		response = sg.send(mail)
		#response = sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)
		verbose="Sent Mail to User "+name_of_user
		return verbose