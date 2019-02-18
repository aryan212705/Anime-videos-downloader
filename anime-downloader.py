from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from math import ceil
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import random

CAPABILITY_KEY = "pageLoadStrategy"
CAPABILITY_VALUE = "eager"
MODE = "-headless"
FIREFOX_EXECUTABLE_PATH = "geckodriver"
CHROME_EXECUTABLE_PATH = "chromedriver"
PHANTOM_EXECUTABLE_PATH = "phantomjs"
ANIME_NAME = ""
TIMEOUT = 30


def start_driver():
    print("Starting webdriver")
    try:
        caps = DesiredCapabilities().FIREFOX
        caps[CAPABILITY_KEY] = CAPABILITY_VALUE
        profile = webdriver.FirefoxProfile()
        options = webdriver.FirefoxOptions()
        options.add_argument(MODE)
        driver = webdriver.Firefox(profile, executable_path=FIREFOX_EXECUTABLE_PATH, firefox_options=options, capabilities=caps)
        print("Driver started")
    except:
        try:
            caps = DesiredCapabilities().CHROME
            caps[CAPABILITY_KEY] = CAPABILITY_VALUE
            options = webdriver.ChromeOptions()
            options.add_argument(MODE)
            driver = webdriver.Chrome(executable_path=CHROME_EXECUTABLE_PATH, capabilities=caps)
            print("Driver started")
        except:
            try:
                caps = DesiredCapabilities().PHANTOMJS
                caps[CAPABILITY_KEY] = CAPABILITY_VALUE
                driver = webdriver.PhantomJS(executable_path=PHANTOM_EXECUTABLE_PATH, capabilities=caps)
                print("Driver started")
            except:
                print("Webdrivers are missing. Require at any one of these drivers:", "\n1. Geckodriver(for Firefox)\n2. Chromedriver(for Chrome)\n3. PhantomJS")
                exit()
    return driver


def get_size(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    typ = 0
    while size > 1024:
        size = ceil(size/1024)
        typ += 1
    return str(size) + units[typ]


def download_file(url, name, directory):
    local_filename = directory + name
    for i in range(3):
        try:
            r = requests.get(url, stream=True)
        except:
            pass
        else:
            break
    size = r.headers['Content-Length']
    size = get_size(int(size))
    print("Size :", size)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return local_filename
    

def search_server_1(driver):
    global ANIME_NAME, TIMEOUT
    URL = "https://www.cartooncrazy.tv/?s="
    try:
        driver.get(URL + ANIME_NAME)
    except:
        print("Connection Error")
        return []
    driver.implicitly_wait(TIMEOUT)
    div = driver.find_element_by_id("new-series-entry")
    results = [0, 0]
    results[0] = div.find_elements_by_tag_name("a")
    results[1] = div.find_elements_by_tag_name("h3")
    links = []
    for i in range(len(results[0])):
        links.append((results[1][i].text, results[0][i].get_attribute("href")))
    return links


def search_server_2(driver):
    global ANIME_NAME
    URL = "https://www.thewatchcartoononline.tv/search"
    try:
        driver.get(URL)
    except:
        print("Connection Error")
        return []
    input_tag = driver.find_element_by_class_name("catara2")
    input_tag.click()
    input_tag.clear()
    input_tag.send_keys(ANIME_NAME)
    submit = driver.find_element_by_class_name("aramabutonu2")
    submit.click()
    div = driver.find_elements_by_class_name("recent-release-episodes")
    links = []
    for link in div:
        links.append((link.text, link.find_element_by_tag_name("a").get_attribute("href")))
    return links
    

def episode_list_1(driver, URL):
    global TIMEOUT
    try:
        driver.get(URL)
    except:
        print("Connection Error")
        return []
    driver.implicitly_wait(TIMEOUT)
    ep_list_element = driver.find_element_by_id("episode-list")
    ep_list = ep_list_element.find_elements_by_tag_name("a")
    ep_list.reverse()
    links = []
    for link in ep_list:
        links.append((link.get_attribute("title"), link.get_attribute("href")))
    return links


def episode_list_2(driver, URL):
    try:
        driver.get(URL)
    except:
        print("Connection Error")
        return []
    div_element = driver.find_element_by_id("sidebar_right3")
    ep_list = div_element.find_elements_by_tag_name("a")
    ep_list.reverse()
    links = []
    for link in ep_list:
        links.append((link.text, link.get_attribute("href")))
    return links


def download_server_1(driver, url_list):
    if not len(url_list):
        return
    global TIMEOUT, ANIME_NAME
    try:
        os.mkdir(ANIME_NAME)
        print("Created directory:", ANIME_NAME) 
        directory = ANIME_NAME + "/"
    except:
        try:
            dir_name = ANIME_NAME + " " + str(int(random.random()*10e9))
            os.mkdir(dir_name)
            print("Created directory:", dir_name) 
            directory = dir_name + "/"
        except:
            directory = ""
    for URL in url_list:
        try:
            driver.get(URL[1])
        except:
            print("Error 1 Connection Error! Cannot download", URL[0])
        else:
            driver.implicitly_wait(TIMEOUT)
            video_element = driver.find_element_by_class_name("cvideo")
            frame = video_element.find_element_by_tag_name("iframe")
            newlink = frame.get_attribute("src")
            try:
                driver.get(newlink)
            except:
                print("Error 2 Connection Error! Cannot download", URL[0])
            else:
                try:
                    driver.find_element_by_tag_name("video").click()
                except:
                    driver.find_element_by_class_name("jw-icon-display").click()
                video = driver.find_element_by_tag_name("video")
                link = video.get_attribute("src")
                print("Downloading", URL[0])
                try:
                    filename = download_file(link, URL[0], directory)
                except:
                    print("Error 3 Connection Error! Cannot download", URL[0])
                else:
                    print(filename, "downloaded")
    return
    

def download_server_2(driver, url_list):
    if not len(url_list):
        return
    global ANIME_NAME
    try:
        os.mkdir(ANIME_NAME)
        print("Created directory:", ANIME_NAME) 
        directory = ANIME_NAME + "/"
    except:
        try:
            dir_name = ANIME_NAME + " " + str(int(random.random()*10e9))
            os.mkdir(dir_name)
            print("Created directory:", dir_name) 
            directory = dir_name + "/"
        except:
            directory = ""
    for URL in url_list:
        try:
            driver.get(URL[1])
        except:
            print("Connection Error! Cannot download", URL[0])
        else:
            div_element = driver.find_element_by_class_name("pcat-jwplayer")
            frame = div_element.find_element_by_tag_name("iframe")
            newlink = frame.get_attribute("src")
            try:
                driver.get(newlink)
            except:
                print("Connection Error! Cannot download", URL[0])
            else:
                video_tag = driver.find_element_by_id("video-js")
                source = video_tag.find_element_by_tag_name("source")
                link = source.get_attribute("src")
                print("Downloading", URL[0])
                try:
                    filename = download_file(link, URL[0], directory)
                except:
                    print("Connection Error! Cannot download", URL[0])
                else:
                    print(filename, "downloaded")
    return    
        

def user_input():
    global ANIME_NAME
    ANIME_NAME = input("\nWhich anime are you looking for?: ")
    return


def user_choice(ep_list):
    for i, ep in enumerate(ep_list, start=1):
        print(str(i)+".", ep[0])
    if len(ep_list):
        print("\n1. Download all\n2. Download selected ones\n3. Download in range\n4. Exit")
        choice = int(input("\nEnter your choice: "))
        if choice == 1:
            return ep_list
        elif choice == 2:
            selected = list(map(int, input("\nEnter episode numbers separated by ',': ").split(',')))
            new_list = []
            for i in selected:
                new_list.append(ep_list[i-1])
            return new_list
        elif choice == 3:
            start = int(input("Starting episode number: "))
            end = int(input("Ending episode number: "))
            return ep_list[start-1:end]
        else:
            return []
    return []        


if __name__ == '__main__':
    driver = start_driver()
    user_input()
    print("\nFetching search results for",  ANIME_NAME + "...\n")
    links_1 = search_server_1(driver)
    links_2 = search_server_2(driver)
    links = links_1 + links_2
    for i, link in enumerate(links, start=1):
        print(str(i)+".", link[0])
    print(str(len(links) + 1)+".", "Exit")
    if len(links):
        choice = int(input("\nEnter your choice: "))
        if choice not in range(1, len(links)+1):
            driver.close()
            exit()
        ANIME_NAME = links[choice-1][0]
        print("\nFetching episode list results for",  ANIME_NAME + "...\n")
        if choice <= len(links_1):
            ep_list = episode_list_1(driver, links[choice-1][1])
            download_list = user_choice(ep_list)
            if len(download_list):
                print("\nSit back and wait for the download to complete.\n")
            download_server_1(driver, download_list)
        else:
            ep_list = episode_list_2(driver, links[choice-1][1])
            download_list = user_choice(ep_list)
            if len(download_list):
                print("\nSit back and wait for the download to complete.\n")
            download_server_2(driver, download_list)
    driver.close()
