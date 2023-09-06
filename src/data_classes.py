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
        return [
            self.link, price, deal_date,
            self.street_address, self.city, self.state, self.zip,
        ]

    @property
    def zip(self):
        return

    @property
    def street_address(self):
        return self.raw_address.split(',')[0]

    @property
    def zip(self):
        return self.raw_address.split(',')[-1]\
            .strip()[-5:]

    @property
    def state(self):
        return self.raw_address.split(',')[-1]\
            .strip()[:-6]

    @property
    def city(self):
        return self.raw_address.split(',')[1]\
            .strip()
