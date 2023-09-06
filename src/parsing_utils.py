import re
from typing import List

import bs4

from src.data_classes import Deal

DATE_SOLD_CLASS = 'base__StyledType-rui__sc-108xfm0-0 kpUjhd message'
PRICE_CLASS = 'Pricestyles__StyledPrice-rui__btk3ge-0 bvgLFe card-price'
ADDRESS_CLASS = 'card-address truncate-line'
LINK_CLASS = 'card-anchor'


def get_item_list(page_content: bs4.BeautifulSoup) -> List[bs4.BeautifulSoup]:
    '''returns a list of items on the pate'''

    if not page_content:
        return None

    return page_content.find_all('div', class_=re.compile(r'^BasePropertyCard'))


def parse_items(element_list: List[bs4.BeautifulSoup]) -> List[Deal]:
    '''parse list of soup elements into a list of deals'''
    if not element_list:
        return None

    return [
        parse_item(element) for element in element_list
    ]


def parse_item(element: bs4.BeautifulSoup) -> Deal:
    '''create a deal object'''

    date_sold = get_date_sold(element)
    price = get_price(element)
    address = get_address(element)
    link = get_item_link(element)

    return Deal(
        raw_date=date_sold,
        raw_price=price,
        raw_address=address,
        link=link,
    )


def get_date_sold(element: bs4.BeautifulSoup) -> str:
    '''returns the date when the item got sold'''
    if not element:
        return None
    found_element = element.find('div', class_=DATE_SOLD_CLASS)
    if not found_element:
        return 'no date'
    return found_element.text.strip()


def get_price(element: bs4.BeautifulSoup) -> str:
    '''search for price element'''
    if not element:
        return None
    found_element = element.find('div', class_=PRICE_CLASS)
    if not found_element:
        return 'no date'
    return found_element.text.strip()


def get_address(element: bs4.BeautifulSoup) -> str:
    '''search for address element'''
    if not element:
        return None
    found_element = element.find('div', class_=ADDRESS_CLASS)
    if not found_element:
        return 'no date'
    return ', '.join(x.text.strip() for x in found_element.children)


def get_item_link(element: bs4.BeautifulSoup) -> str:
    '''search for link to the element'''
    if not element:
        return None
    found_element = element.find('a', class_=LINK_CLASS)
    if not found_element:
        return 'no link'
    return found_element.get('href', 'no link')
