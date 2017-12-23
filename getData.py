#! python3
# get_data.py

import webbrowser, requests, bs4

def get_data(keyword):
    search = keyword
    search = search.lower()
    search = search.split(" ")

    # Search Amazon
    a = "+"
    search_amazon = a.join(search)
    print(search_amazon)
    with open('amazon.html', 'wb') as amazon:
        response = requests.get('https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=nike' + ' '+search_amazon, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
        }, stream=True)
        response.raise_for_status()
        if not response.ok:
            print("There was an error")
        for block in response.iter_content(1024):
            amazon.write(block)

    # Search Nike
    i = "%20"
    search_nike = i.join(search)
    print(search_nike)
    with open('nike.html', 'wb') as nike:
        response = requests.get('http://store.nike.com/us/en_us/pw/n/1j7?sl=' + ' '+search_nike, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
        }, stream=True)
        response.raise_for_status()
        if not response.ok:
            print("There was an error")
        for block in response.iter_content(1024):
            nike.write(block)

    # Close files
    amazon.close()
    nike.close()
