import re
import requests
from bs4 import BeautifulSoup


class Telegram:
    def __init__(self):
        self.author = '@PaketPKSoftware'
        
    def extractTelegramDomains(self, text):
        pattern = r'(?:@|t\.me\/|telegram\.me\/|tg:\/\/)([A-Za-z0-9_.]{5,32})|([A-Za-z0-9_.]{5,32}\.t\.me)'    
        matches = re.findall(pattern, text)
        unique_matches = [match[0] if match[0] else match[1] for match in matches]
        return list(set(unique_matches))

    def _TgUserInfoFromHtml(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('meta', {'property': 'og:title'})['content']
        image_url = soup.find('meta', {'property': 'og:image'})['content']
        description = soup.find('meta', {'property': 'og:description'})['content']
        tg_url = soup.find('meta', {'property': 'al:android:url'})['content']
        return {'name':name, 'image':image_url, 'description':description, 'tg':tg_url}

    def _TgChannelInfoFromHtml(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('meta', {'property': 'og:title'}).get('content')
        image_url = soup.find('meta', {'property': 'og:image'}).get('content')
        description = soup.find('meta', {'property': 'og:description'}).get('content')
        tg_url = soup.find('meta', {'property': 'al:android:url'}).get('content')
        subsc = soup.find('div', {'class': 'tgme_page_extra'}).text.strip()
        return {'name':name, 'image':image_url, 'description':description, 'tg':tg_url, 'subscribers': subsc}
    
    def _TgChatInfoFromHtml(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('meta', {'property': 'og:title'}).get('content')
        image_url = soup.find('meta', {'property': 'og:image'}).get('content')
        description = soup.find('meta', {'property': 'og:description'}).get('content')
        tg_url = soup.find('meta', {'property': 'al:android:url'}).get('content')
        subsc = soup.find('div', {'class': 'tgme_page_extra'}).text.strip()
        return {'name':name, 'image':image_url, 'description':description, 'tg':tg_url, 'users': subsc}

    def TelegramUsername(self, tag: str):
        tag = tag.replace('@', '')
        html = requests.get(f'https://t.me/{tag}').content
        return self._TgUserInfoFromHtml(html)

    def TelegramChannel(self, tag: str):
        tag = tag.replace('@', '')
        html = requests.get(f'https://t.me/{tag}').content
        return self._TgChannelInfoFromHtml(html)
    
    def TelegramChat(self, tag: str):
        tag = tag.replace('@', '')
        html = requests.get(f'https://t.me/{tag}').content
        return self._TgChannelInfoFromHtml(html)
    
    def TelegramCParser(self, chtag):
        chtag = chtag.replace('@', '')
        chtag = 'https://t.me/s/{}'.format(chtag)
        msgs = []
        response = requests.get(chtag)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            messages = soup.find_all('div', class_='tgme_widget_message')
            for message in messages:
                message_text = message.find('div', class_='tgme_widget_message_text')
                if message_text:
                    msgs.append(message_text.text)

            return msgs
        else:
            return msgs
        
    def AutoScan(self, tag):
        ...


def SearchUserBox(query, token):
    url = "https://api.usersbox.ru/v1/search"
    headers = {"Authorization": token}
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)
    return response.json()



def SearchLeak(Term, token):
    try:
        datar = {"token": token, "request": Term, "limit": 100, "lang": "ru"}
        url = 'https://server.leakosint.com/'
        response = requests.post(url, json=datar)
        data =  response.json()
        for source, items in data["List"].items():
            if source == "No results found":
                pass
            else:
                print("\n[data]")
                for item in items["Data"]:
                    for key, value in item.items():
                        print(f"├ {key}: {value}")
                print(f"╰ Data base: {source}")
    except:pass

def ipLookup(ip_address):
    api_url = f'http://ipinfo.io/{ip_address}/json'

    try:
        response = requests.get(api_url)
        data = response.json()

        return data
    except:
        return {}
    
def dbsearch(db, value):
    try:
        with open(db, "r", encoding="utf-8") as f:
            for line in f:
                Fline = line
                break
            
        with open(db, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    if value in line:
                        print("\n[data]")
                        fdata = line.replace(",",";").replace("|",";").replace('"',"").replace('NULL',"").replace(":",";").strip().split(";")
                        sdata = Fline.replace(",",";").replace("|",";").replace('"',"").replace('NULL',"").replace(":",";").strip().split(";")

                        for i in range(len(fdata)):
                            if len(fdata[i]) < 80 and fdata[i]:
                                betadata = f"├ {sdata[i].replace('_', ' ')}: {fdata[i]}"
                                print(f"{betadata}")
                        print("╰ Data base: "+db)
                except:print("╰ Data base: "+db)
    except BaseException as e: print('[ + ] Error: '+e)

def PhoneNumber(phone_number:str):
    phone_number=phone_number.replace('+', '').replace('-', '')
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        http = requests.get(f"https://free-lookup.net/{phone_number}", headers=headers)
        html = BeautifulSoup(http.text, "html.parser")
        infos = html.findChild("ul", {"class": "report-summary__list"}).findAll("div")
        return {k.text.strip(): infos[i + 1].text.strip() if infos[i + 1].text.strip() else "No information" for i, k in enumerate(infos) if not i % 2}
    except:
        return {}
    



