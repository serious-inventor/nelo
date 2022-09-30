import re
import json
import base64
import requests
from bs4 import BeautifulSoup

def search(param):
    headers = {
        "Referer" : "https://m.manganelo.com/wwww",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    r = requests.post(url="https://m.manganelo.com/getstorysearchjson", data={"searchword": param.replace(' ', '_')}, headers=headers)

    if r.status_code == 200:
        result = re.sub(r'<span style=\\"color: #FF530D;font-weight: bold;\\">|<\\/span>', '', r.text)
        result = json.loads(result)
        return result
    return None

def chap_urls(link):
    r = requests.get(link)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        chap_list = soup.find_all('a', class_='chapter-name text-nowrap')[::-1]
        return json.dumps({a['href'].split('/')[-1].split('-')[-1] : a['href'] for a in chap_list})
    return None

def chap_imgs(chap_link):
    r = requests.get(chap_link)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        imgs = soup.find_all('img', class_='reader-content')
        return json.dumps({img['src'].split('/')[-1] : img['src'] for img in imgs})
    return None

def chapter(chap_link):
    d = dict()
    imgs = json.loads(chap_imgs(chap_link))
    for i in imgs:
        r = requests.get(imgs[i], headers={"Referer":"https://chapmanganelo.com/"})
        if r.status_code != 200:
            return None
        d[i] = base64.b64encode(r.content).decode('utf-8')
    return json.dumps(d)

def status(link):
    r = requests.get(link)
    d = dict()
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        a = soup.find_all('div', class_='panel-story-info')
        d['status'] = a[0].find_all('tr')[2].text.strip().split('\n')[-1]
        a = soup.find_all('div', class_='story-info-right-extent')
        d['updated'] = a[0].find_all('p')[0].text.split('Updated :')[-1]
        return json.dumps(d)
    return None


