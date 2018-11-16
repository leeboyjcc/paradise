# -*- coding: utf-8 -*-

import re
from datetime import datetime
from collections import Counter


def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s' 
                   r'\[(.+)\]\s'
                   r'"GET\s(.+)\s\w+/.+"\s'
                   r'(\d+)\s'
                   r'(\d+)\s'
                   r'"(.+)"\s'
                   r'"(.+)"'
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers 

def main():
    logs = open_parser('/home/shiyanlou/Code/nginx.log')

    df = '%d/%b/%Y:%H:%M:%S'
    d1 = datetime(2017,1,11,0,0,0)
    d2 = datetime(2017,1,11,23,59,59)
    ip = [item[0] for item in logs if d1 <= datetime.strptime(item[1].split()[0],df) <= d2]
    url = [item[2] for item in logs if item[3] == '404']

    ip_dict = dict([Counter(ip).most_common()[0]]) 
    url_dict = dict([Counter(url).most_common()[0]]) 
    
    return ip_dict, url_dict


if __name__=='__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
