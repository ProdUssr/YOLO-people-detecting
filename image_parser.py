from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import time
import os


def parse_and_download_images(url, limit=40, save_folder="RSK"):
    """
    Парсит указанную веб-страницу, находит изображения 
    и загружает нужное количество в выбранную папку.
    """

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    print("[INFO] Загружаем сайт")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)
    
    print("[INFO] Переходим в нужный раздел")
    driver.find_element("xpath", "//a[@href='https://fc-rsk.ru/press-center']").click()
    time.sleep(3)

    driver.find_element("xpath", "//a[@href='#!/tfeeds/291301282185/c/#Строительный контроль']").click()
    time.sleep(3)
    
    print("[INFO] Собираем ссылки на фотографии")
    img_count = 0
    while img_count < limit:
        # получаем html код страницы
        page_source = driver.page_source
        
        # парсим фотографии новостей
        soup = BeautifulSoup(page_source, 'html.parser')
        image_elements = soup.find_all('div', class_='t-feed__post-bgimg')
        
        img_count = len(image_elements)
        
        # разворачиваем страницу, так как по умолчанию доступны не все новости
        driver.find_element(by=By.CLASS_NAME, value="js-feed-btn-show-more").click()
        time.sleep(3) 
        
    driver.quit()
    
    print("[INFO] Скачиваем фотографии")
    for i, element in enumerate(image_elements):
        
        if i < limit:
            img_url = element.get('data-original')
                
            # Отправляем запрос на загрузку изображения
            img_response = requests.get(img_url, timeout=15)
            img_response.raise_for_status()
                
            # Сохраняем файл
            filename = os.path.join(save_folder, f"image_{i}.jpg")
            with open(filename, 'wb') as f:
                f.write(img_response.content)

        else:
            break
    
    
if __name__ == "__main__":
    url = "https://fc-rsk.ru"
    parse_and_download_images(url, limit=40, save_folder="RSK")