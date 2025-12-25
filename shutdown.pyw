import os
import psutil
import time
from time import sleep

TIME_SHUTDOWN = 6  # Thời gian hoạt động tối đa (giờ)
thoigiantatmay = TIME_SHUTDOWN * 60 * 60
		
boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time
if uptime_seconds > thoigiantatmay:
	os.system("shutdown /s")