from bs4 import BeautifulSoup
import math
import asyncio
import os
import pandas as pd


async def coin_urls(session, num, sem):
    async with sem:
        response = await session.get(f'https://dexscreener.com/page-{num}?maxAge=48&min1HVol=1000&minLiq=500&order=desc&profile=0&rankBy=trendingScoreH6')
        soup = BeautifulSoup(response.text, 'lxml')
        url = soup.find('div', {'data-table-variant': 'top'}
                        ).find_all('a', {'class': 'dsp-hyDFHY dsp-jTWvec dsp-cGFOJB dsp-fPDMVc dsp-knRUXS dsp-cdmnDD dsp-hhWglN dsp-bWeShP dsp-fLKKbN dsp-cZvorF dsp-gfvIVs dsp-fBbMNf dsp-iRCHKA group'})
        url = [
            f'https://api.dexscreener.com/latest/dex/pairs{i.get('href')}' for i in url]
        return url


async def page_num(session):
    while True:
        try:
            response = await session.get(
                'https://dexscreener.com/?rankBy=trendingScoreH24&order=desc&minLiq=500&maxAge=48&min1HVol=1000&profile=0')
            if response.status_code != 200:
                raise ValueError('not 200')
            soup = BeautifulSoup(response.text, 'lxml')
            page_num = soup.find('div', {'class': 'custom-v0p5eh'}
                                 ).find('span', {'class': 'chakra-text custom-0'}).text
            page_num = (int(page_num.split(' ')[-1]) / 100)
            page_num = math.ceil(page_num)
            return page_num
        except Exception as e:
            print(e)
            await asyncio.sleep(2)


async def coin_info(session, url, sem):
    async with sem:
        response = await session.get(url)
        try:
            response = response.json()
            response = response.get('pairs')[0]
            info = {
                'name': response.get('baseToken', {}).get('name', None),
                'token_address': response.get('baseToken', {}).get('address', None),
                'pair_address': response.get('pairAddress'),
                'chain': response.get('chainId'),
                'dex_name': response.get('dexId'),
                'age': response.get('pairCreatedAt'),
                'price_usd': response.get('priceUsd'),
                'liquidity_usd': response.get('liquidity', {}).get('usd', None),
                'market_cap': response.get('marketCap'),
                'fdv': response.get('fdv'),
                'price_change_1h': response.get('priceChange', {}).get('h1', None),
                'txns_1h': response.get('txns', {}).get('h1', {}).get('buys', None) + response.get('txns', {}).get('h1', {}).get('sells', None),
                'buys_1h': response.get('txns', {}).get('h1', {}).get('buys', None),
                'sells_1h': response.get('txns', {}).get('h1', {}).get('sells', None),
                'volume_1h': response.get('volume', {}).get('h1', None),
                'price_change_6h': response.get('priceChange', {}).get('h6', None),
                'txns_6h': response.get('txns', {}).get('h6', {}).get('buys', None) + response.get('txns', {}).get('h6', {}).get('sells', None),
                'buys_6h': response.get('txns', {}).get('h6', {}).get('buys', None),
                'sells_6h': response.get('txns', {}).get('h6', {}).get('sells', None),
                'volume_6h': response.get('volume', {}).get('h6', None),
                'price_change_24h': response.get('priceChange', {}).get('h24', None),
                'txns_24h': response.get('txns', {}).get('h24', {}).get('buys', None) + response.get('txns', {}).get('h24', {}).get('sells', None),
                'buys_24h': response.get('txns', {}).get('h24', {}).get('buys', None),
                'sells_24h': response.get('txns', {}).get('h24', {}).get('sells', None),
                'volume_24h': response.get('volume', {}).get('h24', None),
                'is_socials': bool(response.get('info', {}).get('socials'))
            }
            return info

        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(1)


def add_to_csv(coin_infos, file):
    df = pd.DataFrame(coin_infos)

    is_exist = os.path.exists(file)

    df.to_csv(file, mode='a', header=not is_exist,
              encoding='utf-8', index=False)
    print(f'{len(df)} unique tokens have been added')
