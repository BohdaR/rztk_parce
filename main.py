import json
import lxml
import requests
import csv
from bs4 import BeautifulSoup


SEARCH_URL = 'https://weather.com/uk-UA/weather/tenday/l/fbd9abfe47326bb176f53692f407ed025fc2916883a34ff763c16c8ba7b25f75'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36',

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

ORDER_BY = '&sp=CAM%253D'
FILE_NAME = 'sample.xlsx'


def main():
    content = []
    # for el in SEARCH_QUERY:
    #     print(SEARCH_URL + el.replace(' ', '+') + ORDER_BY)
    url = 'https://hard.rozetka.com.ua/ua/videocards/c80087/'
    html1 = requests.get(url, headers=HEADERS)
    soup1 = BeautifulSoup(html1.content, 'lxml')
    product_url = soup1.find_all('a', class_='goods-tile__picture ng-star-inserted')
    count = 1
    for el in product_url:
        html = requests.get(el.get('href'), headers=HEADERS)
        soup = BeautifulSoup(html.content, 'lxml')
        print(f'Парсинг {count} товару')
        count += 1
        try:
            prise = soup.find('p', class_='product-prices__big').text.replace('₴', ' грн').replace('\xa0', ' ')
        except:
            prise = 'Ціна не вказана'
        content.append({
            'title' : soup.find('h1', class_='product__title').text.strip(),
            'description' : str(soup.find('div', class_='product-about__description-content').text),
            'img_url' : soup.find('img', class_='picture-container__picture').get('src'),
            'price' : prise,
        })

    with open('product.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['title',
             'description',
             'img_url',
             'price'
             ])

        for item in content:
            writer.writerow([
                item['title'],
                item['description'],
                item['img_url'],
                item['price']
            ])

    with open('product.json', 'w', encoding='utf-8') as jfile:
        json.dump(content, jfile, indent=4, ensure_ascii=False)
    print(content)

if __name__ == '__main__':
    main()