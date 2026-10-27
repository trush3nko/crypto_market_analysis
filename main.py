import asyncio
from curl_cffi.requests import AsyncSession
from functions import coin_urls, page_num, coin_info, add_to_csv
import pandas as pd
import time


async def main():
    sem = asyncio.Semaphore(5)
    df = pd.read_csv('crypto.csv')
    df = [i.lower() for i in df['pair_address']]

    async with AsyncSession(impersonate='chrome') as session:
        pages = await asyncio.gather(page_num(session))
        url_tasks = [coin_urls(session, i, sem)
                     for i in range(1, pages[0] + 1)]
        result = await asyncio.gather(*url_tasks)
        urls = []
        for i in result:
            for j in i:
                if j.split('/')[-1] not in df:
                    urls.append(j)

        info_tasks = [coin_info(session, i, sem) for i in urls]
        coin_infos = await asyncio.gather(*info_tasks)
        coin_infos = [i for i in coin_infos if i is not None]

        add_to_csv(coin_infos, 'crypto.csv')

while True:
    if __name__ == '__main__':
        asyncio.run(main())

    time.sleep(7200)
