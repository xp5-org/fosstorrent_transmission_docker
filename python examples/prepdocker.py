import os
import sys

root_dir = "/mnt/nas/torrent_rootdir"

def make_dirs(num):
    pathcheck = os.path.exists(root_dir)
    print('pathcheck is', pathcheck)
    if pathcheck == False:
        print("Path '% s' not found" % root_dir)
        return
    itx = 0
    while itx <= num:
        path = os.path.join(root_dir, str(itx))
        os.mkdir(path)
        print("dir '% s' created" % itx)
        itx += 1

make_dirs(3)