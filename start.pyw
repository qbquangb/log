import imaplib
import email
import os
import subprocess
from time import sleep
import socket
import time
import ctypes
import sys

def run_as_admin():
	if ctypes.windll.shell32.IsUserAnAdmin():
		return True
	else:
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
		sys.exit()

run_as_admin()

# Cấu hình thông tin đăng nhập Gmail
USERNAME = 'qbquangbinh@gmail.com'
PASSWORD = os.getenv("PASS_EMAIL") # Nếu dùng xác thực 2 bước, hãy sử dụng App Password

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

TIMEOUT_SECONDS = 40 # Thời gian chờ tối đa cho kết nối mạng
isConnected = True

def check_and_download():
	try:
		# Kết nối tới server IMAP của Gmail
		mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
		mail.login(USERNAME, PASSWORD)
		mail.select("inbox")

		# Tìm kiếm email chưa đọc từ người gửi qbquangbinh@gmail.com với Subject chứa "boot config"
		while True:
			search_criteria = '(UNSEEN FROM "qbquangbinh@gmail.com" SUBJECT "boot config")'
			status, messages = mail.search(None, search_criteria)
			if status == 'OK':
				break
		email_ids = messages[0].split()
		if not email_ids:
			print("Không có email mới.")
			mail.logout()

			with open("boot_config.txt", "w", encoding="utf-8") as file:
				lines = ["off\n", "off\n", "off"]
				file.writelines(lines)
				file.close()

			return False # Không có email mới

		for email_id in email_ids:
			status, data = mail.fetch(email_id, '(RFC822)')
			if status != 'OK':
				print("Lỗi khi lấy email id:", email_id)
				continue
			# Lấy nội dung email
			raw_email = data[0][1]
			msg = email.message_from_bytes(raw_email)

			# Lưu nội dung email vào file boot_config.txt
			with open("boot_config.txt", "w", encoding="utf-8") as config_file:
				if msg.is_multipart():
					for part in msg.walk():
						if part.get_content_type() == "text/plain":
							config_file.write(part.get_payload(decode=True).decode("utf-8"))
				else:
					config_file.write(msg.get_payload(decode=True).decode("utf-8"))
					   
			# Đánh dấu email đã đọc
			mail.store(email_id, '+FLAGS', '\\Seen')

		mail.logout()
		return True # Đã tải xuống thành công
	except BaseException as e:
		print(f"Đã xảy ra lỗi khi kiểm tra email: {e}")
		with open("boot_config.txt", "w", encoding="utf-8") as file:
			lines = ["off\n", "off\n", "off"]
			file.writelines(lines)
			file.close()
		return False # Lỗi khi kiểm tra email

def is_connected():
	try:
		# Kiểm tra kết nối tới máy chủ DNS của Google
		socket.create_connection(("8.8.8.8", 53), timeout=5)
		return True
	except:
		return False
	
def clean_boot_config(file_path):
	try:
		# Đọc nội dung tệp
		with open(file_path, "r", encoding="utf-8") as file:
			lines = file.readlines()
			file.close()

		# Chỉ giữ lại dòng số 3, 7 và 11 (chỉ số bắt đầu từ 0)
		selected_lines = [lines[2], lines[6], lines[10]]

		# Ghi lại nội dung đã chọn vào tệp
		with open(file_path, "w", encoding="utf-8") as file:
			file.writelines(selected_lines)
			file.close()

		print("Tệp boot_config.txt đã được sửa thành công.")
	except IndexError:
		print("Tệp boot_config.txt không có đủ dòng để sửa.")
		with open("boot_config.txt", "w", encoding="utf-8") as file:
			lines = ["off\n", "off\n", "off"]
			file.writelines(lines)
			file.close()
	except Exception as e:
		print(f"Đã xảy ra lỗi: {e}")
		with open("boot_config.txt", "w", encoding="utf-8") as file:
			lines = ["off\n", "off\n", "off"]
			file.writelines(lines)
			file.close()
	except BaseException as e:
		print(f"Đã xảy ra lỗi không xác định: {e}")
		with open("boot_config.txt", "w", encoding="utf-8") as file:
			lines = ["off\n", "off\n", "off"]
			file.writelines(lines)
			file.close()

if __name__ == "__main__":
	file_path = "boot_config.txt"
	start = time.time()
	while not is_connected():
		elapsed = time.time() - start
		if elapsed >= TIMEOUT_SECONDS:
			isConnected = False
			with open("boot_config.txt", "w", encoding="utf-8") as file:
				lines = ["off\n", "off\n", "off"]
				file.writelines(lines)
				file.close()
			break
		print("Không có kết nối mạng. Đang chờ...")
		sleep(5)
	if not isConnected:
		print(f"Không có kết nối mạng sau {TIMEOUT_SECONDS}s")
	else:
		print("Đã kết nối mạng.")
	if isConnected:
		if check_and_download():
			clean_boot_config(file_path)

	remove_files = ["log_run.txt", "protect_run.txt", "assistant_run.txt"]
	for file in remove_files:
		if os.path.exists(file):
			os.remove(file)

	with open(file_path, "r", encoding="utf-8") as file:
		lines = file.readlines()

	if lines[0].strip() == "on":
		with open("log_run.txt", "w", encoding="utf-8") as log_file:
			log_file.write("on")
		
	if lines[1].strip() == "on":
		with open("protect_run.txt", "w", encoding="utf-8") as protect_file:
			protect_file.write("on")

	if lines[2].strip() == "on":
		with open("assistant_run.txt", "w", encoding="utf-8") as assistant_file:
			assistant_file.write("on")

	subprocess.run("a.bat", shell=True)