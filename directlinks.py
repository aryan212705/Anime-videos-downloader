import requests
from bs4 import BeautifulSoup
import quality
import downloadfile


def videos(quality, url, name, ep_no):
    url1 = url
    url = url + "&q=" + quality
    try:
        page = requests.get(url)
    except:
        qualities = quality.quality(url1)
        for i in range(len(qualities)):
            qualities[i] = int(qualities[i][:len(qualities[i])-1])
        quality = min(qualities, key=lambda x:abs(x-int(quality[:len(quality)-1])))
        url = url + "&q=" + str(quality) + "p"
        page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    video = soup.find("video")
    video = video.find("source")
    print("Downloading", name, "...")
    filename = downloadfile.download_file(video['src'], name, ep_no)
    print("Download complete")
    
