import datetime
import requests
import bs4

from pprint import pprint

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Ваш код
# <дата> - <заголовок> - <ссылка>
HEADERS = {'Cookie': 'hl=ru; fl=ru; visited_articles=327294:193380:323202:69577:321510:340460:346344:470285:488054:547084; feature_streaming_comments=true; habr_web_home=ARTICLES_LIST_ALL',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'cross-site',
           'Cache-Control': 'max-age=0',
           'If-None-Match': 'W/"36604-9g1LpxNBE6Bhzwn9cBeQqAkJYaQ"',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
           }

if __name__ == '__main__':
    response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
    response.raise_for_status()
    text = response.text
    # с помощью API невозможно достать ссылку на статью
    # data = response.json()
    # pprint(data)
    # pprint(data['articles']['articleRefs'])
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        text_preview = article.find('div', class_='tm-article-body tm-article-snippet__lead').text
        for elem in KEYWORDS:
            flag_find = text_preview.find(elem)
            if flag_find > 0:
                published = article.find('span', class_='tm-article-snippet__datetime-published')
                data_published = published.time['title'][:10]
                title = article.find('a', class_='tm-article-snippet__title-link')
                href = title['href']
                url = 'https://habr.com' + href
                span_title = title.find('span').text
                # print(text_preview)
                print(f'{data_published} - {span_title} - {url}')
                break
