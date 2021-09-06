"""
Some python practice. Scraping information from google search enginge
tags: python, BeautifulSoup, regex, pylint
"""
import csv
import urllib.request
import re
from googlesearch import search
from bs4 import BeautifulSoup


def save_total_number(number,word):
    """Saves total search number with specified word, in text file"""
    with open('result.txt','a',encoding="utf-8") as file:
        file.write(str(number)+" "+word+"\n")


def scrap_number(my_query_word):
    """Function prepares google search request, and scraps total amount of results via regex"""
    url = 'https://google.com/search?q='
    url = url +my_query_word
    # Perform the request
    request = urllib.request.Request(url)
    # Set a normal User Agent header, otherwise Google will block the request.
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/'
                       '537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()
    # Read the repsonse as a utf-8 string
    html = raw_response.decode("utf-8")

    soup = BeautifulSoup(html, 'html.parser')
    string_with_number = soup.find('div', {'id': 'result-stats'}).text
    number = string_with_number.replace(' ', '')
    result = re.search(r'\d+', number).group()
    result = int(result)
    return result


def write_to_csv(word_data="link missing?"):
    """Saves given string(link) to *.csv file"""
    with open('csvResults.csv', mode='a',encoding="utf-8") as csv_file:
        fieldnames = ['link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'link': word_data})


def get_link_selected(query_word,how_many=10):
    """Function tries to get first {how_many} results from search from googlesearch package
     it is not exact scrapping from web page"""
    query = "site:https://www.searchenginejournal.com/ "+ query_word
    for j in search(query, num=10, stop=how_many, pause=0.1):
        write_to_csv(j)


def read_file():
    """Read keywords from given keywords.txt file, and run program for each word
    Main loop of program"""
    with open('keywords.txt', 'r',encoding="utf-8") as file:
        # reading each line
        for line in file:
            # reading each word
            for word in line.split():
                #for each word...
                get_link_selected(query_word=word)
                #save number of pages
                save_total_number(scrap_number(word),word)


if __name__ == '__main__':
    read_file()
