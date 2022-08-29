import subprocess
import pickle
import time


with open('yml_list.pickle', 'rb') as handle:
    pathlist = pickle.load(handle)

for item in pathlist:
    print(item)
    cwdpath = item.split('docker-compose.yml')[0]
    subprocess.Popen("/usr/bin/docker-compose up -d", cwd=cwdpath, shell=True)
    time.sleep(3)
    # need to wait longer and stop first one, then check for settings.json file
    # can set throttle in settings.json or use docker compose to set i/o instead