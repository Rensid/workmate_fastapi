from multiprocessing import Process, Queue
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
import asyncio
from datetime import date, datetime, timedelta
from typing import List
from pandas import DataFrame
from sqlalchemy.dialects.postgresql import insert

from app.parser.parser import parse_page_links
from base import async_session
from models import ExchangeProduct
from app.parser.utils import (
    extract_table,
    filter_needed_columns,
    get_data,
    get_date_from_file_name,
)


def df_to_models(df: DataFrame, date_) -> list[ExchangeProduct]:
    """возвращает список ExchangeProduct вытаскивая их из DataFrame"""
    today = datetime.now().date()

    return [
        ExchangeProduct(
            exchange_product_id=str(row["Код\nИнструмента"]).strip(),
            exchange_product_name=str(row["Наименование\nИнструмента"]).strip(),
            oil_id=str(row["Код\nИнструмента"])[:4],
            delivery_basis_id=str(row["Код\nИнструмента"])[4:7],
            delivery_basis_name=str(row["Базис\nпоставки"]).strip(),
            delivery_type_id=str(row["Код\nИнструмента"])[-1],
            volume=float(row["Объем\nДоговоров\nв единицах\nизмерения"]),
            total=float(row["Обьем\nДоговоров,\nруб."]),
            count=int(row["Количество\nДоговоров,\nшт."]),
            date=date_,
            created_on=today,
            updated_on=today,
        )
        for _, row in df.iterrows()
    ]


async def fetch_page(url: str) -> str:
    """Получает HTML c отправленного url"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


def worker(q, content):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        table = await extract_table(content)
        table = await filter_needed_columns(table)
        return table

    result = loop.run_until_complete(main())
    loop.close()
    q.put(result)


async def get_raw_data(file_url: str, date_: date):
    """Получает данные из HTML, вытаскивает нужную таблицу,
    фильтрует по колонке и возврает объекты модели"""
    content, filename = await get_data(file_url)
    date_ = get_date_from_file_name(filename)
    q = Queue()
    p = Process(target=worker, args=(q, content))
    p.start()
    p.join()
    table = q.get()
    return df_to_models(table, date_)


async def save_to_db(products: List[ExchangeProduct]):
    """Сохраняет в базу продукты, минуя конфликтные"""
    async with async_session() as session:
        for product in products:
            product_dict = product.to_dict()
            stmt = (
                insert(ExchangeProduct)
                .values(product_dict)
                .on_conflict_do_nothing(index_elements=["exchange_product_id"])
            )
            await session.execute(stmt)
        await session.commit()


async def process_link(link):
    file_url, file_date = link
    products: List[ExchangeProduct] = await get_raw_data(file_url, file_date)
    return products


async def get_data_from_url():
    start = datetime.now()
    url = "https://spimex.com/markets/oil_products/trades/results/"
    html = await fetch_page(url)

    end_date = date.today()
    start_date = end_date - timedelta(days=730)
    links = parse_page_links(html, start_date, end_date, url)

    sem = asyncio.Semaphore(5)

    async def limited(link):
        async with sem:
            return await process_link(link)

    results = await asyncio.gather(*(limited(link) for link in links))

    products = [item for group in results for item in group]

    await save_to_db(products)
    print(datetime.now() - start)
