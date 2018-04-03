import time
import requests
import soup as soup
from bs4 import BeautifulSoup
import re

BASE_URL_INFO = 'http://seasonvar.ru/serialinfo/'
BASE_URL = 'http://seasonvar.ru/'


def get_html_soup(html):
    r = requests.get(html, headers=headers)
    data_fromhtml = r.content
    soup = BeautifulSoup(data_fromhtml, "html.parser")
    return soup


def delete_studio(str):
    last_episodes = str.split()
    for word in last_episodes:
        if word[0] + word[-1] == '()':
            last_episodes.remove(word)

    last_episodes = " ".join(last_episodes)
    return last_episodes


def serial_lastepisod(tag):
    last_episod_block = get_serial_url(tag).find("li", {"class": "act"})
    last_episod = last_episod_block.find('span')
    return (delete_studio(last_episod.text[1:-1]))


def get_info(tag):
    reference = tag.get('data-id')
    info = []
    info_source = get_html_soup(BASE_URL_INFO+reference+'/')

    SerialText = info_source.find(("div", {"class": "serial-w"}))
    info.append({'name': tag.text,
                 'last season': serial_lastseason(tag),
                 'last episod': serial_lastepisod(tag),
                 'photo': info_source.find('img').get('src'),
                 'text_info': SerialText.find('p').text,
                 'ratings': [rating.text for rating in SerialText.find_all('div')[1:]]})
    return info


def has_class_but_no_class(tag):
    return not tag.has_attr('class')


def get_serial_url(tag):
    reference = tag.get('href')
    info_source = get_html_soup(BASE_URL + reference)
    return info_source


def serial_lastseason(tag):
    header = get_serial_url(tag).find("h1", {"class": "pgs-sinfo-title"}).text
    try:
        if type((int)(header.split()[-3])) == int:
            return(" ".join(header.split()[-3:-1]))
    except:
        return('1 сезон')


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    seasonvar = get_html_soup('http://seasonvar.ru')
    Variable1 = seasonvar.find("div", {"class": "lside-serial"})
    Variable2 = Variable1.find_all('a')
    for i in Variable2[:1]:
        print(get_info(i))
    print(delete_studio("02.04.2018 16 серия (NewStudio) из 22"))
