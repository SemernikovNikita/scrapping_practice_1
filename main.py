from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

class parser():
    def __init__(self,url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.quotes = []

    def parse_page(self,page):
        url = f"{self.url}/catalogue/page-{page}.html"
        responce = self.session.get(url)

        if responce.status_code != 200:
            print("Страница не загрузилась")
            exit()

        soup = bs(responce.text,'html.parser')

        items = soup.find_all('article', class_='product_pod')
        for item in items:

            name = item.find('h3').find('a')
            if name:
                name = name.get_text(strip=True)
            else:
                print("Имя не найдено")

            price = item.find('p', class_='price_color')
            if price:
                price = price.get_text(strip=True).replace('Â','').replace('£','')
            else:
                print("Цена не найдена")

            self.quotes.append({'name': name, 'price': price})

        time.sleep(1)

    def run(self,max_pages=50):
        for page in range(1,max_pages + 1):
            self.parse_page(page)
        return self.quotes

def main():
    pars = parser('http://books.toscrape.com/')
    data = pars.run()
    df = pd.DataFrame(data)
    df.to_csv('quotes.csv',index=False,encoding='utf-8-sig')
    print(df.head())

if __name__ == '__main__':
    main()

