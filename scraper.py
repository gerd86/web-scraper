import requests
import string
import os
import re

from bs4 import BeautifulSoup


def scrape_article(n_pages, article_category):
    path = os.getcwd()
    regex = re.compile(".*body.*")
    for x in range(1, n_pages + 1):
        r = requests.get(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={x}')
        soup = BeautifulSoup(r.content, 'html.parser')
        article_titles = soup.find_all('article')
        a_cat = article_category.title()
        new_directory = 'Page_' + str(x)
        os.mkdir(new_directory)
        new_path = f'{path}/{new_directory}'
        os.chdir(new_path)
        for i in article_titles:
            a_type = i.find('span', class_='c-meta__type')
            if a_type.text == a_cat:
                nature_url = 'https://www.nature.com'
                a_link = i.find('a')
                response = requests.get(nature_url + a_link['href'])
                a_soup = BeautifulSoup(response.content, 'html.parser')
                article_title = a_soup.find('h1').text.strip().translate(str.maketrans('', '', string.punctuation)
                                                                         ).replace(" ", "_")
                article_body = a_soup.find('div', attrs={'class': regex}).text.strip().encode('utf-8')
                with open(f'{article_title}.txt', 'wb') as file:
                    file.write(article_body)
                    print('\nContent saved.')
        os.chdir(path)


input_one = int(input())
input_two = input()

scrape_article(input_one, input_two)
