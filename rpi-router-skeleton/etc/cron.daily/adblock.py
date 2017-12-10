#!/usr/bin/env python3

import urllib.request as urllib2

ROUTER_IP = '192.168.0.1'
ADLIST_URLS = [ 'https://adaway.org/hosts.txt',                
                'http://hosts-file.net/.%5Cad_servers.txt',
                'http://www.malwaredomainlist.com/hostslist/hosts.txt',
                'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts;showintro=0;mimetype=plaintext',
                'http://someonewhocares.org/hosts/hosts',
                'http://winhelp2002.mvps.org/hosts.txt']


def get_data(url, max_tries=5):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
        res = urllib2.urlopen(req)              
        return res.read()
    except Exception as ex:                    
        if max_tries > 0:
            return get_data(url, max_tries-1)
        else:
            print(ex)
            print(url)
            return None
        

def format_host_line(s):    
    if s.find('localhost') == -1:
        s = s.replace('127.0.0.1', '').strip().replace('  ', ' ')   
        if len(s.split(' ')) == 1:
            return ROUTER_IP + ' ' + s
        elif len(s.split(' ')) == 2:
            return ROUTER_IP + ' ' + s.split(' ')[1]
        else:
            print('Can\'t format_host_line')
            print(s)
    return None

def process_list(urls, file_name):
    items = set()    
    for url in urls:
        lines = get_data(url)
        if lines:
            lines_list = lines.splitlines()
            for line in lines_list:            
                l = line.decode("utf-8")
                trim_l = l if l.find('#') == -1 else l[:l.find('#')]
                if len(trim_l)>1:
                    items.add(trim_l)

    print('Domains: {}'.format(len(items)))
    with open(file_name,'w') as f: 
        for s in items:        
            formatted_line = format_host_line(s)
            if formatted_line:
                f.write(formatted_line+'\n')
    f.close()


if __name__ == '__main__':
    process_list(ADLIST_URLS, '/etc/hosts.adblock')

