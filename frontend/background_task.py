import random
import time
import os

while True:
    os.system("echo %s > companies.txt" % random.randint(0, 100000))
    time.sleep(2)
