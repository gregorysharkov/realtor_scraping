import re
from functools import cache
from typing import Dict, List

import bs4

import src.parsing_utils as pu
import src.request_utils as ru
from src.data_classes import Deal


class DealList:
    '''responsible for getting and fetching a single page list'''
    link: str
    header: Dict
    page_content: str
    search_result_container: str = r'^BasePropertyCard'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def fetch_page_content(self) -> None:
        '''send post request to the server'''
        self.page_content = ru.get_page_content(
            self.link, self.header
        )  # type: ignore

    @property
    @cache
    def _page_soup(self):
        '''convert text into beautifull soup'''
        return ru.convert_content_into_soup(self.page_content)

    @property
    @cache
    def _item_list(self) -> List[bs4.BeautifulSoup]:
        '''returns a list of items on the pate'''

        if not self._page_soup:
            return None

        return self._page_soup.find_all(
            'div',
            class_=re.compile(self.search_result_container),
            id=re.compile(r'^property_id.+?'),
        )

    @property
    @cache
    def deals(self) -> List[Deal]:
        '''parse list of soup elements into a list of deals'''
        if not self._item_list:
            return None

        return [
            pu.parse_item(element) for element in self._item_list
        ]
