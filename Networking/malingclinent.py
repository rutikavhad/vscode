import smtplib

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP("smtp.world4you.com",25)

server.ehlo()

with open("pass.text","r") as f:
    password=f.read()

server.login("sager68104@mogash.com",password)

msg=MIMEMultipart()
msg['from']="Neturalnine"
msg['to']="pafijiw769@besaies.com"
msg['subject']="just a text "


with open("massage.text","r") as f:
    massage=f.read()

msg.attach(MIMEText(massage,"plain"))


# p=MIMEBase('application','octest_strem')
# p.set_payload(atta)

# encoders.encode_base64

text=msg.as_string()
server.sendmail('sager68104@mogash.com','pafijiw769@besaies.com',text)