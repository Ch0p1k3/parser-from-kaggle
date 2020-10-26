from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import time
import json
from pathlib import Path
import urllib

# B-) sdgffsdfsdfdsfsdfsd

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory": "C:\\Users\\Chop\\Desktop\\DownloadedJSON"})
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options)
sel = Selector(text=driver.page_source)
urls = []
url = 'https://www.kaggle.com/c/halite/leaderboard'
    

def enter():
    global driver, sel
    driver.get(url)
    sel = Selector(text=driver.page_source)


def close():
    global driver
    driver.close()


def collect_url():
    global urls
    urls = sel.xpath("//*[starts-with(@class, 'competition-leaderboard__td-entries-watch')]//a/@href").getall()


def downloading_files(computer_name):
    global driver, sel
    id_f = 0
    for link in urls:
        full_link = url + link
        driver.get(full_link)
        time.sleep(2)
        # div//div[@id = 'site-content']/div[3]//ul//li//a
        scr1 = driver.find_element_by_xpath("//main//div[@id='site-content']//div[@class='mdc-dialog__content']")
        last_height = driver.execute_script("return arguments[0].scrollHeight", scr1)
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            time.sleep(0.5)
            new_height = driver.execute_script("return arguments[0].scrollHeight", scr1)
            if new_height == last_height:
                break
            last_height = new_height
        
        sel = Selector(text=driver.page_source)
        replays = sel.xpath("//main//div[@id='site-content']//div[@class='mdc-dialog__content']//ul//li//a/@href").getall()
        for replay in replays:
            driver.get('https://www.kaggle.com' + replay)
            time.sleep(2)
            sel = Selector(text=driver.page_source)
            l = sel.xpath("//main//div[@class='mdc-dialog__container']//a//@href").getall()[0]
            jsonfile = urllib.request.urlopen('https://www.kaggle.com' + l)
            with open(f'C:\\Users\\{computer_name}\\Desktop\\DownloadedJSON\\file_{id_f}.json', 'wb') as output:
                output.write(jsonfile.read())
            print(id_f)
            id_f += 1
            


def parse(computer_name):
    enter()
    collect_url()
    downloading_files(computer_name)
    close()


def main():
    parse('Chop')
    


if __name__ == "__main__":
    main()

    

    
