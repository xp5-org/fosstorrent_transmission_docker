import urllib.request
import re
import pickle

#urllib.request.urlretrieve("https://fosstorrents.com/feed/torrents.xml", "foss_feed.txt")



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


    with open('filename.pickle', 'rb') as handle:
        b = pickle.load(handle)

    containerqty = int(torrentcount / max_torrents) + (torrentcount % max_torrents > 0)
    print('Total number of torrents found: ', len(b))
    print('Number of docker containrs needed: ', containerqty)


process_the_list()