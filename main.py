import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json


class AvitoParser:
    def __init__(self, item, town, filename, count=0):
        self.url = f'https://www.avito.ru/{town}?q={"+".join(item.split())}'
        self.filename = filename
        self.count = count
        self.driver = uc.Chrome(version_main=116)
        self.data = []

    def __set_up(self):
        self.driver.get(self.url)

    def __paginate(self):
        while self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]') and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]').click()
            self.count -= 1


    def __parse_page(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')

        for item in items:
            name = item.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
            description = item.find_element(By.CSS_SELECTOR, '[class*="description"]').text
            url = item.find_element(By.CSS_SELECTOR, '[itemprop="url"]').get_attribute('href')
            price = item.find_element(By.CSS_SELECTOR, '[itemprop="price"]').get_attribute('content')
            self.data.append({name:name, description:description, url:url, price:price})

    def __save_info(self):
        with open(f'{self.filename}.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)


    def parse(self):
        try:
            self.__set_up()
            self.__paginate()
        except Exception as e:
            print(e)
        self.__save_info()


if __name__ == '__main__':
    AvitoParser('nike air jordan 1', 'murmansk', 'test1', 50).parse()
