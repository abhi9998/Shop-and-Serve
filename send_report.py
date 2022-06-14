# https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/
# 
# # Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import os
import smtplib
import shutil

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "ece651sns@gmail.com"
toaddr = ["niravtalaviya011@gmail.com", "zanzarukiaabhi@gmail.com", "heli.mistry24@gmail.com", "shanthimeena.arumugam96@gmail.com"]

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

# storing the receivers email address
msg['To'] = ", ".join(toaddr)

# storing the subject
msg['Subject'] = "Coverage Report of SNS unit test execution"

# string to store the body of the mail
body = "PFA"

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

#### Covearage report 

# open the file to be sent
filename = "htmlcov/index.html"
attachment = open(filename, "rb")

# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

#### Test report
# open the file to be sent
filename = "unit_test_report.html"
attachment = open("reports/all_tests.html", "rb")

# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, "Ece@651software")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()

print("Sent email to " + (', '.join(toaddr)))
