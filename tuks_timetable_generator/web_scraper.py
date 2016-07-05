import urllib2
from bs4 import BeautifulSoup

from . import configuration

def download_url(url):
    return urllib2.urlopen(url)

def download_and_parse_url(url):
    html_response = download_url(url)
    soup = BeautifulSoup(html_response, 'html.parser')
    data_table = soup.find(id="myTable")
    table_body = data_table.find("tbody")
    table_rows = table_body.find_all("tr")

    for row in table_rows:
        print(row)