import requests
from bs4 import BeautifulSoup
from math import ceil


def get_size(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    typ = 0
    while size > 1024:
        size = ceil(size/1024)
        typ += 1
    return str(size) + units[typ]


def download_file(url, name, ep_no):
    local_filename = name + "episode-" + str(ep_no)
    r = requests.get(url, stream=True)
    size = r.headers['Content-Length']
    size = get_size(int(size))
    print("Size :", size)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return local_filename
