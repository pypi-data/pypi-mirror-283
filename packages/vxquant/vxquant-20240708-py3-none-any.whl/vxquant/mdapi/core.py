"""行情接口核心组件"""

import polars as pl

import logging
import polars as pl
from pathlib import Path
from typing import List, Union, Dict, Tuple, Optional, Any, Literal
from datetime import datetime, date, timedelta
from typing import Union, Optional, List, Literal
from vxutils import Datetime, to_datetime
from vxquant.mdapi.loader import VXDataLoaderBase
from vxquant.mdapi.loaders.spiders import VXTencentHQ
from vxquant.models.nomalize import to_symbol as normalize_symbol


class VXCalendar:
    def __init__(
        self,
        trade_dates: Optional[Union[pl.Series, List[date], List[datetime]]] = None,
    ):

        self._data = pl.DataFrame(
            {
                "trade_date": pl.date_range(
                    date(1990, 1, 1), date.today().replace(month=12, day=31), eager=True
                )
            }
        ).with_columns(
            [
                pl.lit(False).cast(pl.Boolean).alias("is_trade_day"),
            ]
        )
        if trade_dates:
            self.update_data(trade_dates)

    def update_data(
        self, trade_dates: Union[pl.Series, List[Union[datetime, date, str, float]]]
    ) -> None:
        """更新交易日数据"""
        if not isinstance(trade_dates, pl.Series):
            trade_dates = pl.Series(trade_dates)

        trade_dates = trade_dates.map_elements(
            lambda x: to_datetime(x).date(), return_dtype=pl.Date
        )

        if max(trade_dates) > self._data["trade_date"].max():
            self._data = pl.concat(
                [
                    self._data,
                    pl.DataFrame(
                        {
                            "trade_date": pl.date_range(
                                self._data["trade_date"].max() + timedelta(days=1),
                                max(trade_dates).replace(month=12, day=31),
                                eager=True,
                            ),
                        }
                    ),
                ]
            )

        self._data = self._data.with_columns(
            pl.when(pl.col("trade_date").is_in(trade_dates))
            .then(True)
            .otherwise(pl.col("is_trade_day"))
            .alias("is_trade_date")
        )

    @property
    def max(self) -> date:
        return self._data["trade_date"].max()

    def add_holidays(
        self,
        start_date: Union[str, date, datetime, float],
        end_date: Union[str, date, datetime, float],
        holidays: List[Union[str, date, datetime, float]],
    ) -> None:
        """添加节假日"""
        holidays = pl.Series(holidays).map_elements(
            lambda x: to_datetime(x).date(), return_dtype=pl.Date
        )
        if holidays:
            start_date = max(to_datetime(start_date).date(), holidays.min())
            end_date = min(to_datetime(end_date).date(), holidays.max())
        else:
            start_date = to_datetime(start_date).date()
            end_date = to_datetime(end_date).date()
        trade_dates = pl.DataFrame(
            {"trade_date": pl.date_range(start_date, end_date, eager=True)}
        ).with_columns(
            pl.col("trade_date").not_().is_in(holidays).alias("is_trade_day")
        )[
            "trade_date"
        ]
        self.update_data(trade_dates)

    def is_trade_day(
        self,
        input_date: Optional[Union[datetime, date, float, str]] = None,
    ) -> bool:
        """判断是否交易日"""
        input_date = (
            to_datetime(input_date).date() if input_date is not None else date.today()
        )
        return input_date in self._data["trade_date"]

    def next_n_trade_day(
        self,
        n: int = 1,
        input_date: Optional[Union[datetime, date, float, str]] = None,
    ) -> date:
        """获取下n个交易日"""
        if n < 1:
            raise ValueError("n should be greater than 0")

        input_date = (
            to_datetime(input_date).date() if input_date is not None else date.today()
        )
        return self._data.filter(pl.col("trade_date") > input_date)["trade_date"][n - 1]

    def prev_n_trade_day(
        self,
        n: int = 1,
        input_date: Optional[Union[datetime, date, float, str]] = None,
    ) -> date:
        """获取前n个交易日"""
        if n < 1:
            raise ValueError("n should be greater than 0")

        input_date = (
            to_datetime(input_date).date() if input_date is not None else date.today()
        )
        return self._data.filter(pl.col("trade_date") < input_date)["trade_date"][-n]

    def date_range(
        self,
        start_date: Union[str, date, datetime, float],
        end_date: Union[str, date, datetime, float],
        perion: Literal["D", "W", "M"] = "D",
    ) -> pl.Series:
        """获取日期范围"""
        start_date = to_datetime(start_date).date()
        end_date = to_datetime(end_date).date()
        return self._data.filter(
            [pl.col("trade_date") >= start_date, pl.col("trade_date") <= end_date]
        )["trade_date"]


def is_in_periods(dt: Datetime, periods: List[Tuple[datetime, datetime]]) -> bool:
    """判断日期是否在时间段内"""
    dt = to_datetime(dt)
    return any(period[0] <= dt <= period[1] for period in periods)


class VXInstruments:
    """股票池类"""

    def __init__(self, name: str, registrations: Optional[pl.DataFrame] = None) -> None:
        self._name = name
        self._registrations = (
            registrations.with_columns(
                [
                    pl.col("start_date").cast(pl.Datetime),
                    pl.col("end_date").cast(pl.Datetime),
                ]
            )
            if registrations is not None
            else pl.DataFrame(
                {"symbol": [], "start_date": [], "end_date": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                },
            )
        )
        self._last_updated_dt = (
            datetime.today()
            if self._registrations.height == 0
            else to_datetime(self._registrations["end_date"].max())
        )

    @property
    def name(self) -> str:
        """股票池名称"""
        return self._name

    def __str__(self) -> str:
        return f"< 证券池({self._name}) " f" 最新证券:\n {self.list_instruments()} >"

    @property
    def registrations(self) -> pl.DataFrame:
        """股票池出入注册表

        Returns:
            pl.DataFrame -- 注册表
        """
        return self._registrations

    def list_instruments(self, trade_date: Optional[Datetime] = None) -> List[str]:
        """列出股票池中的证券

        Keyword Arguments:
            trade_date {Datetime} -- 交易日，若为空，则为当前日期 (default: {None})

        Returns:
            List[InstrumentType] -- 股票列表
        """
        trade_date = (
            to_datetime(trade_date) if trade_date is not None else datetime.today()
        )

        inst = self._registrations.filter(
            [(pl.col("start_date") <= trade_date), (pl.col("end_date") >= trade_date)]
        )

        return inst["symbol"].to_list()

    def add_instrument(
        self,
        symbol: str,
        start_date: Datetime,
        end_date: Optional[Datetime] = None,
        #
    ) -> "VXInstruments":
        try:
            symbol = normalize_symbol(symbol)
            start_date = to_datetime(start_date)
            end_date = to_datetime(end_date) if end_date else start_date
        except Exception as e:
            raise ValueError(f"参数错误: {e}")

        self._registrations.vstack(
            pl.DataFrame(
                [
                    {
                        "symbol": symbol,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                ],
                schema={
                    "symbol": str,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                },
            ),
            in_place=True,
        )
        return self

    def update_components(
        self,
        instruments: List[str],
        start_date: Datetime,
        end_date: Datetime,
    ) -> "VXInstruments":
        """按增量更新股票池"""

        end_date = to_datetime(end_date)
        start_date = to_datetime(start_date)

        new_instruments = pl.DataFrame(
            [
                {
                    "symbol": normalize_symbol(symbol),
                    "start_date": start_date,
                    "end_date": end_date,
                }
                for symbol in instruments
            ],
            schema={
                "symbol": pl.Utf8,
                "start_date": pl.Datetime,
                "end_date": pl.Datetime,
            },
        )

        self._registrations = pl.concat([self._registrations, new_instruments])
        self.rebuild()
        return self

    @classmethod
    def load(cls, name: str, instruments_file: Union[str, Path]) -> "VXInstruments":
        if isinstance(instruments_file, str):
            instruments_file = Path(instruments_file)

        if not instruments_file.exists():
            raise FileNotFoundError(f"{instruments_file} 不存在。")
        if instruments_file.suffix in {".csv"}:
            registrations = pl.read_csv(instruments_file)
        elif instruments_file.suffix in {".parquet"}:
            registrations = pl.read_parquet(instruments_file)
        else:
            raise ValueError(f"{instruments_file} 文件格式不支持。")

        return VXInstruments(name, registrations)

    def dump(
        self,
        instruments_file: Union[str, Path],
        *,
        file_suffix: Literal["csv", "parquet"] = "csv",
    ) -> "VXInstruments":
        """保存相关信息"""
        if isinstance(instruments_file, str):
            instruments_file = Path(instruments_file)

        if Path(instruments_file).is_dir():
            instruments_file = Path(instruments_file, f"{self._name}.{file_suffix}")

        if file_suffix == "csv":
            self._registrations.write_csv(instruments_file)
            logging.info(f"股票池:{self._name} 保存{instruments_file} 完成。")
        elif file_suffix == "parquet":
            self._registrations.write_parquet(instruments_file)
            logging.info(f"股票池:{self._name} 保存{instruments_file} 完成。")
        else:
            raise ValueError(f"{file_suffix} 文件格式不支持。")
        return self

    def rebuild(self) -> "VXInstruments":
        """重建登记表"""

        new_registrations = []
        temp_registrations = {}

        for rows in self._registrations.sort(by=["symbol", "start_date"]).iter_rows(
            named=True
        ):
            symbol = rows["symbol"]

            if symbol not in temp_registrations:
                temp_registrations[symbol] = rows
            elif (
                temp_registrations[symbol]["end_date"] + timedelta(days=1)
                >= rows["start_date"]
                and temp_registrations[symbol]["end_date"] < rows["end_date"]
            ):
                temp_registrations[symbol]["end_date"] = rows["end_date"]

            elif (temp_registrations[symbol]["end_date"]) < rows["start_date"]:
                new_registrations.append(temp_registrations[symbol])
                temp_registrations[symbol] = rows

        new_registrations.extend(temp_registrations.values())
        self._registrations = pl.DataFrame(new_registrations)

        return self

    def all_instruments(self) -> List[str]:
        return self._registrations["symbol"].unique().to_list()

    def union(self, *others: "VXInstruments") -> "VXInstruments":
        """合并另外一个股票池"""
        if len(others) == 1 and isinstance(others[0], (list, tuple)):
            others = others[0]

        registrations = [self._registrations] + [
            other._registrations for other in others
        ]
        self._registrations = pl.concat(registrations)
        self.rebuild()
        return self

    def intersect(self, other: "VXInstruments") -> "VXInstruments":
        """交集"""

        new_registrations: List[Dict[str, Any]] = []
        for rows in self.registrations.sort(["symbol", "start_date"]).iter_rows(
            named=True
        ):
            new_registrations.extend(
                {
                    "symbol": rows["symbol"],
                    "start_date": max(rows["start_date"], other_rows["start_date"]),
                    "end_date": min(rows["end_date"], other_rows["end_date"]),
                    # "weight": rows["weight"],
                }
                for other_rows in other.registrations.filter(
                    (pl.col("start_date") < rows["end_date"])
                    & (pl.col("end_date") > rows["start_date"])
                    & (pl.col("symbol") == rows["symbol"])
                ).iter_rows(named=True)
            )

        self._registrations = (
            pl.DataFrame(new_registrations)
            if new_registrations
            else pl.DataFrame(
                # {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                    # "weight": pl.Float64,
                },
            )
        )

        self.rebuild()
        return self

    def difference(self, other: "VXInstruments") -> "VXInstruments":
        """差集"""
        new_registrations = []
        for rows in self.registrations.sort(["symbol", "start_date"]).iter_rows(
            named=True
        ):
            for other_rows in (
                other.registrations.filter(
                    (pl.col("start_date") <= rows["end_date"])
                    & (pl.col("end_date") >= rows["start_date"])
                    & (pl.col("symbol") == rows["symbol"])
                )
                .sort("start_date")
                .iter_rows(named=True)
            ):
                if rows["start_date"] < other_rows["start_date"]:
                    new_registrations.append(
                        {
                            "symbol": rows["symbol"],
                            "start_date": rows["start_date"],
                            "end_date": other_rows["start_date"] - timedelta(days=1),
                        }
                    )

                rows["start_date"] = other_rows["end_date"] + timedelta(days=1)

                if rows["start_date"] > rows["end_date"]:
                    break

            if rows["start_date"] <= rows["end_date"]:
                new_registrations.append(rows)

        self._registrations = pl.DataFrame(new_registrations)
        self.rebuild()
        return self


class VXMdAPI:
    def __init__(self, data_loader: VXDataLoaderBase) -> None:
        self._data_loader = data_loader
        self._calendar = None
        self._instruments = {}
        data = self._data_loader.load_instruments()
        for row in data.iter_rows(named=True):
            if row["symbol"] == "T00018.SH":
                continue

            if row["list_date"] is None:
                logging.error(
                    f"数据错误: {row['symbol']},{row['name']},{row['list_date']},{row['delist_date']}"
                )
                continue

            if row["sec_type"] not in self._instruments:
                self._instruments[row["sec_type"]] = VXInstruments(name=row["sec_type"])

            self._instruments[row["sec_type"]].add_instrument(
                row["symbol"], row["list_date"], row["delist_date"]
            )
        self._current = VXTencentHQ()

    @property
    def data_loader(self) -> VXDataLoaderBase:
        """数据加载器

        Returns:
            VXDataLoaderBase -- 数据加载器
        """
        return self._data_loader

    @property
    def calendar(self) -> VXCalendar:
        """交易日历

        Returns:
            VXCalendar -- 交易日历类
        """
        if self._calendar is None:
            self._calendar = VXCalendar()
            trade_dates = self._data_loader.load_trade_dates("1990-01-01").filter(
                pl.col("is_open")
            )["trade_date"]
            self._calendar.update_data(trade_dates)
        return self._calendar

    def instruments(
        self, sec_type: Literal["stock", "index", "cbond", "etflof"] = "stock"
    ) -> VXInstruments:
        """获取证券池

        Keyword Arguments:
            sec_type {Literal[stock, index, cbond, etflof]} -- 证券类型 (default: {"stock"})

        Returns:
            VXInstruments -- 证券池
        """
        return self._instruments[sec_type]

    def history(
        self,
        symbols: Union[VXInstruments, List[str]],
        start_date: Datetime,
        end_date: Datetime,
        freq: Literal["d"] = "d",
    ) -> pl.DataFrame:
        """获取历史数据

        Arguments:
            symbols {Union[VXInstruments, List[str]]} -- 证券代码
            start_date {Datetime} -- 开始时间
            end_date {Datetime} -- 结束时间
            freq {Literal[&quot;d&quot;]} -- 数据频率 (default: {"d"})

        Returns:
            pl.DataFrame -- 历史数据，包含 symbol, date, open, high, low, close, volume 等字段
        """
        if isinstance(symbols, VXInstruments):
            symbols = symbols.all_instruments()
        return self._data_loader.load_history_data(symbols, start_date, end_date, freq)

    def factor(
        self,
        symbols: Union[VXInstruments, List[str]],
        start_date: Datetime,
        end_date: Datetime,
        factor: str,
    ) -> pl.DataFrame:
        """获取因子数据

        Arguments:
            symbols {Union[VXInstruments, List[str]]} -- 证券代码
            start_date {Datetime} -- 开始时间
            end_date {Datetime} -- 结束时间
            factor {str} -- 因子名称

        Returns:
            pl.DataFrame -- 因子数据，包含 symbol, date, factor_name 等字段
        """
        raise NotImplementedError

    @property
    def current(self) -> VXTencentHQ:
        """获取当前行情

        Arguments:
            symbols {Union[VXInstruments, List[str]]} -- 需要获取的证券代码

        Returns:
            pl.DataFrame -- 当前行情数据，包含 symbol, date, open, high, low, close, volume 等字段
        """
        return self._current
