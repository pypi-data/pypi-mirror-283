"""Uma source que obtém preços de venda de fundos do Tesouro Direto.

O ticker é composto pelo título em letras maiúsculas, sem espaços, sem o
caractere "+", e com o ano de vencimento no final. Títulos com juros semestrais
recebem o sufixo "JS", e títulos com aposentadoria extra recebem o sufixo "AE".

Exemplos: "TESOUROSELIC2026", "TESOUROIPCAJS2024", "TESOUROPREFIXADO2023".
"""

import csv
from bisect import bisect_left
from datetime import date, datetime
from decimal import Decimal

import requests

from ._source import SourcePrice

_BASE_URL = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"


def parse_ticker(tipo_titulo: str, data_vencimento: date) -> str:
    ano = data_vencimento.year

    return tipo_titulo.replace("com Juros Semestrais", "JS").replace(
        "Aposentadoria Extra", "AE"
    ).replace(" ", "").replace("+", "").upper() + str(ano)


class Source:
    prices: dict[str, list[tuple[date, Decimal]]] | None

    def __init__(self) -> None:
        self.prices = None

    def _download_prices(self) -> None:
        if self.prices is not None:
            return

        response = requests.get(_BASE_URL)
        response.raise_for_status()

        self.prices = {}
        for row in csv.DictReader(response.text.splitlines(), delimiter=";"):
            tipo_titulo = row["Tipo Titulo"]
            data_vencimento = datetime.strptime(
                row["Data Vencimento"], "%d/%m/%Y"
            ).date()
            data_base = datetime.strptime(row["Data Base"], "%d/%m/%Y").date()
            pu_venda = Decimal(row["PU Venda Manha"].replace(",", "."))

            ticker = parse_ticker(tipo_titulo, data_vencimento)
            if ticker not in self.prices:
                self.prices[ticker] = []
            self.prices[ticker].append((data_base, pu_venda))

        for ticker in self.prices:
            self.prices[ticker].sort()

    def get_latest_price(self, ticker: str) -> SourcePrice | None:
        """Get the latest price for a given ticker."""
        self._download_prices()

        if self.prices is None or ticker not in self.prices:
            return None

        last_date, last_price = self.prices[ticker][-1]
        return SourcePrice(
            price=last_price,
            time=datetime.combine(last_date, datetime.min.time()),
            quote_currency="BRL",
        )

    def get_historical_price(self, ticker: str, dt: datetime) -> SourcePrice | None:
        """Get the price for a given ticker on a given date."""
        self._download_prices()

        if self.prices is None or ticker not in self.prices:
            return None

        prices = self.prices[ticker]
        if not prices:
            return None

        idx = bisect_left(prices, (dt.date(), Decimal("0")))
        if idx == len(prices):
            idx -= 1

        return SourcePrice(
            price=prices[idx][1],
            time=datetime.combine(prices[idx][0], datetime.min.time()),
            quote_currency="BRL",
        )

    def get_prices_series(
        self, ticker: str, start_dt: datetime, end_dt: datetime
    ) -> list[SourcePrice]:
        """Get the prices for a given ticker within a date range."""
        self._download_prices()

        if self.prices is None or ticker not in self.prices:
            return []

        prices = self.prices[ticker]
        if not prices:
            return []

        start_idx = bisect_left(prices, (start_dt.date(), Decimal("0")))
        end_idx = bisect_left(prices, (end_dt.date(), Decimal("0")))

        if start_idx == len(prices):
            start_idx -= 1

        if end_idx == len(prices):
            end_idx -= 1

        return [
            SourcePrice(
                price=price,
                time=datetime.combine(dt, datetime.min.time()),
                quote_currency="BRL",
            )
            for dt, price in prices[start_idx:end_idx]
        ]
