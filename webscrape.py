#! python3
# webscrap.py - Searched Amazon and Nike and compares prices
import webbrowser, requests, bs4
from getData import get_data
from amazon_parse_html import parse_amazon_data
from nike_parse_html import parse_nike_data

def present_prices(keyword):
    get_data(keyword)
    parse_amazon_data()
    parse_nike_data()
