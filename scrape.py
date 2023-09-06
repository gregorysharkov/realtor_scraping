from pathlib import Path

import pandas as pd

from src.deal_list import DealList

BASE_URL = 'https://www.realtor.com/realestateandhomes-search/Philadelphia_PA/show-recently-sold/pg-'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
}

PAGES_TO_SCRAPE = ['50', '51', '52']

OUTPUT_PATH = Path() / 'data'


def main():
    '''main application entry point'''
    scraped_deals = []
    for page in PAGES_TO_SCRAPE:
        deal_list = DealList(
            link=BASE_URL+page,
            header=HEADER,
        )

        deal_list.fetch_page_content()
        scraped_deals = scraped_deals + deal_list.deals
        print(f'page {page}, got {len(deal_list.deals)}')

    print(f'In total, got {len(scraped_deals)}')

    return_df = pd.DataFrame(
        data=[deal.to_list() for deal in scraped_deals],
        columns=['link', 'price', 'date', 'address']
    )

    return_df.to_csv(
        OUTPUT_PATH / 'scraped_deals.csv',
        sep=';',
        index=False
    )


if __name__ == '__main__':
    main()
