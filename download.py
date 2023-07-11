import csv
import os
import requests




import traceback

crypto_directory = 'podatki'

def download_url_to_string(url):
    try:
        page_content = requests.get(url)
        if page_content.status_code == 200:
            return page_content.text
        else:
            raise ValueError(f"Čudna koda: {page_content.status_code}")
    except Exception:
        print(f"Prišlo je do spodnje napake:\n{traceback.format_exc()}")

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    html_strani = download_url_to_string(page)
    save_string_to_file(html_strani, directory, filename)

def top_url(index):
    return 'https://coinmarketcap.com/?page={}'.format(index)
def top_name(index):
    return 'crypto{}'.format(index)

for i in range(1,51):
    save_frontpage(top_url(i), crypto_directory, top_name(i)) 





