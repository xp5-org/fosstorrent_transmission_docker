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
    max_torrents = 100 # sets max number of torrents per container
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
    errorlist = []
    #completedlist = [] #might use this some day
    resumepos = 1       
    # for debug , should be 1 if we arent using this dont assign 0
    with open('filename.pickle', 'rb') as handle:
        file = pickle.load(handle)

    containerid = (resumepos // max_torrents) + 1
    itxdupe = resumepos % max_torrents
    itx = resumepos
    while itx < len(file):
        url = file[itx]
        filepath = os.path.join(torrent_base_path, str(containerid), "watch", os.path.basename(url))
        print(file[itx])
        try:
            urllib.request.urlretrieve(url, filepath) #download it
            #completedlist.append({'position': itx, 'container_id':containerid, 'url': url})
        except Exception as e:
            print("error", e)
            errorlist.append({'position':itx, 'container_id':containerid, 'url':url, 'error':str(e)})
            with open('download_log.pickle', 'wb') as loghandle:
                pickle.dump(errorlist, loghandle, protocol=pickle.HIGHEST_PROTOCOL)
                loghandle.close()
                print('appended errorlist: ', errorlist)
        itx += 1        #outer loop
        itxdupe += 1    #inner-loop , resets for each outer loop
        if itxdupe == max_torrents:
            itxdupe = 0
            containerid += 1
        print('itx val: ', itx , '\n', 'containerid: ', containerid)




# get_main_list()
process_the_list()
#grab_torrent_files()