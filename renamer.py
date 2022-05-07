
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import Levenshtein as lev

def scroll_till_end(driver, pause_time=1):
    # Get scroll height
    """last_height = driver.execute_script("return document.body.scrollHeight")
    this doesn't work due to floating web elements on youtube
    """
    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    while True:
        print("\n*********Scrolling, Please Wait.*********\n")
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0,document.documentElement.scrollHeight);")
        # Wait to load page
        time.sleep(pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("\n*********Reached end of the page*************\n")


def fetch_titles(driver, url, printList=False):
    print("\n*********Loading Page*********\n")
    driver.get(url)
    print("\n*********Page Loaded Successfully*********\n")
    elem = driver.find_element(By.TAG_NAME, 'html')
    scroll_till_end(driver, 1)
    main_a = driver.find_elements(By.ID,"video-title")

    titles_list = []
    for a in main_a:
        titles_list.append(a.get_attribute("title"))
    driver.close()

    if printList:
        print("\n\n*********Fetched Title of each Video from Playlist*********\n")
        for idx, i in enumerate(titles_list, start=1):
            print(idx, ":", i)

    return titles_list

def find(title_list, key):
    maxSimilarity = -1
    maxSimilarityIdx = -1
    for idx, title in enumerate(titles_list):
        ratio = lev.ratio(title.strip().lower(), key.strip().lower())
        if ratio > maxSimilarity:
            maxSimilarity = ratio
            maxSimilarityIdx = idx
    return maxSimilarityIdx

def renameFiles(folder, title_list):
    for filename in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, filename)):
            # check if files is present in fetched titles_list
            # if present, then add suitable index no like 1,2,3 as prefix
            # Example:- 1_FileName.mp4 or 2_FileName.mkv
            idx = find(title_list, filename)
            if idx != -1:
                dst = str(idx+1) + "_" + filename
                src = f"{folder}/{filename}"
                dst = f"{folder}/{dst}"
                os.rename(src, dst)
    print("\n\n*********Renaming Complete*********\n")


if __name__ == "__main__":
    # Getting driver object for chrome browser
    driver = webdriver.Chrome()
    print("\n*********Chrome Driver Successfully loaded.*********\n")

    # URL of Playlist
    url = "https://www.youtube.com/playlist?list=PLUcsbZa0qzu3yNzzAxgvSgRobdUUJvz7p"

    # fetched title of each video from playlist sequentially
    titles_list = fetch_titles(driver, url)

    # folder where downloaded files of playlist is saved
    folder_path = "DownloadedVideos"

    if titles_list:
        renameFiles(folder_path, titles_list)
    else:
        print("Titles are not fetched")
