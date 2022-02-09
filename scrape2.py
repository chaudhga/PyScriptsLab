from lxml import html
import requests
import re
import urllib.request
import shutil

print('starting...')
url = "https://www.gutenberg.org/ebooks/1727"
mainWebsite = "https://www.gutenberg.org/"

page = requests.get(url)
tree = html.fromstring(page.content)
print(page.content)
section = tree.xpath('//a[@charset="utf-8"]/text()')

if 'Plain Text UTF-8' in section:
    print("inside section")
    r = requests.get(url, allow_redirects=True)
    links = re.findall('a href="(.*txt)"', r.text)
    print(len(links))
    for lnk in links:
        fileurl = mainWebsite+lnk
        with urllib.request.urlopen(fileurl) as response, open('trainingtext.txt', 'wb') as out_file:
            print("writing to {file_name}...")
            shutil.copyfileobj(response, out_file)
            break