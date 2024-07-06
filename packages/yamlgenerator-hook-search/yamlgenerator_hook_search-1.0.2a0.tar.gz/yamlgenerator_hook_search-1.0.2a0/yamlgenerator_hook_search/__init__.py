import concurrent.futures
import functools
from concurrent.futures import Future
from re import sub
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from gameyamlspiderandgenerator.exception import GenerateError
from gameyamlspiderandgenerator.hook import BaseHook
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.spider import get_text
from loguru import logger
from serpapi import GoogleSearch

# print(config, type(config))
Result = tuple[str | None, dict | None]


class APIRequestError(GenerateError):
    pass


def error_handler(original_function):
    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        try:
            result = original_function(*args, **kwargs)
            return result
        except Exception as e:
            logger.warning(f"An {type(e).__name__} occurred in {original_function.__name__}: {str(e)}")
            return None, None

    return wrapper_function


class Search(BaseHook):
    CHANGED = ["tags", "links", "publish", "platform"]
    REQUIRE_CONFIG = True

    def __init__(self):
        self.pure = None
        self.encode = None
        self.root_config = config()["hook_configs"]['search']
        if self.root_config['apple'] is None or self.root_config['apple'] is None:
            raise GenerateError('Starting from version 2.0.1, default configuration options are no longer provided. '
                                'Please obtain an API token from https://serpapi.com/ and fill it in the YAML '
                                'under the .hook_configs.search."google-play" and .hook_configs.search.apple sections.')

    @staticmethod
    def name_filter(string: str, pattern: str = r"[^A-z]", repl: str = ""):
        """

        Args:
            string: The string to be replaced
            pattern: Regular expression, replace non-English letters by default
            repl: The string to replace with

        Returns:

        """
        return sub(pattern, repl, string)

    @error_handler
    def search_play(self) -> Result:
        """
        publish
        """
        params = {
            "engine": "google_play",
            "q": self.encode,
            "api_key": self.root_config["google-play"],
            "store": "apps"
        }

        search = GoogleSearch(params)
        data = search.get_dict()
        if 'error' in data:
            raise APIRequestError(data['error'])
        if "organic_results" in data and any(
                self.name_filter(i["title"]) == self.pure for i in data["organic_results"][0]["items"]
        ):
            return "google-play", {
                'name': '.play-store',
                'uri': f'google-play-store:{data["organic_results"][0]["items"][0]["product_id"]}'
            }
        return None, None

    @error_handler
    def search_apple(self) -> Result:
        """
        publish
        """
        params = {
            "engine": "apple_app_store",
            "term": self.encode,
            "api_key": self.root_config["apple"]
        }

        search = GoogleSearch(params)
        data = search.get_dict()
        if 'error' in data:
            raise APIRequestError(data['error'])
        if "organic_results" in data and any(
                self.name_filter(i["title"]) == self.pure for i in data["organic_results"]
        ):
            return "apple-appstore", {
                'name': '.apple-appstore',
                'uri': data["organic_results"][0]["link"]
            }
        return None, None

    def search_all(self, type_tag: str) -> list:
        """
        publish
        """
        func_list = [
            getattr(self, i)
            for i in (list(filter(lambda x: "search_" in x and not x.endswith('_all'), self.__dir__())))
        ]
        func_list = list(filter(
            lambda x: x.__doc__.strip() == type_tag,
            func_list,
        ))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            result: list[Future] = [executor.submit(i) for i in func_list]
            return [i.result() for i in result]

    @error_handler
    def search_epic(self) -> Result:
        """
        publish
        """
        from epicstore_api import EpicGamesStoreAPI
        api = EpicGamesStoreAPI().fetch_store_games(keywords=self.encode, sort_dir="DESC")
        game_list = api['data']['Catalog']['searchStore']['elements']
        reg = r"[^A-z\d]"
        if game_list and any(
                [self.name_filter(i["title"]) == self.pure for i in game_list]):
            return "epic", {'name': '.epic',
                            'uri': f'https://store.epicgames.com/p/'
                                   f'{self.name_filter(game_list[0]["title"], pattern=reg, repl="-").lower()}'}
        return None, None

    @error_handler
    def search_xbox(self) -> Result:
        """
        platform
        """
        search_string = self.pure
        data = BeautifulSoup(get_text(f"https://www.xbox.com/en-us/search?q={quote_plus(search_string)}"
                                      ), features="lxml")

        if data.select_one('#nav-general > div > div') is None:
            return None, None
        else:
            data = data.select('#nav-general > div > div:nth-child(2) > div > h3 > a')
            data1 = [(i.attrs['href'], i.text.strip()) for i in data]
            for _, i in data1:
                if self.name_filter(self.pure, " ").lower() in self.name_filter(i, " ").lower():
                    return "xbox-one", None
            return None, None

    @error_handler
    def search_gog(self) -> Result:
        """
        publish
        """
        search_string = self.encode
        data = BeautifulSoup(get_text(f"https://www.gog.com/en/games?query={search_string}"
                                      ), features="lxml")

        if data.select_one('#Catalog > div.catalog__empty.ng-star-inserted > h2') is not None:
            return None, None
        else:
            data1 = data.select('product-title > span')
            data1 = [i.text for i in data1]
            data2 = data.select('product-tile > a')
            data2 = [i.attrs['href'] for i in data2]
            data1 = list(zip(data2, data1))
            for url, i in data1:
                if self.name_filter(self.pure, " ").lower() in self.name_filter(i, " ").lower():
                    return "gog", {'name': '.gog', 'uri': url}
            return None, None

    @error_handler
    def search_microsoft_store(self) -> Result:
        """
        publish
        """
        # TODO
        return None, None

    @error_handler
    def search_playstation_store(self) -> Result:
        """
        publish
        """
        search_string = self.encode
        data = BeautifulSoup(get_text(f"https://store.playstation.com/en-us/search/{search_string}"
                                      ), features="lxml")
        title = data.select_one("#main > section > div > ul > li:nth-child(1) > div > a > div > section > span")
        element = data.select_one("#main > section > div > ul > li:nth-child(1) > div > a")
        if title is None or element is None:
            return None, None
        title = title.text
        if self.name_filter(self.pure, " ").lower() in self.name_filter(title, " ").lower():
            return "playstation-store", {'name': '.playstation-store',
                                         'uri': 'https://store.playstation.com/'
                                                + data.select_one(
                                             "#main > section > div > ul > li:nth-child(1) > div > a").attrs['href']}
        return None, None

    def setup(self, data: dict):
        """
        hook handler
        Args:
            data: yaml data

        Returns:
            The processed dict data

        """
        self.pure = self.name_filter(data['name'])
        self.encode = quote_plus(self.name_filter(data['name'], repl=" "))
        temp = data.copy()
        result = self.search_all('publish')
        publish = set([i for i, ii in result if i is not None]) | set(temp["tags"]['publish']) - {None}
        link = [ii for i, ii in result if ii is not None]
        result = self.search_all('platform')
        platform = set([i for i, ii in result if i is not None]) | set(temp["tags"]["platform"]) - {None}
        link = link + [ii for i, ii in result if ii is not None] + temp["links"]
        temp["tags"]['publish'] = list(publish)
        temp["links"] = list(link)
        temp["tags"]["platform"] = list(platform)
        return temp
