import urllib.request
import re
import pickle
import os
import socket


torrent_base_path = "/home/user/torrent_rootdir/"
max_torrents = 100
socket.setdefaulttimeout(3)

def get_main_list():
    urllib.request.urlretrieve("https://fosstorrents.com/feed/torrents.xml", "foss_feed.txt")



def process_the_list():
    max_torrents = 100
    file = open('foss_feed.txt', "r")
    lines = file.readlines()
    torrentcount = 0
    torrentlist = []

    for line in lines:
        if '<link>' in line:    # get torrent file - opening tag
            if '.torrent</link>' in line:  # get torrent file - closing tag
                #print(line)
                out = re.search('<link>(.*)</link>', line) # remove xml tags
                output = out.group(1)
                #print(output)
                torrentcount += 1  # count every torrent found
                torrentlist.append(output)

    with open('filename.pickle', 'wb') as handle:
        pickle.dump(torrentlist, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('writing pickle')
        handle.close()

    containerqty = int(torrentcount / max_torrents) + (torrentcount % max_torrents > 0)
    print('Total number of torrents found: ', torrentcount)
    print('Number of docker containrs needed: ', containerqty)



def grab_torrent_files():
    resumepos = 380 # should be 1 if we arent using this dont assign 0
    with open('filename.pickle', 'rb') as handle:
        file = pickle.load(handle)
    containerid = (resumepos // max_torrents) + 1
    itxdupe = resumepos % max_torrents
    itx = resumepos
    while itx < len(file):
        line = file[itx]
        filepath = os.path.join(torrent_base_path, str(containerid), "watch", os.path.basename(line))
        print(file[itx])
        try:
            urllib.request.urlretrieve(line, filepath) #download it
        except Exception as e:
            print("error", e)
        itx += 1
        itxdupe += 1
        if itxdupe == max_torrents:
            itxdupe = 0
            containerid += 1
        print('itx val: ', itx , '\n', 'containerid: ', containerid)




# get_main_list()
#process_the_list()
grab_torrent_files()