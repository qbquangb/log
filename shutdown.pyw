import os
import psutil
import time
from time import sleep

TIME_SHUTDOWN = 14  # Thời gian hoạt động tối đa (giờ)
thoigiantatmay = TIME_SHUTDOWN * 60 * 60
		
boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time

while True:
	if uptime_seconds > thoigiantatmay:
		os.system("shutdown /s")
	sleep(60)  # Kiểm tra mỗi phút