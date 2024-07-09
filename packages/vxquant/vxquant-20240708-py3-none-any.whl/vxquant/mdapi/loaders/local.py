"""本地数据加载器"""

import polars as pl

from pathlib import Path
from datetime import date
from typing import List, Literal, Union, Optional
from vxutils import Datetime, to_datetime
from vxquant.mdapi.loader import VXDataLoaderBase
from vxquant.models.instruments import VXInstruments


class VXLocalDataLoader(VXDataLoaderBase):
    def __init__(self, data_dir: Union[str, Path] = "~/.data/") -> None:
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def load_trade_dates(
        self, start_date: Datetime, end_date: Optional[Datetime] = None
    ) -> pl.DataFrame:
        start_date = to_datetime(start_date).date()
        if end_date is None:
            end_date = date.today().replace(month=12, day=31)
        else:
            end_date = to_datetime(end_date).date()
        return (
            pl.read_csv(self._data_dir / "calendar.csv")
            .select(
                pl.col("trade_date").str.to_date("%Y-%m-%d"),
                (pl.col("SHSE") == 1).alias("is_open"),
            )
            .filter(
                pl.col("trade_date") >= start_date,
                pl.col("trade_date") <= end_date,
            )
        )

    def load_instruments(self) -> pl.DataFrame:
        return pl.read_csv(self._data_dir / "instruments.csv")

    def load_history_data(
        self,
        symbols: Union[VXInstruments, List[str]],
        start_date: Datetime,
        end_date: Optional[Datetime] = None,
        freq: Literal["d", "min"] = "d",
    ) -> pl.DataFrame:
        start_date = to_datetime(start_date).date()
        end_date = date.today() if end_date is None else to_datetime(end_date).date()
        symbols = symbols if isinstance(symbols, list) else symbols.all_instruments()

        return pl.read_parquet(self._data_dir / f"daily.parquet").filter(
            pl.col("symbol").is_in(symbols),
            pl.col("date") >= start_date,
            pl.col("date") <= end_date,
        )
