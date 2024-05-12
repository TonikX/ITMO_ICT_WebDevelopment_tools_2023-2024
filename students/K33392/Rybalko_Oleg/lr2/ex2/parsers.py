import requests
import aiohttp
from datetime import datetime
import os
from bs4 import BeautifulSoup
from models import Transaction
from abc import ABC, abstractmethod


class AbstractParser(ABC):
    base_url: str

    @abstractmethod
    def parse(self) -> list[Transaction]:
        ...
    
    @abstractmethod
    async def aio_parse(self) -> list[Transaction]:
        ...
    
class BaseParser(AbstractParser):
    base_url: str

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(requests.get(self.base_url).text, "html.parser")

    async def aio_get_soup(self) -> BeautifulSoup:
        async with aiohttp.ClientSession() as client:
            async with client.get(self.base_url) as resp:
                return BeautifulSoup(await resp.read(), "html.parser")


class BlockchainComParser(BaseParser):
    def __init__(self):
        self.base_url = "https://www.blockchain.com/explorer/mempool/btc"

    def parse(self) -> list[Transaction]:
        return self.__parse(self.get_soup())
    
    async def aio_parse(self) -> list[Transaction]:
        return self.__parse(await self.aio_get_soup())
    
    def __parse(self, soup: BeautifulSoup):
        el = soup.find("div", class_="sc-7b53084c-1")
        trs = []
        for transaction in el:
            tr_hash = os.path.basename(transaction["href"])
            timestamp = datetime.strptime(transaction.find("div", class_="sc-35e7dcf5-7").text, "%m/%d/%Y, %H:%M:%S")
            amount = float(transaction.find("div", class_="sc-35e7dcf5-13").text.split()[0])
            trs.append(Transaction(transaction_id=int(tr_hash, 16), user_id=1, amount=amount, transaction_type="transfer", category_id=1, timestamp=timestamp))
        return trs

class BtcComParser(BaseParser):
    def __init__(self) -> None:
        self.base_url = "https://explorer.btc.com/btc/unconfirmed-txs"

    def parse(self) -> list[Transaction]:
        return self.__parse(self.get_soup())
    
    async def aio_parse(self) -> list[Transaction]:
        return self.__parse(await self.aio_get_soup())

    def __parse(self, soup: BeautifulSoup) -> list[Transaction]:
        table = soup.find("table")
        tbody = table.find("tbody")
        trs = []
        for row in tbody:
            tx_hash, timestamp, _, output_volume, _, _ = row.find_all("td")
            tx_hash = os.path.basename(tx_hash.find("a")["href"])
            trs.append(Transaction(
                transaction_id=int(tx_hash, 16),
                user_id=1,
                amount=float(output_volume.text.split()[0]),
                transaction_type="transfer",
                category_id=1,
                timestamp=datetime.strptime(timestamp.text, "%Y-%m-%d %H:%M:%S")
            ))
        return trs
