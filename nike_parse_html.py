#! python3
# parse_html.py

import requests, sys, webbrowser, bs4
import json
import os
from flask import Flask, send_file, make_response, request, render_template, url_for, json

def image_url(filename):
	myfile = open(filename)
	soup_object = bs4.BeautifulSoup(myfile.read(), 'lxml')

	divtag = soup_object.findAll('div', \
		attrs={'class':'grid-item-image'})

	links = [divtag[i].findAll('img')[0]['src']\
	 for i in range(len(divtag))]

	return links



def parse_nike_data():

    char1 = '>'
    char2 = '<'

    # Nike - Retrieve data from first 5 results
    soupNike = bs4.BeautifulSoup(open("nike.html"), "lxml")
    nameElemsNike = soupNike.select('p.product-display-name')
    priceElemsNike = soupNike.select('span.local.nsg-font-family--base')
    genderElemsNike = soupNike.select('p.product-subtitle')

    nike_price_class = []
    nike_gender_class = []
    nike_name_class = []

    nike_price = []
    nike_gender = []
    nike_name = []

    nike_price_float = []
    nike_price_mens = []
    nike_price_womens = []

    mens_index = []
    womens_index = []

    for j in priceElemsNike:
        nike_price_class.append(str(j))
    for i in genderElemsNike:
        nike_gender_class.append(str(i))
    for k in nameElemsNike:
        nike_name_class.append(str(k))

    for n in nike_name_class:
        nike_name.append(n.partition(char1)[-1].rpartition(char2)[0])

    for g in nike_gender_class:
        nike_gender.append(g.partition(char1)[-1].rpartition(char2)[0])

    for p in nike_price_class:
        nike_price.append(p.partition(char1)[-1].rpartition(char2)[0])

    for i in nike_price:
        price_total = i.split("$")[1]
        nike_price_float.append(float(price_total))

    for i in range(len(nike_gender)):
        if "Men's" in nike_gender[i]:
            mens_index.append(i)
        elif "Women's" in nike_gender[i]:
            womens_index.append(i)

    for i in mens_index:
        nike_price_mens.append(nike_price_float[i])
    for i in womens_index:
        nike_price_womens.append(nike_price_float[i])

    average_total = round((sum(nike_price_float) / len(nike_price_float)),2)

    if len(nike_price_mens) != 0:
        average_mens = round((sum(nike_price_mens) / len(nike_price_mens)),2)
    else:
        average_mens = str("No prices for men's products.")

    if len(nike_price_womens) != 0:
        average_womens = round((sum(nike_price_womens) / len(nike_price_womens)),2)
    else:
        average_womens = str("No prices for women's products.")


    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/js", "nike-output.json")

    average_url = os.path.join(SITE_ROOT, "static/js", "nike-average.json")

    list_images_nike = image_url("nike.html")

    with open(average_url, "w") as averageFile:
        json.dump({'average_total': average_total, 'average_mens': average_mens, 'average_womens': average_womens}, averageFile, indent=4)
	bar_url = os.path.join(SITE_ROOT, "static/js", "nike-bar.json")
	with open(bar_url, "w") as barFile:
	    json.dump([ {"Category": "average_total", "Price":average_total}, {"Category": "average_mens", "Price":average_mens}, {"Category": "average_womens", "Price":average_womens}], barFile, indent=4)
	barFile.close()
    averageFile.close()

    with open(json_url, "w") as outfile:
        outfile.write("{ \"items\": [ ")
        #json.dump({'average_total': average_total, 'average_mens': average_mens, 'average_womens': average_womens}, outfile, indent=4)
        #outfile.write(",")
        for i in range(len(nike_price)):
            json.dump({'name': nike_name[i], 'gender': nike_gender[i], 'price': nike_price[i], 'image': list_images_nike[i] }, outfile, indent=4)
            if i != (len(nike_price) -1):
                outfile.write(",")
        outfile.write(" ] }")

    outfile.close()
