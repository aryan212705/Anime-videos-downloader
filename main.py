import os
import requests
from bs4 import BeautifulSoup
import getlinks
import quality
import directlinks
import downloadfile


def choices(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.findAll("div", class_ = "ep-box")
    links, names = [], []
    i = 0
    for divs in div:
        i += 1
        div1 = divs.find("div", class_ = "caption-category")
        div2 = divs.find("div", class_ = "cch-content")
        ep_no = div1.find("span", class_ = "ep-no")
        ep_no = ep_no.get_text()
        status = div1.find("span", class_ = "anime-status")
        if status:
            status = status.get_text()
        else:
            status = "Finished"
        link = div1.find("a")
        links.append(link['href'])
        name = link.get_text()
        names.append(name)
        print("\n")
        print("..........Option :", i,"..........")
        print("Name :", name)
        print(ep_no)
        print("Status :", status)
        for para in div2:
            print(para.get_text())
        print("x===x===x===x===x===x===x===x===x===x===x===x")
    return [links, names]


def select(total):
    option = int(input("\nChoose the required option: "))
    while option not in range(1, total+1):
        option = int(input("\nChoose a valid option: "))
    return option
    

def init():
    name = input("Enter the name of anime to be downloaded: ")
    url = "http://otakustream.tv"
    name.replace(" ","+")
    url = url + "?s=" + name
    response = choices(url)
    return response

response = init()
links = response[0]
names = response[1]

while not len(links):
    print("SORRY!! No anime by this name exist...")
    response = init()
    links, names = response[0], response[1]
    
choice = select(len(links))
urls = getlinks.playlist(links[choice-1])
qualities = quality.quality(urls[0])
choice = select(len(qualities))
name = names[choice-1]
ep_no = 0

for url in urls:
    ep_no += 1
    directlinks.videos(qualities[choice-1], url, name, ep_no)
    
print("Done")
