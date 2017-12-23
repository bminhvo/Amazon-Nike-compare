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



def parse_amazon_data():

    soupAmazon = bs4.BeautifulSoup(open("amazon.html"), "lxml")
    rows = soupAmazon.select('div.s-item-container')

    range_price = soupAmazon.find_all("span", "sx-price-whole")

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

    mens_index = []
    womens_index = []
    amazon_price_string = []
    amazon_rating_string = []
    amazon_price_low = []
    amazon_price_high = []
    amazon_price_indv = []


    amazon_mens_low = []
    amazon_womens_low = []
    amazon_mens_high = []
    amazon_womens_high = []
    amazon_mens_indv = []
    amazon_womens_indv = []

    for i in prices:
       if len(i) > 60:
        lower = i.partition(char1)[-1].rpartition(char2)[0]
        higher = i.partition(char3)[-1].rpartition(char4)[0]
        amazon_price_string.append(str("$"+lower+"-"+"$"+higher))
       else:
        indv = i.partition(">")[-1].rpartition("<")[0]
        amazon_price_string.append(str("$"+indv))



    for j in ratings:
        rate = j.partition('<span class="a-icon-alt">')[-1].rpartition('</span></i><i class="a-icon a-icon-popover">')[0]
        amazon_rating_string.append(rate)

    for i in range(len(amazon_rating_string)):
        if amazon_rating_string[i] == '':
            amazon_rating_string[i] = "No ratings."

    for i in amazon_price_string:
        if len(i) > 4:
            low_int = i.partition("$")[-1].rpartition("-")[0]
            high_int = i.split("-$")[1]
            amazon_price_low.append(int(low_int))
            amazon_price_high.append(int(high_int))
        else:
            indv_int = i.split("$")[1]
            amazon_price_indv.append(int(indv_int))

    average_low = sum(amazon_price_low) / len(amazon_price_low)
    average_high = sum(amazon_price_high) / len(amazon_price_high)
    average_indv = sum(amazon_price_indv) / len(amazon_price_indv)

    for i in range(len(descs)):
        if "Men's" in descs[i] or "Mens" in descs[i]:
            mens_index.append(i)
        elif "Women's" in descs[i] or "Womens" in descs[i]:
            womens_index.append(i)

    for i in mens_index:
        if len(amazon_price_string[i]) > 4:
            mens_low = amazon_price_string[i].partition("$")[-1].rpartition("-")[0]
            mens_high = amazon_price_string[i].split("-$")[1]
            amazon_mens_low.append(int(mens_low))
            amazon_mens_high.append(int(mens_high))
        else:
            mens_indv = amazon_price_string[i].split("$")[1]
            amazon_mens_indv.append(int(mens_indv))

    for i in womens_index:
        if len(amazon_price_string[i]) > 4:
            womens_low = amazon_price_string[i].partition("$")[-1].rpartition("-")[0]
            womens_high = amazon_price_string[i].split("-$")[1]
            amazon_womens_low.append(int(womens_low))
            amazon_womens_high.append(int(womens_high))
        else:
            womens_indv = amazon_price_string[i].split("$")[1]
            amazon_womens_indv.append(int(womens_indv))

    if len(amazon_mens_low) != 0:
        average_mens_low = sum(amazon_mens_low) / len(amazon_mens_low)
    else:
        average_mens_low = str("No lower (ranging) prices for men's products.")

    if len(amazon_mens_high) != 0:
        average_mens_high = sum(amazon_mens_high) / len(amazon_mens_high)
    else:
        average_mens_high = str("No higher (ranging) prices for men's products.")

    if len(amazon_mens_indv) != 0:
        average_mens_indv = sum(amazon_mens_indv) / len(amazon_mens_indv)
    else:
        average_mens_indv = str("No individual prices for men's products.")

    if len(amazon_womens_low) != 0:
        average_womens_low = sum(amazon_womens_low) / len(amazon_womens_low)
    else:
        average_womens_low = str("No lower (ranging) prices for women's products.")

    if len(amazon_womens_high) != 0:
        average_womens_high = sum(amazon_womens_high) / len(amazon_womens_high)
    else:
        average_womens_high = str("No higher (ranging) prices for women's products.")

    if len(amazon_womens_indv) != 0:
        average_womens_indv = sum(amazon_womens_indv) / len(amazon_womens_indv)
    else:
        average_womens_indv = str("No individual prices for women's products.")

    list_images_amazon = image_url("amazon.html", type = 'amazon')

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/js", "amazon-output.json")
    average_url = os.path.join(SITE_ROOT, "static/js", "amazon-average.json")

    with open(average_url, "w") as averageFile:
        json.dump({ 'average_womens_indv': average_womens_indv, 'average_womens_high': average_womens_high, 'average_womens_low': average_womens_low, 'average_mens_indv': average_mens_indv, 'average_mens_high': average_mens_high, 'average_mens_low': average_mens_low, 'average_low': average_low, 'average_high': average_high, 'average_indv': average_indv}, averageFile, indent=4)
    averageFile.close()


    with open(json_url, "w") as outfile:
        outfile.write("{ \"items\": [ ")
        for i in range(len(amazon_price_string)):
            json.dump({'name': descs[i], 'price': amazon_price_string[i], 'rating': amazon_rating_string[i], 'image': list_images_amazon[i] }, outfile, indent=4)
            if i != (len(amazon_price_string) -1):
                outfile.write(",")
        outfile.write(" ] }")

    outfile.close()
