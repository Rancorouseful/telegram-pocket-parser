import requests
import os
import aiohttp
from bs4 import BeautifulSoup

class get():
    
    @staticmethod
    def page(url):
        response = requests.get(url)

        if response.status_code == 200:
            return response.content
        else:
            return False
    
    @staticmethod
    def tag(content, tag):
        soup = BeautifulSoup(content, "html.parser")
        tags = soup.find_all(tag)

        return tags

    @staticmethod
    # Функция для получения HTML-кода сайта и отправки его пользователю в Telegram
    async def html(chat_id, url):
        try:
            # Путь к директории пользователя
            user_dir = f'user_data/{chat_id}'

            # Создаем директорию, если она не существует
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html = await response.text()

            # Сохраняем HTML-код в файл .txt в директории пользователя
            html_file_path = os.path.join(user_dir, 'website.txt')
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html)
            
            return(html_file_path)
            
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    # Функция для получения HTML-кода сайта и отправки его пользователю в Telegram
    async def styles(chat_id, url):
        try:
            # Путь к директории пользователя
            user_dir = f'user_data/{chat_id}'

            # Создаем директорию, если она не существует
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            css_links = []

            # Найдите все ссылки на CSS файлы (может потребоваться настроить селектор)
            for link in soup.find_all('link', rel='stylesheet'):
                css_url = link.get('href')
                if css_url:
                    if css_url.startswith('/'):
                        css_links.append(f"{url}{css_url}")
                    else:
                        css_links.append(css_url)
            
            # for i in range(0, len(css_links)):
            #     if css_links[i].startswith('/'):
            #         css_links[i] = f"{url}{link}"

            return(css_links)
            
        except Exception as e:
            print(e)
            return False





