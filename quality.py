import requests
from bs4 import BeautifulSoup


def quality(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    anchor_tags = soup.findAll("a")
    quality, links = [], []
    for i in range(len(anchor_tags)):
        links.append(anchor_tags[i]['href'])
        index = links[-1].find("&")
        quality.append(links[-1][index+3:])
        print(i+1,":",quality[-1])
    return quality
    

