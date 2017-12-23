#! python3
# parse_html.py

import requests, sys, webbrowser, bs4
import json
import os
from flask import Flask, send_file, make_response, request, render_template, url_for, json


def image_url(filename, type = 'amazon'):
	myfile = open(filename)
	soup_object = bs4.BeautifulSoup(myfile.read(), 'lxml')

	if type == 'amazon':
		divtag = soup_object.findAll('div', \
			attrs={'class':'a-column a-span12 a-text-center s-position-relative'})
	elif type == 'nike':
		divtag = soup_object.findAll('div', \
			attrs={'class':'grid-item-image'})
	else:
		print " Please select either 'nike' or 'amazon' as the type. "

	links = [divtag[i].findAll('img')[0]['src']\
	 for i in range(len(divtag))]

	return links


def parse_data():
    soupAmazon = bs4.BeautifulSoup(open("amazon.html"), "lxml")
    rows = soupAmazon.select('div.s-item-container')

    # Initialize lists
    matched_rows = []
    prices = []
    ratings = []
    descs = []

    for i in range(len(rows)):
        temp_string = str(rows[i])
        if "sx-price-whole" in temp_string:
            matched_rows.append(rows[i])

    for card in matched_rows:
        price = card.find_all("span", "sx-price-whole")
        rating = card.find_all("a", "a-popover-trigger")
        desc_h2 = card.find_all("h2",{"data-attribute":True})
        for des in desc_h2:
            desc = des["data-attribute"]

        prices.append(str(price))
        ratings.append(str(rating))
        descs.append(str(desc))

    char1 = '>'
    char2 = '</span>,'
    char3 = ', <span class="sx-price-whole">'
    char4 = '</span>]'
    lower = ''
    higher = ''
    rate = ''
    amazon_price_string = []
    amazon_rating_string = []

    for i in prices:
       if len(i) > 60:
        lower = i.partition(char1)[-1].rpartition(char2)[0]
        higher = i.partition(char3)[-1].rpartition(char4)[0]
        amazon_price_string.append(str("$"+lower+"-"+"$"+higher))
       else:
        individual = i.partition(">")[-1].rpartition("<")[0]
        amazon_price_string.append(str("$"+individual))


    for j in ratings:
        rate = j.partition('<span class="a-icon-alt">')[-1].rpartition('</span></i><i class="a-icon a-icon-popover">')[0]
        amazon_rating_string.append(rate)

    for i in range(len(amazon_rating_string)):
        if amazon_rating_string[i] == '':
            amazon_rating_string[i] = "No ratings."


    list_images_amazon = image_url("amazon.html", type = 'amazon')

	list_images_nike = image_url("nike.html", type = 'nike')


    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/js", "amazon-output.json")

    with open(json_url, "w") as outfile:
        outfile.write("{ \"items\": [ ")
        for i in range(len(prices)):
            json.dump({'name': descs[i], 'price': amazon_price_string[i], 'rating': amazon_rating_string[i], 'image': list_images_amazon[i] }, outfile, indent=4)
            if i != (len(prices) -1):
                outfile.write(",")
        outfile.write(" ] }")

    outfile.close()
