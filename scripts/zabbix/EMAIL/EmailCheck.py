import os
import sys
import smtplib

#server = smtplib.SMTP('smtp.gmail.com',587)
server = smtplib.SMTP('smtp.gmail.com', 25)
server.connect("smtp.gmail.com",465)
server.ehlo()
server.starttls()
server.ehlo()
server.login("gomesvenzi@gmail.com", "password")
text = msg.as_string()
server.sendmail("gomesvenzi@gmail.com", "gomesvenzi@gmail.com", "Hello!")
server.quit()
