import asyncio
import logging

import aiohttp

GET_ALL_PRICES = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"


async def fetch_data(api_token: str) -> list:
    headers = {
        "Authorization": api_token
    }
    limit = 1000
    offset = 0
    result = []

    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            params = {
                "limit": limit,
                "offset": offset,
            }

            data = await fetch_page_with_retry(session=session, url=GET_ALL_PRICES, params=params)
            goods = data.get("data", {}).get("listGoods", [])

            if not goods:
                break

            result.extend(goods)
            offset += limit

    return result


async def fetch_page_with_retry(session, url, params):
    while True:
        async with session.get(url, params=params) as response:
            if response.status == 429:
                retry_after = int(response.headers.get('X-Ratelimit-Retry', 10))
                logging.warning(f"Rate limited (429). Retrying after {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                continue

            response.raise_for_status()
            return await response.json()
