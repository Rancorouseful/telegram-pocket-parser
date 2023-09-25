import requests
from bs4 import BeautifulSoup

class get():
    
    @staticmethod
    def page(url):
        response = requests.get(url)

        if response.status_code == 200:
            return response.content
        else:
            print(f"Request error: {response.status_code}")
    
    def tag(content, tag):
        soup = BeautifulSoup(content, "html.parser")
        tags = soup.find_all(tag)

        return tags


