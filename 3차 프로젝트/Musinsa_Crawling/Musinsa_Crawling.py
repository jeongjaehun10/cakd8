# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pyautogui
import random as r
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process


# def close_pop_up():
#     image_path = 'C:/Users/sel20/OneDrive/Desktop/스크린샷/액스.png'
#     try:
#             # 이미지를 화면에서 찾기
#         location = pyautogui.locateOnScreen(image_path)
#         print(location)
#         pyautogui.click(location)
#         if location is not None:
#             pass
#     except:
#         pass
#     time.sleep(1)
def get_href():
    urls = []
    for i in range(11,20):
        url = 'https://www.musinsa.com/ranking/best?period=now&age=ALL&mainCategory=&subCategory=&leafCategory=&price=&golf=false&kids=false&newProduct=false&exclusive=false&discount=false&soldOut=false&page='+str(i)+'&viewType=small&priceMin=&priceMax='
        chrome_driver_path = 'C:/Users/sel20/Downloads/chromedriver_win32/chromedriver.exe'
        # Create a Service object using the chromedriver path
        service = Service(executable_path=chrome_driver_path)
        service.start()
        # Pass the Service object as an argument when creating an instance of the webdriver.Chrome class
        driver = webdriver.Chrome(service=service)
        # Load the page and start scraping
        driver.get(url)
        for i in range(1,90):
            e = driver.find_element(By.XPATH,'//*[@id="goodsRankList"]/li['+str(i)+']/div[3]/div[1]/a')
            urls.append(e.get_attribute('href'))
    return urls

# Press the green button in the gutter to run the script.
def crawling(url):
    url = url
        # Set the path to your downloaded chromedriver executable
    chrome_driver_path = 'C:/Users/sel20/Downloads/chromedriver_win32/chromedriver.exe'
        # Create a Service object using the chromedriver path
    service = Service(executable_path=chrome_driver_path)
    service.start()
        # Pass the Service object as an argument when creating an instance of the webdriver.Chrome class
    driver = webdriver.Chrome(service=service)
        # Load the page and start scraping
    driver.get(url)
    text = []

    try:
        t = driver.find_element(By.XPATH, '//*[@id="page_product_detail"]/div[3]/div[3]/span')
        b = driver.find_element(By.XPATH, '//*[@id="page_product_detail"]/div[3]/div[3]/div[1]/p/a[1]')
        title = t.text
        board = b.text
        p = driver.find_element(By.XPATH,'//*[@id="goods_price"]')
        price = p.text
        for i in range(1, 11):
            # Scrape the review text
            e = driver.find_element(By.XPATH, '//*[@id="reviewListFragment"]/div[' + str(i) + ']/div[4]/div[1]')
            text.append(e.text)

        return {'title':title,'url': url,'content':'\t'.join(text),'board' : board,'price':price}
    except:
        return {'title': '','url':url,'content':'','board' : board,'price':price}


if __name__=="__main__":
    text =[]
    numbers = []
    urls = get_href()
    for url in urls:
        text.append(crawling(url))

    with open('C:/Users//admin/PycharmProjects/pythonProject/data/data11-20.json','w') as f:
        json.dump(text,f)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/