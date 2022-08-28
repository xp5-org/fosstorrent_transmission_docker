import subprocess
import pickle
#os.system('ls -l')
#sudo docker-compose up -d

with open('yml_list.pickle', 'rb') as handle:
    pathlist = pickle.load(handle)

for item in pathlist:
    print(item)
    cwdpath = item.split('docker-compose.yml')[0]
    subprocess.Popen("/usr/bin/docker-compose up -d", cwd=cwdpath, shell=True)
    #proc = subprocess.Popen(['sudo', 'docker-compose up -d'], cwd=cwdpath, shell=True)