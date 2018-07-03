import smtplib
import os
import sys


def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = "From: {0}
".format(from_addr)
    header += "To: {0}
".format(to_addr_list)",".join(to_addr_list)
    header += "Cc: %s
" % ",".join(cc_addr_list)
    header += "Subject: %s

" % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

sendemail(from_addr    = 'gomesvenzi@gmail.com', 
          to_addr_list = ['gomesvenzi@gmail.com'],
          cc_addr_list = ['RC@xx.co.uk'], 
          subject      = 'Howdy', 
          message      = 'Howdy from a python function', 
          login        = 'pythonuser', 
          password     = 'XXXXX')
