import os
import logging
from abc import abstractmethod
from argparse import ArgumentParser
from datetime import datetime, timedelta
from dataclasses import dataclass
from time import sleep
from typing import List, Dict, Any, Protocol

import schedule
from dotenv import load_dotenv
from requests import Session
from tabulate import tabulate


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


class OutputStrategy(Protocol):
    @abstractmethod
    def output(self, formatted_news: List[Dict[str, str]]) -> None:
        raise NotImplementedError(f"output method must be implemented at {self.__class__.__name__}")


@dataclass
class ConsoleOutputStrategy(OutputStrategy):
    def output(self, formatted_news: List[Dict[str, str]]) -> None:
        longest_url = max(len(row["Link"]) for row in formatted_news)
        print(tabulate(formatted_news, headers="keys", tablefmt="rounded_grid", maxcolwidths=[30, 50, longest_url]))


@dataclass
class NewsFetcher:
    session: Any
    api_url: str
    search_query: str

    def fetch_news(self) -> List[Dict[str, Any]]:
        _from = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        params = {
            "q": self.search_query,
            "from": _from
        }
        logging.info(f"Searching for news from {_from} for query: {self.search_query}")
        response = self.session.get(self.api_url, params=params)
        if response.status_code != 200:
            logging.error(f"Failed to get news: {response.text}")
            return []
        return response.json().get("articles", [])


@dataclass
class NewsFormatter:
    def format_news(self, articles: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        table = []
        for article in articles:
            table.append({
                "Author": article["author"] or "N/A,",
                "Title": article["title"],
                "Description": article["description"],
                "Link": article["url"]
            })
        return sorted(table, key=lambda x: x["Title"])


def main(arguments):
    logging.info(f"Searching for news using query: {arguments.search_for}")
    sess = arguments.session
    api_url = os.getenv('NEWS_API_URL')
    search_query = arguments.search_for

    news_fetcher = NewsFetcher(sess, api_url, search_query)
    articles = news_fetcher.fetch_news()
    if not articles:
        logging.error(f"No news found for query: {search_query} at {datetime.now()}")
        return

    news_formatter = NewsFormatter()
    formatted_news = news_formatter.format_news(articles)

    output_strategy = ConsoleOutputStrategy()
    output_strategy.output(formatted_news)


if __name__ == '__main__':
    load_dotenv()

    session = Session()
    session.headers.update({
        "X-Api-Key": os.getenv("NEWS_API_TOKEN")
    })
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-s', "--search_for", help="Search for news", required=True)
    args = arg_parser.parse_args()
    args.session = session

    schedule.every(30).minutes.do(main, args)
    # schedule.every(30).seconds.do(main, args)  # for testing

    while True:
        schedule.run_pending()
        sleep(1)
