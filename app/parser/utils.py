from datetime import datetime
from typing import List, Optional
from pathlib import Path
from multiprocessing import Process, Queue
import asyncio
import re

import pandas as pd
import requests
from pandas import DataFrame

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)


async def get_data(link: str, save_dir: str = "./downloads"):
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    filename = link.split("/")[-1]
    file_path = Path(save_dir) / filename

    response = await asyncio.to_thread(requests.get, link)
    response.raise_for_status()
    await asyncio.to_thread(file_path.write_bytes, response.content)

    df = await asyncio.to_thread(pd.read_excel, file_path, header=None, engine="xlrd")

    await asyncio.to_thread(file_path.unlink)

    return df, filename


def get_date_from_file_name(filename):
    match = re.search(r"(\d{4})(\d{2})(\d{2})", filename)
    if match:
        year, month, day = match.groups()
        file_date = f"{day}.{month}.{year}"
        format_string = "%d.%m.%Y"
        date_object = datetime.strptime(file_date, format_string).date()
        return date_object
    return None


async def extract_table(
    df_raw: DataFrame, target_phrase: str = "Единица измерения: Метрическая тонна"
) -> DataFrame:
    mask = await asyncio.to_thread(
        df_raw.apply,
        lambda row: row.astype(str)
        .str.contains("Единица измерения:", case=False, na=False)
        .any(),
        axis=1,
    )

    markers: List[int] = mask[mask].index.tolist()

    if not markers:
        raise ValueError("Не найдено ни одной строки с 'Единица измерения:'")

    target_idx: Optional[int] = None
    for i in markers:
        row_text: str = " ".join(df_raw.iloc[i].astype(str))
        if target_phrase in row_text:
            target_idx = i
            break

    if target_idx is None:
        raise ValueError(f"Не найдена таблица с '{target_phrase}'")

    next_marker: int = next((m for m in markers if m > target_idx), len(df_raw))

    header_row: int = target_idx + 1
    data_start: int = header_row + 1

    columns: List[str] = df_raw.iloc[header_row].tolist()

    table: DataFrame = df_raw.iloc[data_start:next_marker].copy()
    table.columns = columns
    table.reset_index(drop=True, inplace=True)

    return table


async def filter_needed_columns(table: DataFrame) -> DataFrame:
    needed_columns = [
        "Код\nИнструмента",
        "Наименование\nИнструмента",
        "Базис\nпоставки",
        "Объем\nДоговоров\nв единицах\nизмерения",
        "Обьем\nДоговоров,\nруб.",
        "Количество\nДоговоров,\nшт.",
    ]

    df_selected = await asyncio.to_thread(lambda: table[needed_columns].copy())

    def convert_and_filter(df):
        df["Количество\nДоговоров,\nшт."] = (
            pd.to_numeric(df["Количество\nДоговоров,\nшт."], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        return df[df["Количество\nДоговоров,\nшт."] > 0].reset_index(drop=True)

    df_filtered = await asyncio.to_thread(convert_and_filter, df_selected)

    return df_filtered
