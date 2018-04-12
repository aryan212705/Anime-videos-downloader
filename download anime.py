import requests
import os
from bs4 import BeautifulSoup
link = input("Enter the link of the page with list of episodes(for ex: https://otakustream.tv/anime/steinsgate): ")
#link = "https://otakustream.tv/anime/steinsgate"
page = requests.get(link)
soup = BeautifulSoup(page.content, "html.parser")
eplist_div = soup.find("div", class_ = "ep-list")
eplist = eplist_div.find("ul")
episodes = eplist.findAll("li")
no_of_ep = len(episodes)
links = []
for episode in range(no_of_ep):
    if link[-1] == '/':
        new_link = link + "episode-" + str(episode+1)
    else:
        new_link = link + "/episode-" + str(episode+1)
    new_page = requests.get(new_link)
    new_soup = BeautifulSoup(new_page.content, "html.parser")
    ep_div = new_soup.find("div", class_ = "embed-responsive embed-responsive-16by9")
    iframe1 = ep_div.find("iframe")
    frame_link = "http://otakustream.tv" + iframe1['src']
    response = requests.get(frame_link)
    iframe2 = BeautifulSoup(response.content, "html.parser").find("iframe")
    links.append(iframe2['src'])
    print("Episode -", episode+1, " : ", links[-1])
    cmd = "youtube-dl "+iframe2['src']
    print("Downloading Episode - ",episode+1,"...")
    print(os.system(cmd))

