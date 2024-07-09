"""数据加载器"""

import polars as pl
from typing import Optional, Literal, Union, List
from vxutils import Datetime
from vxquant.models.instruments import VXInstruments


class VXDataLoaderBase:

    def load_trade_dates(
        self, start_date: Datetime, end_date: Optional[Datetime] = None
    ) -> pl.DataFrame:
        """获取交易日历

        Arguments:
            start_date {Datetime} -- 开始时间

        Keyword Arguments:
            end_date {Optional[Datetime]} -- 结束时间 (default: {None})

        Returns:
            pl.DataFrame -- 交易日历, 包含 trade_date, is_open 等字段，其中 trade_date 为交易日，is_open 为是否开市
        """
        raise NotImplementedError

    def load_instruments(self) -> pl.DataFrame:
        """获取证券信息

        Arguments:
            sec_type {str} -- 证券类型

        Returns:
            pl.DataFrame -- 证券信息，包含 symbol, name, sec_type, list_date, delist_date 等字段
        """
        raise NotImplementedError

    def load_instruments_details(self, sec_type: str) -> pl.DataFrame:
        """获取证券详细信息

        Arguments:
            sec_type {str} -- 证券类型

        Returns:
            pl.DataFrame -- 证券详细信息，包含 symbol, name, sec_type, list_date, delist_date 等字段，以及其他相关信息
        """
        raise NotImplementedError

    def load_history_data(
        self,
        symbols: Union[VXInstruments, List[str]],
        start_date: Datetime,
        end_date: Optional[Datetime] = None,
        freq: Literal["d", "min"] = "d",
    ) -> pl.DataFrame:
        """获取历史数据

        Arguments:
            symbol {Union[VXInstruments, List[str]]} -- 证券代码
            start_date {Datetime} -- 开始时间
            end_date {Optional[Datetime]} -- 结束时间 (default: {None})

        Returns:
            pl.DataFrame -- 历史数据,包含 date,symbol,open,high,low,close,yclose,volume,amount 等字段
        """
        raise NotImplementedError

    def load_factors(self, factor_name: str) -> pl.DataFrame:
        """加载因子数据

        Arguments:
            factor_name {str} -- 因子名称

        Returns:
            pl.DataFrame -- 因子数据,包含 date,symbol,factor 等字段
        """
        raise NotImplementedError
