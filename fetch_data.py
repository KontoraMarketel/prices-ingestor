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

            async with session.get(GET_ALL_PRICES, params=params) as response:
                data = await response.json()
                response.raise_for_status()
                goods = data.get("data", {}).get("listGoods", [])

                if not goods:
                    break

                result.extend(goods)
                offset += limit

    return result
