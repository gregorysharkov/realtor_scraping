import random
import time
from functools import reduce
from pathlib import Path
from typing import List

import pandas as pd
from tqdm import tqdm

from src.deal_list import DealList

BASE_URL = 'https://www.realtor.com/realestateandhomes-search/Philadelphia_PA/show-recently-sold'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
}

PAGES_TO_SCRAPE = ['', *[f'/pg-{page}' for page in range(2, 51, 1)]]

OUTPUT_PATH = Path() / 'data'


def scrape_chunk(chunk: List[str], chunk_id: int) -> None:
    '''scrapes and stores a chunk'''
    scraped_deals = []

    for page in tqdm(chunk, f'Scraping chunk {chunk_id +1}'):
        deal_list = DealList(
            link=BASE_URL+page,
            header=HEADER,
        )

        deal_list.fetch_page_content()
        scraped_deals = scraped_deals + deal_list.deals if deal_list.deals else scraped_deals
        time.sleep(random.randint(1, 5))
        # print(f'page {page}, got {len(deal_list.deals)}')

    return_df = pd.DataFrame(
        data=[deal.to_list() for deal in scraped_deals],
        columns=[
            'link', 'price', 'date',
            'street_address', 'city', 'state', 'zip'
        ]
    )

    return_df.to_csv(
        OUTPUT_PATH / f'scraped_deals_{chunk_id}.csv',
        sep=';',
        index=False
    )
    slep_time = random.randint(10, 20)
    print(f'Waiting {slep_time} sec')
    time.sleep(slep_time)


def main():
    '''main application entry point'''
    chunk_size = 10
    chunks = [
        PAGES_TO_SCRAPE[i:min(i+chunk_size, len(PAGES_TO_SCRAPE))]
        for i in range(0, len(PAGES_TO_SCRAPE), chunk_size)
    ]

    # for idx, chunk in enumerate(chunks):
    #     scrape_chunk(chunk, idx)
    scrape_chunk(chunks[-1], 4)

    chunks = []
    for idx in range(5):
        chunk_data = pd.read_csv(
            OUTPUT_PATH / f'scraped_deals_{idx}.csv',
            sep=';'
        )
        chunks.append(chunk_data)

    combined_data = reduce(lambda x, y: pd.concat([x, y]), chunks)
    combined_data.to_csv(
        OUTPUT_PATH / 'scraped_deals_combined.csv',
        sep=';',
        index=False,
    )


if __name__ == '__main__':
    main()
