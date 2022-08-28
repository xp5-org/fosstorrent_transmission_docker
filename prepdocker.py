import os
import pickle

root_dir = "/home/user/torrent_rootdir"
download_dir = "/home/user/torrent_rootdir/download_complete"
master_compose_file = "/mnt/nas/foss_transmission_tool/docker-compose-example.txt"


def make_dirs(num):
    pathcheck = os.path.exists(root_dir)
    print('pathcheck is', pathcheck)
    if pathcheck == False:
        print("Path '% s' not found" % root_dir)
        return
    itx = 1
    while itx <= num:
        path = os.path.join(root_dir, str(itx))
        os.mkdir(path)
        print("dir '% s' created" % itx)
        itx += 1


def make_config_files(num):
    ymlpathlist = []
    #define start port range here
    rpcport = 9091
    tcpport = 51410
    udpport = 51410
    #base docker name
    container_name = 'transmission'
    itx = 1
    with open(master_compose_file, "r") as masterfile:
        filedata = masterfile.read()
        masterfile.close()
    while itx <= num:
        print(itx)
        path = os.path.join(root_dir, str(itx))
        ymlpath = os.path.join(root_dir, str(itx), 'docker-compose.yml')
        newrpcport = str(rpcport + itx)
        newtcpport = str(tcpport + itx)
        newudpport = str(udpport + itx)
        print('new rpc port is', str(newrpcport))
        print('new tcp port is', str(newtcpport))
        print('new tcp port is', str(newudpport))
        rpcportstring = str(newrpcport)
        new_container_name = container_name + str(itx)
        filedata2 = filedata.replace('RPCPORT', rpcportstring)
        filedata3 = filedata2.replace('TCPPORT', str(newtcpport))
        filedata4 = filedata3.replace('UDPPORT', str(newudpport))
        filedata5 = filedata4.replace('UNIQUEROOTPATH', path)
        filedata6 = filedata5.replace('SHAREDROOTPATH', download_dir)
        filedata7 = filedata6.replace('CONTAINERNAME', new_container_name)
        with open(ymlpath, 'w') as outputfile:
            outputfile.write(filedata7)
            outputfile.close()
            print('wrote a file')
            ymlpathlist.append(ymlpath)
        itx += 1

    with open('yml_list.pickle', 'wb') as handle:
        pickle.dump(ymlpathlist, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('writing yml_list pickle')
        handle.close()




make_dirs(11)
make_config_files(11)