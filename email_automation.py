import smtplib
from email.message import EmailMessage


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('aayush.181509@ncit.edu.np', 'Ncit@181509')


def send_email(reciever,subject,message):
    email=EmailMessage()
    email['From']='aayush.181509@ncit.edu.np'
    email['To'] = reciever
    email['Subject']=subject
    email.set_content(message)
    server.send_message(email)

send_email("ayushregmi@gmail.com","Just Checking","Hello This is Aayush")