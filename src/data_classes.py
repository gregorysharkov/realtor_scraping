import re
from dataclasses import dataclass


@dataclass
class Deal:
    '''responsible for storing and representing a single deal'''
    link: str
    raw_price: str
    raw_date: str
    raw_address: str

    def to_list(self):
        '''list representation of the deal class'''
        price = re.sub(r'\D', '', self.raw_price).strip()
        price = float(price)

        deal_date = re.sub('Sold - ', '', self.raw_date).strip()
        return [self.link, price, deal_date, self.raw_address]
